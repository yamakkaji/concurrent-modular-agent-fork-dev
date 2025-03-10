import os, datetime, uuid
import numpy as np
from loguru import logger
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from dataclasses import dataclass
import warnings
import datetime

@dataclass
class StateRecord:
    id: str
    text: str
    vector: np.ndarray
    timestamp: float
    
from dataclasses import dataclass
import numpy as np

@dataclass
class StateRecord:
    id: str
    text: str
    vector: np.ndarray
    timestamp: float

class State:
    def __init__(self, ids, texts, vector, timestamps):
        if len(ids) != len(texts) or len(ids) != len(vector) or len(ids) != len(timestamps):
            raise ValueError("The length of ids, texts, vectors, and timestamps must be the same.")
        if isinstance(ids, np.ndarray):
            ids = ids.tolist()
        if isinstance(texts, np.ndarray):
            texts = texts.tolist()
        if isinstance(timestamps, np.ndarray):
            timestamps = timestamps.tolist()
        self.ids = ids
        self.texts = texts
        self.vector = np.array(vector)  # Ensure vector is a NumPy array
        self.timestamps = timestamps
    
    def __len__(self):
        return len(self.ids)

    def __getitem__(self, i):
        if isinstance(i, int):  # 単一の整数インデックス
            return StateRecord(
                id=self.ids[i],
                text=self.texts[i],
                vector=self.vector[i],
                timestamp=self.timestamps[i]
            )
        elif isinstance(i, (list, tuple, np.ndarray)):  # リスト、タプル、NumPy配列
            indices = np.array(i, dtype=int)  # NumPy配列に変換
            return State(
                ids=[self.ids[idx] for idx in indices],
                texts=[self.texts[idx] for idx in indices],
                vector=self.vector[indices],
                timestamps=[self.timestamps[idx] for idx in indices]
            )
        elif isinstance(i, slice):  # スライス
            return State(
                ids=self.ids[i],
                texts=self.texts[i],
                vector=self.vector[i],
                timestamps=self.timestamps[i]
            )
        else:
            raise TypeError("Indexing must be an integer, list, tuple, NumPy array, or slice.")


class StateClient():
    def __init__(self, agent_name, module_name:str=None):
        self._chromadb_client = chromadb.HttpClient(host='localhost', port=8000)
        self._embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv('OPENAI_API_KEY'),
            model_name="text-embedding-ada-002"
        )
        self._chromadb_collection = self._chromadb_client.get_or_create_collection(
            self._make_collection_name(agent_name),
            embedding_function=self._embedding_function)

    def _make_collection_name(self, agent_name):
        return f"{__package__}-state-{agent_name}"
    
    def add(self, states:str|list, timestamp:float|datetime.datetime=None):
        if type(states) == str:
            states = [states]
        n = len(states)
        ids = [str(uuid.uuid4()) for i in range(n)]
        if timestamp is None:
            now = datetime.datetime.now().timestamp()
            timestamps = [now for i in range(n)]
        else:
            if type(timestamp) == datetime.datetime:
                timestamp = timestamp.timestamp()
            timestamps = [timestamp for i in range(n)]
        metadatas = [{'timestamp': t} for t in timestamps]
        self._chromadb_collection.add(ids=ids, documents=states, metadatas=metadatas)
    
    def latest(self, max_count:int=10):
        data = self._chromadb_collection.get(include=['embeddings', 'documents', 'metadatas'])
        timestamp = [m['timestamp'] for m in data['metadatas']]
        index = np.argsort(timestamp)[::-1]
        if max_count is not None and max_count > 0:
            index = index[:max_count]
        ids = np.array(data['ids'])[index]
        texts = np.array(data['documents'])[index]
        vector = np.array(data['embeddings'])[index]
        timestamps = np.array([m['timestamp'] for m in data['metadatas']])[index]
        state = State(
            ids=ids,
            texts=texts,
            vector=vector,
            timestamps=timestamps
        )
        return state
    
    def retrieve(self, query_text:str, max_count:int=10):
        warnings.warn("The 'retrieve' method is deprecated, use 'query' method instead.", DeprecationWarning)
        return self.query(query_text=query_text, max_count=max_count)
    
    def query(self, query_text:str, max_count:int=10, return_distances:bool=False):
        query_include = ['embeddings', 'documents', 'metadatas']
        if return_distances:
            query_include.append('distances')
        data = self._chromadb_collection.query(query_texts=query_text, 
                                               n_results=max_count, 
                                               include=query_include)
        ids = np.array(data['ids'])[0]
        texts = np.array(data['documents'])[0]
        vector = np.array(data['embeddings'])[0]
        timestamps = np.array([m['timestamp'] for m in data['metadatas'][0]])
        state = State(
            ids=ids,
            texts=texts,
            vector=vector,
            timestamps=timestamps
        )
        if return_distances:
            return state, data['distances'][0]
        else:
            return state

    def delete(self, id:str):
        raise NotImplementedError("The delete method is not implemented yet.")

    def count(self):
        n = self._chromadb_collection.count()
        return n
    
    def clear(self):
        collection_name = self._chromadb_collection.name
        self._chromadb_client.delete_collection(collection_name)
        self._chromadb_collection = self._chromadb_client.create_collection(
            collection_name, 
            embedding_function=self._embedding_function)


    
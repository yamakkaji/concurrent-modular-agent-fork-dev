import os, datetime, uuid
import numpy as np
from loguru import logger
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from dataclasses import dataclass



@dataclass
class StateRecord:
    id: str
    text: str
    vector: np.ndarray
    timestamp: float
    

@dataclass
class State:
    ids: list[str]
    texts: list[str]
    vector: np.ndarray
    timestamps: list[float]
    def __init__(self, ids, texts, vector, timestamps):
        if len(ids) != len(texts) or len(ids) != len(vector) or len(ids) != len(timestamps):
            raise ValueError("The length of ids, texts, vectors, and timestamps must be the same.")
        if type(ids) == np.ndarray:
            ids = ids.tolist()
        if type(texts) == np.ndarray:
            texts = texts.tolist()
        if type(timestamps) == np.ndarray:
            timestamps = timestamps.tolist()
        self.ids = ids
        self.texts = texts
        self.vector = vector
        self.timestamps = timestamps
    
    def __len__(self):
        return len(self.ids)

    def __getitem__(self, i):
        return StateRecord(
            id=self.ids[i],
            text=self.texts[i],
            vector=self.vector[i],
            timestamp=self.timestamps[i]
        )


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
    
    def add(self, states:str|list):
        if type(states) == str:
            states = [states]
        n = len(states)
        ids = [str(uuid.uuid4()) for i in range(n)]
        now = datetime.datetime.now().timestamp()
        timestamps = [now for i in range(n)]
        metadatas = [{'timestamp': t} for t in timestamps]
        self._chromadb_collection.add(ids=ids, documents=states, metadatas=metadatas)
    
    def latest(self, max_count:int=10):
        data = self._chromadb_collection.get(include=['embeddings', 'documents', 'metadatas'])
        timestampe = [m['timestamp'] for m in data['metadatas']]
        index = np.argsort(timestampe)[::-1][:max_count]
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
        data = self._chromadb_collection.query(query_texts=query_text, n_results=max_count, include=['embeddings', 'documents', 'metadatas'])
        # import ipdb; ipdb.set_trace()
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


    
import os, datetime, uuid
import numpy as np
from loguru import logger
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from dataclasses import dataclass
import warnings
import datetime
from .state import State

class StateClient():
    def __init__(self, agent_name, module_name:str=None):
        self._chromadb_client = chromadb.HttpClient(host='localhost', port=8000)
        self._embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv('OPENAI_API_KEY'),
            model_name="text-embedding-ada-002"
        )
        self._chromadb_collection = self._chromadb_client.get_or_create_collection(
            self._make_collection_name(agent_name),
            # embedding_function=self._embedding_function
            embedding_function=None
        )
        self._chromadb_collection._embedding_function = self._embedding_function

    def _make_collection_name(self, agent_name):
        return f"{__package__}-state-{agent_name}"
    
    def add(self, 
            states:str|list, 
            timestamp:float|datetime.datetime=None, 
            metadata:dict=None):
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
        if metadata is not None:
            for m in metadatas:
                m.update(metadata)
        self._chromadb_collection.add(ids=ids, documents=states, metadatas=metadatas)

    def get(self, max_count:int=None, metadata:dict=None, reverse:bool=False):
        if metadata is None:
            data = self._chromadb_collection.get(include=['embeddings', 'documents', 'metadatas'])
        else:
            data = self._chromadb_collection.get(include=['embeddings', 'documents', 'metadatas'], where=metadata)
        state = self._convert_chromadb_data_to_state(data)
        index = np.argsort(state.timestamps)[::-1]
        state = state[index]
        if reverse:
            state = state[::-1]
        if max_count is not None and max_count > 0:
            state = state[:max_count]
        return state

    def query(self, query_text:str, max_count:int=10, return_distances:bool=False, metadata:dict=None):
        query_include = ['embeddings', 'documents', 'metadatas']
        if return_distances:
            query_include.append('distances')
        if metadata is None:
            data = self._chromadb_collection.query(query_texts=query_text, n_results=max_count, include=query_include)
        else:
            data = self._chromadb_collection.query(query_texts=query_text, n_results=max_count, include=query_include, where=metadata)
                                               
        ids = data['ids'][0]
        texts = data['documents'][0]
        vector = data['embeddings'][0]
        timestamps = []
        metadata = []
        for m in data['metadatas'][0]:
            timestamps.append(m['timestamp'])
            m.pop('timestamp')
            metadata.append(m)
        state = State(
            ids=ids,
            texts=texts,
            vector=vector,
            timestamps=timestamps,
            metadata=metadata
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
            embedding_function=None)
        self._chromadb_collection._embedding_function = self._embedding_function

    @staticmethod
    def _convert_chromadb_data_to_state(data):
        ids = data['ids']
        texts = data['documents']
        vector = data['embeddings']
        metadata = data['metadatas']
        timestamps = []
        metadata = []
        for m in data['metadatas']:
            timestamps.append(m['timestamp'])
            m.pop('timestamp')
            metadata.append(m)
        state = State(
            ids=ids,
            texts=texts,
            vector=vector,
            timestamps=timestamps,
            metadata=metadata
        )
        return state
    
    def latest(self, max_count:int=10):
        warnings.warn("The 'latest' method is deprecated, use 'get' method instead.", DeprecationWarning)
        return self.get(max_count=max_count)

    def retrieve(self, query_text:str, max_count:int=10, metadata:dict=None):
        warnings.warn("The 'retrieve' method is deprecated, use 'query' method instead.", DeprecationWarning)
        return self.query(query_text=query_text, max_count=max_count, metadata=metadata)
    
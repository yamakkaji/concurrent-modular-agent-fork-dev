import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import os, datetime
import numpy as np
from typing import Optional, Dict, Any
from loguru import logger
import uuid

class StateClient():
    def __init__(self, agent_name, module_name:str=None):
        self.chromadb_client = chromadb.HttpClient(host='localhost', port=8000)
        self._setup_chromadb_collection(agent_name)
        
    def _setup_chromadb_collection(self, collection_name):
        ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv('OPENAI_API_KEY'),
            model_name="text-embedding-ada-002"
        )
        self.chromadb_collection = self.chromadb_client.get_or_create_collection(name=collection_name, embedding_function=ef)
    
    def put(self, state:str):
        self.chromadb_collection.add(
            ids=str(uuid.uuid4()),
            documents=state,
            metadatas={
                # 'datetime': datetime.now().isoformat(),
                'timestamp': datetime.datetime.now().timestamp(),
            }
        )
        cn = self.chromadb_collection.count()
        logger.trace(
            f'New state is added. number of documents in the state is {cn}')
    
    def get(self, max_count:int=10):
        return []

    def clear(self):
        collection_name = self.chromadb_collection.name
        self.chromadb_client.delete_collection(collection_name)
        self._setup_chromadb_collection(collection_name)

    def count(self):
        n = self.chromadb_collection.count()
        return n
    
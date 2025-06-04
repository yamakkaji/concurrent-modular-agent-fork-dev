import os, datetime, uuid
import chromadb
import chromadb.utils.embedding_functions as embedding_functions


def get_all_memory():
    chromadb_client = chromadb.HttpClient(host='localhost', port=8000)
    collections = chromadb_client.list_collections()
    memory_list = []
    for collection in collections:
        if collection.name.startswith('concurrent_modular_agent-state-'):
            name = collection.name.replace(f'{__package__.split('.')[0]}-state-', '')
            memory_list.append(name)
    return memory_list
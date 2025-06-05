import os, datetime, uuid
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from .state import StateClient

def get_all_memory():
    chromadb_client = chromadb.HttpClient(host='localhost', port=8000)
    collections = chromadb_client.list_collections()
    agent_memory_list = []
    for collection in collections:
        memory_name = StateClient._convert_collection_name_2_agent_name(collection.name)
        agent_memory_list.append(memory_name)
    return agent_memory_list

def delete_memory(name):
    chromadb_client = chromadb.HttpClient(host='localhost', port=8000)
    collection_name = StateClient._convert_agent_name_2_collection_name(name)
    try:
        chromadb_client.delete_collection(collection_name)
    except chromadb.errors.NotFoundError:
        raise ValueError(f"Agent memory with the name '{name}' does not exist.")

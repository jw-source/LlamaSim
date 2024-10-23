from mem0 import Memory
import os
from dotenv import load_dotenv

load_dotenv()

config = {
    # "llm": {
    #     "provider": "litellm",
    #     "config": {
    #         "model": "cerebras/llama3.1-70b",
    #         "api_key": os.getenv("CEREBRAS_API_KEY"),
    #         "openai_base_url": 'https://api.cerebras.ai/v1',
    #     }
    # },
        "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o-mini",
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-large",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    },
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "LlamaSim",
            "path": "db",
        }
    },
    "version": "v1.1"
}

def add_memory(m, information, user_id, metadata):
    m.add(information, user_id=user_id, metadata=metadata)
    return 

def search_memory(m, query, user_id):
    related_memories = m.search(query=query, user_id=user_id)
    output = [m['memory'] for m in related_memories['results']]
    output = ' '.join(output)
    return output

def get_all_memories(m):
    all_memories = m.get_all()
    output = [m['memory'] for m in all_memories['results']]
    output = ' '.join(output)
    return output

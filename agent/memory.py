"""
Agent Memory — stores past predictions and analysis context.
"""

import json
import os
from datetime import datetime


class AgentMemory:
    def __init__(self, path: str = "memory_store.json"):
        self.path = path
        self.store_data = {}
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.store_data = json.load(f)

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.store_data, f, indent=2)

    def store(self, key: str, value: dict):
        self.store_data[key] = {
            "value": value,
            "timestamp": datetime.utcnow().isoformat()
        }
        self._save()

    def retrieve(self, key: str):
        return self.store_data.get(key, {}).get("value")

    def all(self):
        return self.store_data

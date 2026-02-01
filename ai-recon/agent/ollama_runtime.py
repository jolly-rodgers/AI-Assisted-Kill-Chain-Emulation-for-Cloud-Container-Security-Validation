import requests
import json
import os

class OllamaRuntime:
    def __init__(self):
        self.url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
        self.model = os.getenv("OLLAMA_MODEL", "llama3")

    def plan(self, goal: str):
        prompt = """
You are an offensive security planner.

Rules:
- Only select techniques appropriate for the confidence level.
- Prefer enumeration before exploitation.
- Never suggest destructive actions.
- Only lab-safe techniques are allowed.

Available techniques:
- docker_api_enumerate (confidence >= 0.8)
- docker_mount_host_ro (confidence >= 0.9, lab only)

Respond in JSON:
{
  "techniques": ["technique_id"]
}
"""
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": goal}
            ],
            "stream": False
        }

        r = requests.post(self.url, json=payload, timeout=30)
        r.raise_for_status()

        return self._safe_json(r.json()["message"]["content"])

    def _safe_json(self, text):
        try:
            return json.loads(text)
        except Exception:
            return {"techniques": []}

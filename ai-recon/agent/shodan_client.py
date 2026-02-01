"""
shodan_client.py

Real Shodan API client.
Used during development for live reconnaissance.
In production, this module can be swapped for an MCP-backed client
without changing the orchestration layer.
"""

import os
from typing import Dict, Any
import shodan


class ShodanMCPClient:
    def __init__(self):
        api_key = os.getenv("SHODAN_API_KEY")
        if not api_key:
            raise RuntimeError("SHODAN_API_KEY environment variable not set")

        self.client = shodan.Shodan(api_key)

    def search(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Execute a Shodan search and return results
        in a Shodan-native structure.
        """

        try:
            results = self.client.search(query, limit=limit)
        except shodan.APIError as e:
            raise RuntimeError(f"Shodan API error: {e}")

        return results
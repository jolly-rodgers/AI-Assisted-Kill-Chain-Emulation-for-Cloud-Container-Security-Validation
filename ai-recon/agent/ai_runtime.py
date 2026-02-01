from typing import List, Dict, Protocol


class AIRuntime(Protocol):
    def plan(self, goal: str) -> Dict:
        """
        Given a high-level goal, return a structured plan.
        Example: what intel source to use, what query to run.
        """
        ...

    def reflect(self, findings: List[Dict]) -> Dict:
        """
        Given normalized recon results, decide next action
        (continue, stop, escalate, etc.)
        """
        ...

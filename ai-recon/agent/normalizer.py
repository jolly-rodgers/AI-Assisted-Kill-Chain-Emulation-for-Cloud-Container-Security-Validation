"""
normalizer.py

Transforms raw Shodan-like host data into normalized,
confidence-scored recon targets.
"""

from datetime import datetime, timezone
from typing import Dict, Any


def normalize_docker_host(host: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a raw Shodan host record representing
    an exposed Docker API.
    """

    ip = host.get("ip_str")
    port = host.get("port")
    org = host.get("org")
    product = host.get("product", "") or ""
    location = host.get("location", {}) or {}

    confidence = 0.0

    # Strong indicator: unauthenticated Docker API port
    if port == 2375:
        confidence += 0.5

    # Banner / product evidence
    if isinstance(product, str) and "docker" in product.lower():
        confidence += 0.3

    # Organizational attribution (reduces scan noise)
    if isinstance(org, str) and org.strip():
        confidence += 0.1

    # Geolocation metadata present
    if location.get("country_code"):
        confidence += 0.1

    # Final safety clamp — confidence must always be a float [0.0, 1.0]
    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        confidence = 0.0

    confidence = round(min(confidence, 1.0), 2)

    return {
        "ip": ip,
        "port": port,
        "service": "docker",
        "exposure": "public",
        "org": org,
        "country": location.get("country_code"),
        "risk_reason": "Unauthenticated Docker API exposed on TCP/2375",
        "confidence": confidence,
        "tags": ["docker", "unauthenticated", "container"],
        "source": "shodan",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
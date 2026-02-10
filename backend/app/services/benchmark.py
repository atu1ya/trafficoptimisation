from __future__ import annotations

from typing import Any
import httpx


def benchmark_google(start: str, end: str, api_key: str | None) -> dict[str, Any]:
    if not api_key:
        return {"available": False, "reason": "GOOGLE_MAPS_API_KEY not configured"}

    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {"origin": start, "destination": end, "key": api_key, "departure_time": "now"}
    try:
        response = httpx.get(url, params=params, timeout=5)
        response.raise_for_status()
        payload = response.json()
        route = payload.get("routes", [{}])[0]
        leg = route.get("legs", [{}])[0]
        return {
            "available": True,
            "duration_s": leg.get("duration", {}).get("value"),
            "distance_m": leg.get("distance", {}).get("value"),
        }
    except Exception as exc:  # noqa: BLE001
        return {"available": False, "reason": f"Google request failed: {exc}"}

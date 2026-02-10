from __future__ import annotations

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "perth-greenwave"
    host: str = "0.0.0.0"
    port: int = 8000
    google_maps_api_key: str | None = None
    osm_bbox_south: float = Field(default=-32.120)
    osm_bbox_north: float = Field(default=-31.920)
    osm_bbox_west: float = Field(default=115.740)
    osm_bbox_east: float = Field(default=116.050)
    network_cache_dir: str = "backend/data/networks"
    default_seed: int = 42
    simulation_steps: int = 180
    websocket_tick_ms: int = 250

    class Config:
        env_file = ".env"
        env_prefix = ""


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

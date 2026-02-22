#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path


def bbox_key(south: float, north: float, west: float, east: float, drivable_only: bool = True) -> str:
    raw = json.dumps({"south": south, "north": north, "west": west, "east": east, "drive": drivable_only}, sort_keys=True)
    return hashlib.sha1(raw.encode()).hexdigest()[:12]


def run() -> None:
    parser = argparse.ArgumentParser(description="Build SUMO network from OSM bbox")
    parser.add_argument("--south", type=float, default=float(os.getenv("OSM_BBOX_SOUTH", "-32.120")))
    parser.add_argument("--north", type=float, default=float(os.getenv("OSM_BBOX_NORTH", "-31.920")))
    parser.add_argument("--west", type=float, default=float(os.getenv("OSM_BBOX_WEST", "115.740")))
    parser.add_argument("--east", type=float, default=float(os.getenv("OSM_BBOX_EAST", "116.050")))
    args = parser.parse_args()

    out_root = Path("backend/data/networks")
    out_root.mkdir(parents=True, exist_ok=True)
    key = bbox_key(args.south, args.north, args.west, args.east)
    out_dir = out_root / key
    out_dir.mkdir(parents=True, exist_ok=True)

    osm_path = out_dir / "network.osm.xml"
    net_path = out_dir / "network.net.xml"
    meta_path = out_dir / "meta.json"

    if net_path.exists():
        print(f"Using cached network: {net_path}")
        return

    query = f"[out:xml][timeout:120];(way['highway']({args.south},{args.west},{args.north},{args.east});>;);out body;"
    import urllib.request
    req = urllib.request.Request("https://overpass-api.de/api/interpreter", data=query.encode(), method="POST")
    with urllib.request.urlopen(req, timeout=180) as response:  # noqa: S310
        osm_path.write_bytes(response.read())

    cmd = [
        "netconvert",
        "--osm-files", str(osm_path),
        "--output-file", str(net_path),
        "--tls.guess", "true",
        "--junctions.join", "true",
        "--remove-edges.isolated", "true",
        "--keep-edges.by-vclass", "passenger,bus,delivery",
    ]
    subprocess.run(cmd, check=True)

    meta_path.write_text(json.dumps({"bbox": vars(args), "key": key, "net": str(net_path)}, indent=2))
    print(f"Built network at {net_path}")


if __name__ == "__main__":
    run()

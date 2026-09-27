#!/bin/bash
set -e

NETWORK="superkart-network"

docker network inspect "$NETWORK" >/dev/null 2>&1 || docker network create "$NETWORK"

BRIDGE=$(docker network inspect "$NETWORK" -f '{{.Id}}' | cut -c1-12)
BRIDGE="br-$BRIDGE"

sudo iptables-legacy -C FORWARD -i "$BRIDGE" -o "$BRIDGE" -j ACCEPT 2>/dev/null || \
sudo iptables-legacy -I FORWARD 1 -i "$BRIDGE" -o "$BRIDGE" -j ACCEPT

docker rm -f superkart-backend superkart-frontend >/dev/null 2>&1 || true

docker run -d --name superkart-backend \
  --network "$NETWORK" \
  -p 5000:5000 \
  superkart-backend:latest

docker run -d --name superkart-frontend \
  --network "$NETWORK" \
  -p 8501:8501 \
  superkart-frontend:latest

echo "SuperKart backend and frontend started."

#!/bin/bash
set -e

echo "[SETUP] Installing CAN tools..."
sudo apt-get update -y
sudo apt-get install -y can-utils

echo "[SETUP] Creating vcan0..."
sudo modprobe vcan || true
sudo ip link add dev vcan0 type vcan || true
sudo ip link set up vcan0 || true

echo "[SETUP] Installing Python dependencies..."
pip install --upgrade pip
pip install python-can

echo "[SETUP] Setup completed. vcan0 is ready."

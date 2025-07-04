#!/bin/bash
echo "Starting NeuroScribe PDF Copilot..."
cd "$(dirname "$0")"
streamlit run app.py --server.port 8501

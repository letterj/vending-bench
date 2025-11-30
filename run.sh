#!/bin/bash
docker build -t vending-grok4fast .
docker run --rm \
  -e XAI_API_KEY=$XAI_API_KEY \
  -v "$(pwd)/results:/app/results" \
  vending-grok4fast
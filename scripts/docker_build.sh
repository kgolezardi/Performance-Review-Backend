#!/bin/bash
VERSION=$(python -c "import toml; print(toml.load('review/pyproject.toml')['tool']['poetry']['version'])")
docker build \
  -t "kgolezardi/performance-review-api:latest" \
  -t "kgolezardi/performance-review-api:$VERSION" \
  -f review/api.Dockerfile \
  review

docker build \
  -t "kgolezardi/performance-review-statics:latest" \
  -t "kgolezardi/performance-review-statics:$VERSION" \
  -f review/statics.Dockerfile \
  review

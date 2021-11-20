#!/bin/bash
bash scripts/docker_build_dev.sh
echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
docker push kgolezardi/performance-review-api:dev
docker push kgolezardi/performance-review-api:dev-$TRAVIS_COMMIT
docker push kgolezardi/performance-review-api:dev-$TRAVIS_BUILD_NUMBER
docker push kgolezardi/performance-review-statics:dev
docker push kgolezardi/performance-review-statics:dev-$TRAVIS_COMMIT
docker push kgolezardi/performance-review-statics:dev-$TRAVIS_BUILD_NUMBER

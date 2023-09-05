#!/bin/bash -eu

rm -rf events-generator
mkdir events-generator
cp -r ../lib ../generate.py events-generator/
tar -zcf tarball.tgz events-generator
rm -rf events-generator
trap "rm -f tarball.tgz" EXIT

if which docker >/dev/null 2>&1; then
  DOCKER=docker
elif which podman >/dev/null 2>&1; then
  DOCKER=podman
else
  echo "ERROR: either docker or podman must be installed!"
  exit 1
fi

$DOCKER build \
  -t viyadb/events-generator:latest \
  -t viyadb/events-generator:$(cat ../VERSION) \
  .


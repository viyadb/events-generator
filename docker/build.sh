#!/bin/bash -eu

rm -rf events-generator
mkdir events-generator
cp -r ../lib ../generate.py events-generator/
tar -zcf tarball.tgz events-generator
rm -rf events-generator
trap "rm -f tarball.tgz" EXIT

docker build \
  -t viyadb/events-generator:latest \
  -t viyadb/events-generator:$(cat ../VERSION) \
  .


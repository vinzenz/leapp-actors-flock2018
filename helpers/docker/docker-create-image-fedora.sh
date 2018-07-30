#!/bin/bash

date > marker
docker build -f Dockerfile.fedora -t leapp-initrd-fedora-build:latest .


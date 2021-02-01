#!/usr/bin/bash

rm -rf ./output
mkdir ./output

singularity exec \
    --bind ./output:/mnt \
    --bind ./build.sh:/tmp/build.sh \
    ./intermediate.sif \
    /tmp/build.sh

ls ./output

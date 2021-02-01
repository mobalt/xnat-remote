#!/usr/bin/bash

rm -rf ./output
mkdir ./output

singularity exec \
    --bind ./output:/usr/local/ \
    --bind ./build.sh:/tmp/build.sh \
    ./intermediate.sif \
    /tmp/build.sh

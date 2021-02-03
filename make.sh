#!/usr/bin/bash
echo 'Building the "Intermediate" container.'
sudo singularity build intermediate.sif intermediate.def



echo 'Using the "Intermediate" container to build alpine-compatible singularity.'
rm -rf ./output
mkdir ./output

singularity exec \
    --bind ./output:/usr/local/ \
    --bind ./build-singularity.sh:/tmp/build-singularity.sh \
    ./intermediate.sif \
    /tmp/build-singularity.sh



echo 'Building the "Final" container.'
sudo singularity build final.sif final.def

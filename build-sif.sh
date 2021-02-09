#!/usr/bin/bash
echo 'Building the "Intermediate" container.'
sudo singularity build container/intermediate.sif container/intermediate.def



echo 'Using the "Intermediate" container to build alpine-compatible singularity.'
rm -rf ./container/output
mkdir ./container/output

singularity exec \
    --bind ./container/output:/usr/local/ \
    --bind ./container/build-singularity.sh:/tmp/build-singularity.sh \
    ./container/intermediate.sif \
    /tmp/build-singularity.sh



echo 'Building the "Final" container.'
sudo singularity build xnat-remote.sif container/final.def

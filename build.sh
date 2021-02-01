#!/bin/bash

pushd /tmp/
git clone https://github.com/sylabs/singularity.git
pushd /tmp/singularity
git checkout v3.7.1
./mconfig --without-suid
pushd /tmp/singularity/builddir
make
make install

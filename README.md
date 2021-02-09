# XNAT Remote
This repo builds the singularity container used in the HPC remote for the XNAT
Container Service Plugin. It is capable of converting docker containers into
singularity containers.

## Usage
You need to have a working installation of singularity already. Then, clone this
repo and run `./build-sif.sh`.

The final generated singularity image is `xnat-remote.sif`.


To test it out, try converting a docker alpine image into singularity:
```bash
singularity exec ./xnat-remote.sif \
    singularity build ./test.sif "docker://alpine"
```

Please notice that the first call to singularity is running on the host, while
the entire second line is being run inside `./xnat-remote.sif`.

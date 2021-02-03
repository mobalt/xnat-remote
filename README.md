# Singularity Container Builder
This is a recipe for building a singularity container that contains
singularity and all it's dependencies. It is capable of producing other
singularity containers.

## Usage
You need to have a working installation of singularity already. Then, clone this
repo and run `./make.sh`.

The final generated singularity image is `final.sif`.


To test it out, try converting a docker alpine image into singularity:
```bash
singularity exec ./final.sif \
    singularity build ./test.sif "docker://alpine"
```

Please notice that the first call to singularity is running on the host, while
the entire second line is being run inside `./final.sif`.

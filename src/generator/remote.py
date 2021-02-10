#!/usr/bin/env python

import os
import argparse
import re
from jinja2 import Environment, BaseLoader


def process_image(docker_image):
    namespace, image, version = re.search("(.+)/(.+):(.+)", docker_image).groups()
    docker_image = f"docker://{namespace}/{image}"
    sif_image = f"~/{namespace}_{image}_{version}.sif"
    return docker_image, sif_image


def parse_arguments(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--gpu", type=int, default=0)
    parser.add_argument("--nodes", type=int, default=1)
    parser.add_argument("--name", type=str, help="The job name")
    parser.add_argument(
        "--walltime", type=int, help="The time limit (in hours) for runtime."
    )
    parser.add_argument(
        "--mem", type=int, default=4, help="The GB of memory to allocate."
    )
    parser.add_argument("--stdout", type=str, help="The location of the stdout file.")
    parser.add_argument("--stderr", type=str, help="The location of the stderr file.")
    parser.add_argument(
        "--additional-params",
        type=str,
        help="Misc additional params to append to queue request.",
    )
    parser.add_argument(
        "--docker-image",
        type=str,
        help="The Image from DockerHub to use.",
    )
    parser.add_argument(
        "--cmd",
        type=str,
        help="The command to run within the image",
    )
    parser.add_argument(
        "--bind",
        "-b",
        type=str,
        action="append",
        help="The volumes to bind",
    )
    parsed_args = parser.parse_args(args)
    image = parsed_args["docker-image"]
    docker_image, sif_image = process_image(image)
    return dict(
        docker_image=docker_image,
        sif_image=sif_image,
        cmd=parsed_args.cmd,
        binds=parsed_args.bind,
        gpu=parsed_args.gpu,
        nodes=parsed_args.nodes,
        name=parsed_args.name,
        walltime=parsed_args.walltime,
        mem=parsed_args.mem,
        stdout=parsed_args.stdout,
        stderr=parsed_args.stderr,
        additional_params=parsed_args["additional-params"],
    )


conversion_template = """
module load singularity

if [ ! -f {{ sif_image }} ]; then
    singularity build {{sif_image}} {{docker_image}}
fi
"""


singularity_template = """
singularity exec \\
{%- for item in binds %}
    --bind {{ item }} \\
{%- endfor %}
    {{ sif_image }} \\
    {{ cmd }}
"""


slurm_header = """#!/bin/bash
#SBATCH --job-name="{{ name }}"
#SBATCH --nodes=1 --ntasks-per-node=1
{% if gpu %}
#SBATCH --partition=gpu --gres=gpu:{{ gpu|int }}
{% endif -%}
#SBATCH --time={{ walltime|int }}:00:00 --mem={{ mem|int }}000
#SBATCH --output="{{ stdout }}"
#SBATCH --error="{{ stderr }}"
"""


torque_header = """#PBS -S /bin/bash
#PBS -l nodes=1:ppn=1

{%- if additional_params -%}
:{{ additional_params }}
{%- endif -%}

{%- if gpu -%}
:gpus={{ gpu|int }}
{%- endif -%}

,walltime={{ walltime|int }}:00:00,mem={{ mem|int }}gb
#PBS -o {{ stdout }}
#PBS -e {{ stderr }}
"""

torque = f"""{torque_header}
{conversion_template}
{singularity_template}
"""
slurm = f"""{slurm_header}
{conversion_template}
{singularity_template}
"""


def main():
    params = parse_arguments()
    env = Environment(loader=BaseLoader)
    template = env.from_string(slurm)
    output_script = template.render(**params)

    filename = os.path.join(os.path.expanduser("~"), "output.sh")
    with open(filename, "w") as fd:
        fd.write(output_script)
    os.chmod(filename, 0o700)

if __name__ == "__main__":
    main()

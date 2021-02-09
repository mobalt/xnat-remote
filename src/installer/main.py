#!/usr/bin/env python
import os
from jinja2 import Template, StrictUndefined


key_dir = "./keys"
key_name = "id_rsa"
xnat_remote_sif_url = (
    "https://github.com/mobalt/xnat-remote/releases/download/v0.1/xnat-remote.sif"
)

private_filename = os.path.join(key_dir, key_name)
public_filename = f"{private_filename}.pub"


def generate_keys():
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.backends import default_backend

    key = rsa.generate_private_key(
        backend=default_backend(), public_exponent=65537, key_size=2048
    )
    private_key = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption(),
    )
    public_key = key.public_key().public_bytes(
        serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH
    )
    return private_key, public_key


def write_new_keys():
    os.makedirs(key_dir, exist_ok=True)
    private_key, public_key = generate_keys()

    with open(public_filename, "wb") as fd:
        fd.write(public_key)
    with open(private_filename, "wb") as fd:
        fd.write(private_key)
    os.chmod(private_filename, 0o600)

    return private_key.decode(), public_key.decode()


def read_existing_keys():
    with open(public_filename, "r") as fd:
        public_key = fd.read()
    with open(private_filename, "r") as fd:
        private_key = fd.read()

    return private_key, public_key


def keys_exist():
    return os.path.exists(private_filename) and os.path.exists(public_filename)


def print_instructions():
    print(
        """
    Step 1. Copy `install.sh` over to HPC of choice.
    scp install.sh hpc_user@slurm.local:~/

    Step 2. Run `install.sh`
    ssh hpc_user@slurm.local 'bash ~/install.sh'

    Step 3. Use locked-down key
    ssh -i keys/id_rsa hpc_user@slurm.local -- "args"
    """
    )


def main():
    private_key, public_key = read_existing_keys() if keys_exist() else write_new_keys()

    with open("./templates/install.sh", "r") as fd:
        content = fd.read()
        template = Template(content, undefined=StrictUndefined)

    output = template.render(
        XNAT_REMOTE_SIF_URL=xnat_remote_sif_url,
        KEY=public_key,
    )

    with open("install.sh", "w") as fd:
        fd.write(output)

    print_instructions()


if __name__ == "__main__":
    main()

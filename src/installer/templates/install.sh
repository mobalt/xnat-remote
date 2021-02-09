#!/bin/bash

dir_exists(){
    if [ ! -d $1 ]; then
        mkdir $1
        chmod 700 $1
    fi
}


# Step 1.
# Download the xnat-remote singularity container
# It converts docker images to singularity and also provides a python environment.
dir_exists ~/containers
[ ! -f ~/containers/xnat-remote.sif ] && wget -O ~/containers/xnat-remote.sif {{ XNAT_REMOTE_SIF_URL }}


# Step 2.
# Install the bash command (xnat-remote),
# which routes ssh xnat requests to the xnat-remote.sif
dir_exists ~/bin
cat << 'REMOTE_CODE' > ~/bin/xnat-remote
#!/bin/bash
#module load singularity-3.5.2

singularity exec \
        ~/containers/xnat-remote.sif \
        python ~/remote.py $@

# if generate output.sh, run it
if [ -f ~/output.sh ]; then
    bash ~/output.sh
fi
REMOTE_CODE
# make executable
chmod 700 ~/bin/xnat-remote


# Step 3.
# Append generated ssh public-key to `authorized_keys`
# with locked-down capabilities of what the key can do.
dir_exists ~/.ssh
if [ ! -f ~/.ssh/authorized_keys ]; then
    touch ~/.ssh/authorized_keys
    chmod 644 ~/.ssh/authorized_keys
fi

echo 'command="~/bin/xnat-remote $SSH_ORIGINAL_COMMAND",no-port-forwarding,no-x11-forwarding,no-agent-forwarding {{ KEY }} Automatically added for xnat-remote.' \
    >> ~/.ssh/authorized_keys


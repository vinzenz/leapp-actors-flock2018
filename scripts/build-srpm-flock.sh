#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$( dirname $SCRIPT_DIR )"
BUILD_DIR="$( mktemp -d )"
pushd $ROOT_DIR

echo "=============================================================================="
echo "                PREPARING LEAPP ACTORS INTERNAL REPOSITORY                    "
echo "=============================================================================="

command -v which > /dev/null || dnf -y install which

if [ -z "$(which git)" ]; then
    dnf -y install git-core
fi

if ! git status 2>&1 > /dev/null; then
    rm -rf leapp
    git clone https://github.com/leapp-to/leapp-actors-internal.git
    POPD=`pushd leapp`
fi

# Having this exported will affect the naming of the leapp-repository SRPM and extends it for the number of patches
# This should help to have a continous upgrade path between the builds since upstream and downstream are split
export LEAPP_PATCHES_SINCE_RELEASE_EXTERNAL=".$(git log `git describe  --abbrev=0`..HEAD --format=oneline | wc -l)"
echo "Patches since last release $LEAPP_PATCHES_SINCE_RELEASE_EXTERNAL"

#echo "=============================================================================="
#echo "                        RUNNING INITRD BUILD                                  "
#echo "=============================================================================="

#if [[ $LEAPP_INITRD_SKIP != 1 ]]; then
#    helpers/docker/docker-build.sh
#else
#    echo SKIPPED BUILD of INITRD image
#fi

#mkdir -p repos-internal/offline-upgrade/files
#tar xf sources/dracut/upgrade-boot-files.tgz -C repos-internal/offline-upgrade/files/

echo "=============================================================================="
echo "                    GETTING UPSTREAM ACTORS REPOSITORY                        "
echo "=============================================================================="
git clone https://github.com/leapp-to/leapp-actors.git $BUILD_DIR/leapp-actors
cp -a repos-internal/offline-upgrade $BUILD_DIR/leapp-actors/repos/offline-upgrade
pushd $BUILD_DIR/leapp-actors

git config --global user.email leapp-ci-builder@leapp-to.github.io
git config --global user.name "Leapp CI Builder"
git add repos/offline-upgrade
git commit -m 'Added offline-upgrade repo'

echo "=============================================================================="
echo "                           STARTING SRPM BUILD                                "
echo "=============================================================================="

make -f .copr/Makefile srpm

export SRPM_PATH="$(realpath $(find . -name "leapp-repository-*.src.rpm"))"

echo "=============================================================================="
echo "                           FINISHED SRPM BUILD                                "
echo "=============================================================================="

echo SRPM_PATH=$SRPM_PATH

# Leaving temp/leapp-actors
popd

git clone https://github.com/leapp-to/leapp $BUILD_DIR/leapp
pushd $BUILD_DIR/leapp

make -f .copr/Makefile srpm
export SRPM_LEAPP_PATH="$(realpath $(find . -name "leapp-*.src.rpm"))"

# Leaving temp/leapp
popd

# Back in the leapp-actors-internal repo submit SRPMs for builds

scripts/publish-flock2018.sh $SRPM_PATH $SRPM_LEAPP_PATH

rm -rf $BUILD_DIR
popd

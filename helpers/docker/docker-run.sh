#!/bin/bash

if [[ -z "$BASEDIR" ]]; then
    export BASEDIR=/payload
fi

dnf update -y
cd $BASEDIR/sources/dracut
source dracut-helpers
dracutbuild

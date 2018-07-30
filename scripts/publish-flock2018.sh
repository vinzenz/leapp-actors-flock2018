#!/bin/bash

copr-cli build -r fedora-28-x86_64 evilissimo/leapp-flock2018 $@
RESULT=$?

exit $RESULT

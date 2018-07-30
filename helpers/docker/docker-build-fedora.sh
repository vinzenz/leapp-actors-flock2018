if [[ -z "$SHARED_PATH" ]]; then
    export SHARED_PATH=$PWD
fi
CONTAINER_IMAGE=leapp-initrd-fedora-build:latest
docker run -i --rm -v ${SHARED_PATH}:/payload:Z $CONTAINER_IMAGE /payload/helpers/docker/docker-run.sh

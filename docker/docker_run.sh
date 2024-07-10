#!/bin/bash

# prepare /datasets, /pretrained_models and /output folders as explained in the main README.md
xhost +
docker run \
--gpus all \
-it \
--shm-size=8gb --env="DISPLAY" \
--volume="/home/hoenig/BOP/GDRNet:/gdrn" \
--volume="/ssd3/datasets_bop:/gdrn/datasets/BOP_DATASETS" \
--volume="/tmp/.X11-unix:/tmp/.X11-unix" \
--name=gdrnv0 gdrn_base
#!/bin/bash

# prepare /datasets, /pretrained_models and /output folders as explained in the main README.md
docker run \
--gpus all \
-it \
--shm-size=8gb --env="DISPLAY" \
--volume="/home/hoenig/BOP/ZebraPose:/zebra" \
--name=zebrav0 zebra
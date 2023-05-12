#!/bin/bash

# Loop over each number from 0 to 49
for (( i=0; i<50; i++ ))
do
    # Construct the folder name using the current number
    folder=$(printf "%06d" "$i")
    # Replace the "ape" string with the current folder name in the command
    command="scp -r datasets/BOP_DATASETS/lmo_50k_mix/train_pbr/${folder} peter@192.168.141.41:/home/peter/GDRNet/datasets/BOP_DATASETS/lmo_50k_mix/train_pbr/${folder}"
    # Execute the command
    eval "$command"
done

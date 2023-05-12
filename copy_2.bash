#!/bin/bash

# Loop over each folder in the datasets/BOP_DATASETS/lmo_50k_mix directory
for folder in datasets/BOP_DATASETS/lmo_50k_mix/*
do
    # Check if the current folder name is "train_pbr"
    if [ "${folder##*/}" != "train_pbr" ]
    then
        # If not, copy the entire contents of the folder to the remote server
        command="scp -r ${folder}* peter@192.168.141.41:/home/peter/GDRNet/$folder"
        eval "$command"
    fi
done

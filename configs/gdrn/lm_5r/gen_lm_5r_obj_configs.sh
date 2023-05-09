#!/bin/bash

# List of object names
objects=("ape" "benchvise" "camera" "can" "cat" "driller" "duck" "eggbox" "glue" "holepuncher" "iron" "lamp" "phone")

for object in "${objects[@]}"
do
  # Create filename for modified script
  filename="a6_cPnP_lm_5r_${object}.py"
  
  # Replace "ape" with object name and save modified script
  sed "s/OBJ/$object/g" _a6_cPnP_lm_5r_single_obj_conf.py > "$filename"
done

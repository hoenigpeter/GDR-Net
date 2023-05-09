#!/bin/bash

# List of object names
objects=("ape" "can" "cat" "driller" "duck" "eggbox" "glue" "holepuncher")

for object in "${objects[@]}"
do
  # Create filename for modified script
  filename="a6_cPnP_lmo_${object}.py"
  
  # Replace "ape" with object name and save modified script
  sed "s/OBJ/$object/g" _a6_cPnP_lmo_single_obj_conf.py > "$filename"
done

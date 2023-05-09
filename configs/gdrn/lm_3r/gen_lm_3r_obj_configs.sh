#!/bin/bash

# List of object names
objects=("ape" "benchvise" "camera" "can" "cat" "driller" "duck" "eggbox" "glue" "holepuncher" "iron" "lamp" "phone")

# for object in "${objects[@]}"
# do
#   # Create filename for modified script
#   filename="a6_cPnP_lm_3r_${object}.py"
  
#   # Replace "ape" with object name and save modified script
#   sed "s/OBJ/$object/g" _a6_cPnP_lm_3r_single_obj_conf.py > "$filename"
# done

#!/bin/bash

# Set the path to the directory containing this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd/configs/gdrn/ )"

# Loop through the object names and modify the config file
for object in "${objects[@]}"
do
  # Set the input and output file paths
  INPUT_FILE="$SCRIPT_DIR/_a6_cPnP_lm_3r_single_obj_conf.py"
  OUTPUT_FILE="$SCRIPT_DIR/a6_cPnP_lm_3r_${object}.py"

  # Replace "ape" with the current object name in the input file and save to the output file
  sed "s/OBJ/${object}/g" "$INPUT_FILE" > "$OUTPUT_FILE"
done
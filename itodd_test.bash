#!/bin/bash

# Declare an empty array
itodd_objects=()

# Populate the array with numbers from 1 to 30
for ((i=1; i<=28; i++)); do
    itodd_objects+=($i)
done

# Print the elements of the array
for itodd_object in "${itodd_objects[@]}"; do
    echo "$itodd_object"
done

itodd_variants=("itodd" "itodd_random_texture")
itodd_minus_variants=("itodd" "itodd-random-texture")

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Generate the single obj config files
for variant in "${itodd_variants[@]}"
do
    # Loop through the object names and modify the config file
    for itodd_object in "${itodd_objects[@]}"
    do
        # Set the input and output file paths
        INPUT_FILE="$SCRIPT_DIR/configs/gdrn/_a6_cPnP_itodd_single_obj_conf.py"
        OUTPUT_FILE="$SCRIPT_DIR/configs/gdrn/${variant[@]}/a6_cPnP_${variant[@]}_${itodd_object}.py"

        # Replace "ape" with the current object name in the input file and save to the output file
        sed -e "s/OBJ/${itodd_object}/g" -e "s/VAR/${variant}/g" "$INPUT_FILE" > "$OUTPUT_FILE"
    done
done

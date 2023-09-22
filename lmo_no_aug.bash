#!/bin/bash

lmo_objects=("ape" "can" "cat" "driller" "duck" "eggbox" "glue" "holepuncher")

lmo_variants=("lmo" "lmo_random_texture_all")
lmo_minus_variants=("lmo" "lmo-random-texture-all")

# lmo_objects=("ape" "can" "cat" "driller" "duck" "eggbox" "glue" "holepuncher")

# lmo_variants=("lmo" "lmo_3r" "lmo_5r" "lmo_7r" "lmo_random_texture_all" "lmo_50k_mix")
# lmo_minus_variants=("lmo" "lmo-3r" "lmo-5r" "lmo-7r" "lmo-random-texture-all" "lmo-50k-mix")

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# echo "Removing cache!"
# command="rm -r .cache"
# eval "$command"

# Generate the single obj config files
for lmo_variant in "${lmo_variants[@]}"
do
    # Loop through the object names and modify the config file
    for lmo_object in "${lmo_objects[@]}"
    do
        # Set the input and output file paths
        INPUT_FILE="$SCRIPT_DIR/configs/gdrn/_a6_cPnP_lmo_single_obj_no_aug_conf.py"
        OUTPUT_FILE="$SCRIPT_DIR/configs/gdrn/${lmo_variant[@]}_no_aug/a6_cPnP_${lmo_variant[@]}_no_aug_${lmo_object}.py"

        # Replace "ape" with the current object name in the input file and save to the output file
        sed -e "s/OBJ/${lmo_object}/g" -e "s/VAR/${lmo_variant}/g" "$INPUT_FILE" > "$OUTPUT_FILE"
    done
done

# Generate the config file for testing 1 per obj LMO / shared LMO
for lmo_variant in "${lmo_variants[@]}"
do
    # Set the input and output file paths
    INPUT_FILE="$SCRIPT_DIR/configs/gdrn/_a6_cPnP_lmo_1_per_obj_no_aug_conf.py"
    OUTPUT_FILE="$SCRIPT_DIR/configs/gdrn/${lmo_variant[@]}_no_aug/a6_cPnP_${lmo_variant[@]}_1_per_obj_no_aug.py"

    # Replace "VAR" with the current object name in the input file and save to the output file
    sed -e "s/VAR/${lmo_variant}/g" "$INPUT_FILE" > "$OUTPUT_FILE"
done

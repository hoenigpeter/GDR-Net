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

# itodd_variants=("itodd" "itodd_random_texture")
# itodd_minus_variants=("itodd" "itodd-random-texture")

itodd_variants=("itodd_random_texture")
itodd_minus_variants=("itodd-random-texture")

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

#test object models itodd
for itodd_variant in "${itodd_variants[@]}"
do
    for itodd_object in "${itodd_objects[@]}"
    do
    # Replace the "ape" string with the current model string in the command
    command="./core/gdrn_modeling/test_gdrn.sh configs/gdrn/${itodd_variant[@]}/a6_cPnP_${itodd_variant[@]}_${itodd_object}.py 0 output/gdrn/40_epochs/${itodd_variant[@]}_SO/${itodd_object}/model_final.pth"
    
    # Execute the command
    eval "$command"
    done
done

for i in "${!itodd_variants[@]}"
do
    itodd_variant="${itodd_variants[i]}"
    itodd_minus_variant="${itodd_minus_variants[i]}"
    
    # Set the directory path
    DIR="./output/gdrn/40_epochs/${itodd_variant[@]}_SO/_all/csv_files"

    # Check if the directory exists
    if [ ! -d "$DIR" ]
    then
        # Create the directory if it does not exist
        mkdir -p "$DIR"
    fi

    for itodd_object in "${itodd_objects[@]}"
    do
    # Replace the "ape" string with the current model string in the command
    command="cp ./output/gdrn/40_epochs/${itodd_variant[@]}_SO/${itodd_object}/inference_model_final/itodd_${itodd_object}_bop_test/a6-cPnP-${itodd_minus_variant[@]}-${itodd_object}-test-iter0_itodd-test.csv ./output/gdrn/40_epochs/${itodd_variant[@]}_SO/_all/csv_files/a6-cPnP-${itodd_minus_variant[@]}-${itodd_object}-test-iter0_itodd-test.csv"

    # Execute the command
    eval "$command"
    done
done

# #Generate the config file for testing combined LM csv
# for itodd_variant in "${itodd_variants[@]}"
# do
#     # Set the input and output file paths
#     INPUT_FILE="$SCRIPT_DIR/configs/gdrn/_a6_cPnP_itodd_1_per_obj_conf.py"
#     OUTPUT_FILE="$SCRIPT_DIR/configs/gdrn/${itodd_variant[@]}/a6_cPnP_${itodd_variant[@]}_1_per_obj.py"

#     # Replace "ape" with the current object name in the input file and save to the output file
#     sed -e "s/VAR/${itodd_variant}/g" "$INPUT_FILE" > "$OUTPUT_FILE"
# done

# # # Generate the config file for testing combined LM csv
 for i in "${!itodd_variants[@]}"
 do
    itodd_variant="${itodd_variants[i]}"
    itodd_minus_variant="${itodd_minus_variants[i]}"

    command="cp ./output/gdrn/40_epochs/concat_csv_result_files.py ./output/gdrn/40_epochs/${itodd_variant[@]}_SO/_all/concat_csv_result_files.py"
    eval "$command"
    command="python ./output/gdrn/40_epochs/${itodd_variant[@]}_SO/_all/concat_csv_result_files.py"
    eval "$command"

    # Set the directory path
    DIR="./output/gdrn/40_epochs/${itodd_variant[@]}/_all/inference_dummy/itodd_bop_test"

    # Check if the directory exists
    if [ ! -d "$DIR" ]
    then
        # Create the directory if it does not exist
        mkdir -p "$DIR"
    fi

    command="cp ./output/gdrn/40_epochs/${itodd_variant[@]}_SO/_all/csv_files/concatenated_result_files.csv ./output/gdrn/40_epochs/${itodd_variant[@]}_SO/_all/inference_dummy/itodd_bop_test/a6-cPnP-${itodd_minus_variant[@]}-1-per-obj-iter0_itodd-test.csv"
    eval "$command"
    command="cp -R -u -p ./output/gdrn/40_epochs/dummy.pth ./output/gdrn/40_epochs/${itodd_variant[@]}_SO/_all/dummy.pth"
    eval "$command"

done





#!/bin/bash

# Declare an empty array
tless_objects=()

# Populate the array with numbers from 1 to 30
for ((i=1; i<=30; i++)); do
    tless_objects+=($i)
done

# Print the elements of the array
for tless_object in "${tless_objects[@]}"; do
    echo "$tless_object"
done

# tless_variants=("tless" "tless_random_texture")
# tless_minus_variants=("tless" "tless-random-texture")

tless_variants=("tless")
tless_minus_variants=("tless")

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

Generate the single obj config files
for variant in "${tless_variants[@]}"
do
    # Loop through the object names and modify the config file
    for tless_object in "${tless_objects[@]}"
    do
        # Set the input and output file paths
        INPUT_FILE="$SCRIPT_DIR/configs/gdrn/_a6_cPnP_tless_single_obj_conf.py"
        OUTPUT_FILE="$SCRIPT_DIR/configs/gdrn/${variant[@]}/a6_cPnP_${variant[@]}_${tless_object}.py"

        # Replace "ape" with the current object name in the input file and save to the output file
        sed -e "s/OBJ/${tless_object}/g" -e "s/VAR/${variant}/g" "$INPUT_FILE" > "$OUTPUT_FILE"
    done
done

# # Generate the config file for testing combined LM csv
for variant in "${tless_variants[@]}"
do
    # Set the input and output file paths
        INPUT_FILE="$SCRIPT_DIR/configs/gdrn/_a6_cPnP_tless_1_per_obj_conf.py"
        OUTPUT_FILE="$SCRIPT_DIR/configs/gdrn/${variant[@]}/a6_cPnP_${variant[@]}_1_per_obj.py"

        # Replace "ape" with the current object name in the input file and save to the output file
        sed -e "s/VAR/${variant}/g" "$INPUT_FILE" > "$OUTPUT_FILE"
done

for variant in "${tless_variants[@]}"
do
    for tless_object in "${tless_objects[@]}"
    do
    # Replace the "ape" string with the current model string in the command
    command="./core/gdrn_modeling/test_gdrn.sh configs/gdrn/${variant[@]}/a6_cPnP_${variant[@]}_${tless_object}.py 0 output/gdrn/40_epochs/${variant[@]}_SO/${tless_object}/model_final.pth"
    
    # Execute the command
    eval "$command"
    done
done

for i in "${!tless_variants[@]}"
do
    tless_variant="${tless_variants[i]}"
    tless_minus_variant="${tless_minus_variants[i]}"
    
    # Set the directory path
    DIR="./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/csv_files"

    # Check if the directory exists
    if [ ! -d "$DIR" ]
    then
        # Create the directory if it does not exist
        mkdir -p "$DIR"
    fi

    for tless_object in "${tless_objects[@]}"
    do
    # Replace the "ape" string with the current model string in the command
    command="cp ./output/gdrn/40_epochs/${tless_variant[@]}_SO/${tless_object}/inference_model_final/tless_${tless_object}_bop_test_primesense/a6-cPnP-${tless_minus_variant[@]}-${tless_object}-test-iter0_tless-test.csv ./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/csv_files/a6-cPnP-${tless_minus_variant[@]}-${tless_object}-test-iter0_tless-test.csv"

    # Execute the command
    eval "$command"
    done
done

# Generate the config file for testing combined LM csv
for variant in "${tless_variants[@]}"
do
    # Set the input and output file paths
    INPUT_FILE="$SCRIPT_DIR/configs/gdrn/_a6_cPnP_tless_1_per_obj_conf.py"
    OUTPUT_FILE="$SCRIPT_DIR/configs/gdrn/${variant[@]}/a6_cPnP_${variant[@]}_1_per_obj.py"

    # Replace "ape" with the current object name in the input file and save to the output file
    sed -e "s/VAR/${variant}/g" "$INPUT_FILE" > "$OUTPUT_FILE"
done

# # Generate the config file for testing combined LM csv
 for i in "${!tless_variants[@]}"
 do
    tless_variant="${tless_variants[i]}"
    tless_minus_variant="${tless_minus_variants[i]}"

    command="cp ./output/gdrn/40_epochs/concat_csv_result_files.py ./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/concat_csv_result_files.py"
    eval "$command"
    command="python ./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/concat_csv_result_files.py"
    eval "$command"

    # Set the directory path
    DIR="./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/inference_dummy/tless_bop_test_primesense"

    # Check if the directory exists
    if [ ! -d "$DIR" ]
    then
        # Create the directory if it does not exist
        mkdir -p "$DIR"
    fi

    command="cp ./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/csv_files/concatenated_result_files.csv ./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/inference_dummy/tless_bop_test_primesense/a6-cPnP-${tless_minus_variant[@]}-1-per-obj-iter0_tless-test.csv"
    eval "$command"
    command="cp -R -u -p ./output/gdrn/40_epochs/dummy.pth ./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/dummy.pth"
    eval "$command"

done




#!/bin/bash

lm_objects=("ape" "benchvise" "camera" "can" "cat" "driller" "duck" "eggbox" "glue" "holepuncher" "iron" "lamp" "phone")
lmo_objects=("ape" "can" "cat" "driller" "duck" "eggbox" "glue" "holepuncher")
lm_only_objects=("benchvise" "camera" "iron" "lamp" "phone")

# lm_variants=("lm" "lm_3r" "lm_5r" "lm_7r" "lm_random_texture_all" "lm_50k_mix")
# lmo_variants=("lmo" "lmo_3r" "lmo_5r" "lmo_7r" "lmo_random_texture_all" "lmo_50k_mix")
# lm_minus_variants=("lm" "lm-3r" "lm-5r" "lm-7r" "lm-random-texture-all" "lm-50k-mix")

lm_variants=("lm" "lm_random_texture_all")
lmo_variants=("lmo" "lmo_random_texture_all")
lm_minus_variants=("lm" "lm-random-texture-all")

# Generate the single obj config files
for variant in "${lm_variants[@]}"
do
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

    # Loop through the object names and modify the config file
    for lm_object in "${lm_objects[@]}"
    do
        # Set the input and output file paths
        INPUT_FILE="$SCRIPT_DIR/configs/gdrn/_a6_cPnP_lm_single_obj_conf.py"
        OUTPUT_FILE="$SCRIPT_DIR/configs/gdrn/${variant[@]}/a6_cPnP_${variant[@]}_${lm_object}.py"

        # Replace "ape" with the current object name in the input file and save to the output file
        sed -e "s/OBJ/${lm_object}/g" -e "s/VAR/${variant}/g" "$INPUT_FILE" > "$OUTPUT_FILE"
    done
done

# Generate the config file for testing combined LM csv
for variant in "${lm_variants[@]}"
do
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

    # Set the input and output file paths
        INPUT_FILE="$SCRIPT_DIR/configs/gdrn/_a6_cPnP_lm_1_per_obj_conf.py"
        OUTPUT_FILE="$SCRIPT_DIR/configs/gdrn/${variant[@]}/a6_cPnP_${variant[@]}_1_per_obj.py"

        # Replace "ape" with the current object name in the input file and save to the output file
        sed -e "s/VAR/${variant}/g" "$INPUT_FILE" > "$OUTPUT_FILE"
done

# Generate the config file for testing shared LM
for variant in "${lm_variants[@]}"
do
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

    # Set the input and output file paths
        INPUT_FILE="$SCRIPT_DIR/configs/gdrn/_a6_cPnP_lm_conf.py"
        OUTPUT_FILE="$SCRIPT_DIR/configs/gdrn/${variant[@]}/a6_cPnP_${variant[@]}.py"

        # Replace "ape" with the current object name in the input file and save to the output file
        sed -e "s/VAR/${variant}/g" "$INPUT_FILE" > "$OUTPUT_FILE"
done

for i in "${!lm_variants[@]}"
do
    lm_variant="${lm_variants[i]}"
    lmo_variant="${lmo_variants[i]}"
    
    for lmo_object in "${lmo_objects[@]}"
    do
    # Replace the "ape" string with the current model string in the command
    command="./core/gdrn_modeling/test_gdrn.sh configs/gdrn/${lm_variant[@]}/a6_cPnP_${lm_variant[@]}_${lmo_object}.py 0 output/gdrn/40_epochs/${lmo_variant[@]}_SO/${lmo_object}/model_final.pth"
    
    # Execute the command
    eval "$command"
    done
done

for i in "${!lm_variants[@]}"
do
    lm_variant="${lm_variants[i]}"
    lmo_variant="${lmo_variants[i]}"
    
    for lm_only_object in "${lm_only_objects[@]}"
    do
    # Replace the "ape" string with the current model string in the command
    command="./core/gdrn_modeling/test_gdrn.sh configs/gdrn/${lm_variant[@]}/a6_cPnP_${lm_variant[@]}_${lm_only_object}.py 0 output/gdrn/40_epochs/${lm_variant[@]}_SO/${lm_only_object}/model_final.pth"
    
    # Execute the command
    eval "$command"
    done
done

# 

for i in "${!lm_variants[@]}"
do
    lm_variant="${lm_variants[i]}"
    lm_minus_variant="${lm_minus_variants[i]}"
    
    # Set the directory path
    DIR="./output/gdrn/40_epochs/${lm_variant[@]}_SO/_all/csv_files"

    # Check if the directory exists
    if [ ! -d "$DIR" ]
    then
        # Create the directory if it does not exist
        mkdir -p "$DIR"
    fi

    for lm_object in "${lm_objects[@]}"
    do
    # Replace the "ape" string with the current model string in the command
    command="cp ./output/gdrn/40_epochs/${lm_variant[@]}_SO/${lm_object}/inference_model_final/lm_real_${lm_object}_test/a6-cPnP-${lm_minus_variant[@]}-${lm_object}-test-iter0_lm-test.csv ./output/gdrn/40_epochs/${lm_variant[@]}_SO/_all/csv_files/a6-cPnP-${lm_minus_variant[@]}-${lm_object}-test-iter0_lm-test.csv"

    # Execute the command
    eval "$command"
    done
done

# Generate the config file for testing combined LM csv
for variant in "${lm_variants[@]}"
do
    # Set the input and output file paths
    INPUT_FILE="$SCRIPT_DIR/configs/gdrn/_a6_cPnP_lm_1_per_obj_conf.py"
    OUTPUT_FILE="$SCRIPT_DIR/configs/gdrn/${variant[@]}/a6_cPnP_${variant[@]}_1_per_obj.py"

    # Replace "ape" with the current object name in the input file and save to the output file
    sed -e "s/VAR/${variant}/g" "$INPUT_FILE" > "$OUTPUT_FILE"
done

# Generate the config file for testing combined LM csv
 for i in "${!lm_variants[@]}"
 do
    lm_variant="${lm_variants[i]}"
    lm_minus_variant="${lm_minus_variants[i]}"

    command="cp ./output/gdrn/40_epochs/concat_csv_result_files.py ./output/gdrn/40_epochs/${lm_variant[@]}_SO/_all/concat_csv_result_files.py"
    eval "$command"
    command="python ./output/gdrn/40_epochs/${lm_variant[@]}_SO/_all/concat_csv_result_files.py"
    eval "$command"

    # Set the directory path
    DIR="./output/gdrn/40_epochs/${lm_variant[@]}_SO/_all/inference_dummy/lm_13_test"

    # Check if the directory exists
    if [ ! -d "$DIR" ]
    then
        # Create the directory if it does not exist
        mkdir -p "$DIR"
    fi

    command="cp ./output/gdrn/40_epochs/${lm_variant[@]}_SO/_all/csv_files/concatenated_result_files.csv ./output/gdrn/40_epochs/${lm_variant[@]}_SO/_all/inference_dummy/lm_13_test/a6-cPnP-${lm_minus_variant[@]}-1-per-obj-iter0_lm-test.csv"
    eval "$command"
    command="cp -R -u -p ./output/gdrn/40_epochs/dummy.pth ./output/gdrn/40_epochs/${lm_variant[@]}_SO/_all/dummy.pth"
    eval "$command"

done




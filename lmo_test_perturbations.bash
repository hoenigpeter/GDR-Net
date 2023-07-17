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
# perturbations=("1" "2" "3" "4" "5")
# noise_types=("defocus_blur" "glass_blur" "motion_blur" "brightness" "contrast" "elastic_transform"
# "pixelate" "jpeg_compression" "speckle_noise" "gaussian_blur" "spatter" "saturate")

# perturbations=("1" "2" "3" "4" "5")

# noise_types=("gaussian_noise" "shot_noise" "impulse_noise" "defocus_blur"
# "glass_blur" "motion_blur" "zoom_blur" "snow" "frost" "fog"
# "brightness" "contrast" "elastic_transform" "pixelate" "jpeg_compression"
# "speckle_noise" "gaussian_blur" "spatter" "saturate")

perturbations=("1")

noise_types=("gaussian_noise")

for noise_type in "${noise_types[@]}"
do
    for perturbation in "${perturbations[@]}"
    do
        for lmo_variant in "${lmo_variants[@]}"
        do
            command="mv ./datasets/BOP_DATASETS/lmo/test/${noise_type[@]}/lmo_test_${noise_type[@]}_${perturbation[@]}/000002 ./datasets/BOP_DATASETS/lmo/test/000002"
            eval "$command"
            
        done   
        for lmo_variant in "${lmo_variants[@]}"
        do
            # Loop through the object names and modify the config file
            for lmo_object in "${lmo_objects[@]}"
            do
                # Set the input and output file paths
                INPUT_FILE="$SCRIPT_DIR/configs/gdrn/_a6_cPnP_lmo_single_obj_conf.py"
                OUTPUT_FILE="$SCRIPT_DIR/configs/gdrn/${lmo_variant[@]}/a6_cPnP_${lmo_variant[@]}_${lmo_object}.py"

                # Replace "ape" with the current object name in the input file and save to the output file
                sed -e "s/OBJ/${lmo_object}/g" -e "s/VAR/${lmo_variant}/g" "$INPUT_FILE" > "$OUTPUT_FILE"
            done
        done

        # Generate the config file for testing 1 per obj LMO / shared LMO
        for lmo_variant in "${lmo_variants[@]}"
        do
            # Set the input and output file paths
            INPUT_FILE="$SCRIPT_DIR/configs/gdrn/_a6_cPnP_lmo_1_per_obj_conf.py"
            OUTPUT_FILE="$SCRIPT_DIR/configs/gdrn/${lmo_variant[@]}/a6_cPnP_${lmo_variant[@]}_1_per_obj.py"

            # Replace "VAR" with the current object name in the input file and save to the output file
            sed -e "s/VAR/${lmo_variant}/g" "$INPUT_FILE" > "$OUTPUT_FILE"
        done

        for lmo_variant in "${lmo_variants[@]}"
        do
            # Set the input and output file paths
            INPUT_FILE="$SCRIPT_DIR/configs/gdrn/_a6_cPnP_lmo_conf.py"
            OUTPUT_FILE="$SCRIPT_DIR/configs/gdrn/${lmo_variant[@]}/a6_cPnP_${lmo_variant[@]}.py"

            # Replace "VAR" with the current object name in the input file and save to the output file
            sed -e "s/VAR/${lmo_variant}/g" "$INPUT_FILE" > "$OUTPUT_FILE"
        done

        #test object models LMO
        for lmo_variant in "${lmo_variants[@]}"
        do
            for lmo_object in "${lmo_objects[@]}"
            do
            # Replace the "ape" string with the current model string in the command
            command="./core/gdrn_modeling/test_gdrn.sh configs/gdrn/${lmo_variant[@]}/a6_cPnP_${lmo_variant[@]}_${lmo_object}.py 0 output/gdrn/40_epochs/${lmo_variant[@]}_SO/${lmo_object}/model_final.pth"
            
            # Execute the command
            eval "$command"
            done
        done

        for i in "${!lmo_variants[@]}"
        do
            lmo_variant="${lmo_variants[i]}"
            lmo_minus_variant="${lmo_minus_variants[i]}"
            
            # Set the directory path
            DIR="./output/gdrn/40_epochs/${lmo_variant[@]}_SO/_all/csv_files"

            # Check if the directory exists
            if [ ! -d "$DIR" ]
            then
                # Create the directory if it does not exist
                mkdir -p "$DIR"
            fi

            for lmo_object in "${lmo_objects[@]}"
            do
            # Replace the "ape" string with the current model string in the command
            command="cp ./output/gdrn/40_epochs/${lmo_variant[@]}_SO/${lmo_object}/inference_model_final/lmo_${lmo_object}_bop_test/a6-cPnP-${lmo_minus_variant[@]}-${lmo_object}-test-iter0_lmo-test.csv ./output/gdrn/40_epochs/${lmo_variant[@]}_SO/_all/csv_files/a6-cPnP-${lmo_minus_variant[@]}-${lmo_object}-test-iter0_lmo-test.csv"

            # Execute the command
            eval "$command"
            done
        done

        #Generate the config file for testing combined LM csv
        for lmo_variant in "${lmo_variants[@]}"
        do
            # Set the input and output file paths
            INPUT_FILE="$SCRIPT_DIR/configs/gdrn/_a6_cPnP_lmo_1_per_obj_conf.py"
            OUTPUT_FILE="$SCRIPT_DIR/configs/gdrn/${lmo_variant[@]}/a6_cPnP_${lmo_variant[@]}_1_per_obj.py"

            # Replace "ape" with the current object name in the input file and save to the output file
            sed -e "s/VAR/${lmo_variant}/g" "$INPUT_FILE" > "$OUTPUT_FILE"
        done

        # # # Generate the config file for testing combined LM csv
        for i in "${!lmo_variants[@]}"
        do
            lmo_variant="${lmo_variants[i]}"
            lmo_minus_variant="${lmo_minus_variants[i]}"

            command="cp ./output/gdrn/40_epochs/concat_csv_result_files.py ./output/gdrn/40_epochs/${lmo_variant[@]}_SO/_all/concat_csv_result_files.py"
            eval "$command"
            command="rm ./output/gdrn/40_epochs/${lmo_variant[@]}_SO/_all/csv_files/concatenated_result_files.csv"
            eval "$command"
            command="python ./output/gdrn/40_epochs/${lmo_variant[@]}_SO/_all/concat_csv_result_files.py"
            eval "$command"

            # Set the directory path
            DIR="./output/gdrn/40_epochs/${lmo_variant[@]}_SO/_all/inference_dummy/lmo_bop_test"

            # Check if the directory exists
            if [ ! -d "$DIR" ]
            then
                # Create the directory if it does not exist
                mkdir -p "$DIR"
            fi

            command="cp ./output/gdrn/40_epochs/${lmo_variant[@]}_SO/_all/csv_files/concatenated_result_files.csv ./output/gdrn/40_epochs/${lmo_variant[@]}_SO/_all/inference_dummy/lmo_bop_test/a6-cPnP-${lmo_minus_variant[@]}-1-per-obj-iter0_lmo-test.csv"
            eval "$command"
            command="cp -R -u -p ./output/gdrn/40_epochs/dummy.pth ./output/gdrn/40_epochs/${lmo_variant[@]}_SO/_all/dummy.pth"
            eval "$command"

        done

        for i in "${!lmo_variants[@]}"
        do
            lmo_variant="${lmo_variants[i]}"
            lmo_minus_variant="${lmo_minus_variants[i]}"

            command="./core/gdrn_modeling/test_gdrn.sh configs/gdrn/${lmo_variant[@]}/a6_cPnP_${lmo_variant[@]}_1_per_obj.py 0 output/gdrn/40_epochs/${lmo_variant[@]}_SO/_all/dummy.pth"
            eval "$command"
        done

        # Move test image folder back to its location
        command="mv ./datasets/BOP_DATASETS/lmo/test/000002 ./datasets/BOP_DATASETS/lmo/test/${noise_type[@]}/lmo_test_${noise_type[@]}_${perturbation[@]}/000002"
        eval "$command"

        # copy result files to specific test dataset folder
        for i in "${!lmo_variants[@]}"
        do
            lmo_variant="${lmo_variants[i]}"
            lmo_minus_variant="${lmo_minus_variants[i]}"

            command="mv ./output/gdrn/40_epochs/${lmo_variant[@]}_SO/_all/inference_dummy/lmo_bop_test/a6-cPnP-${lmo_minus_variant[@]}-1-per-obj-iter0_lmo-test.csv  ./datasets/BOP_DATASETS/lmo/test/${noise_type[@]}/lmo_test_${noise_type[@]}_${perturbation[@]}/a6-cPnP-${lmo_minus_variant[@]}-1-per-obj-iter0_lmo-test.csv"
            eval "$command"
            command="mv ./output/gdrn/40_epochs/${lmo_variant[@]}_SO/_all/inference_dummy/lmo_bop_test/a6-cPnP-${lmo_minus_variant[@]}-1-per-obj-iter0_lmo-test_tab_obj_col.txt  ./datasets/BOP_DATASETS/lmo/test/${noise_type[@]}/lmo_test_${noise_type[@]}_${perturbation[@]}/a6-cPnP-${lmo_minus_variant[@]}-1-per-obj-iter0_lmo-test_tab_obj_col.txt"
            eval "$command"
            command="mv ./output/gdrn/40_epochs/${lmo_variant[@]}_SO/_all/inference_dummy/lmo_bop_test/a6-cPnP-${lmo_minus_variant[@]}-1-per-obj-iter0_lmo-test_tab_obj_row.txt  ./datasets/BOP_DATASETS/lmo/test/${noise_type[@]}/lmo_test_${noise_type[@]}_${perturbation[@]}/a6-cPnP-${lmo_minus_variant[@]}-1-per-obj-iter0_lmo-test_tab_obj_row.txt"
            eval "$command"
        done
    done
done




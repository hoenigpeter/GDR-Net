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

tless_variants=("tless" "tless_random_texture")
tless_minus_variants=("tless" "tless-random-texture")

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

#perturbations=("1" "2" "3" "4" "5")
perturbations=("2")
#["gaussian_noise","shot_noise","motion_blur","brightness","gaussian_blur"]
#noise_types=("gaussian_blur")
#noise_types=("gaussian_noise" "shot_noise" "motion_blur" "brightness" "gaussian_blur")
noise_types=("gaussian_noise")

for noise_type in "${noise_types[@]}"
do
    for perturbation in "${perturbations[@]}"
    do
        command="mv ./datasets/BOP_DATASETS/tless/perturbations/${noise_type[@]}/test_primesense_${noise_type[@]}_${perturbation[@]} ./datasets/BOP_DATASETS/tless/test_primesense"
        eval "$command"

        for tless_variant in "${tless_variants[@]}"
        do
            for tless_object in "${tless_objects[@]}"
            do
                INPUT_FILE="$SCRIPT_DIR/configs/gdrn/_a6_cPnP_tless_single_obj_conf.py"
                OUTPUT_FILE="$SCRIPT_DIR/configs/gdrn/${tless_variant[@]}/a6_cPnP_${tless_variant[@]}_${tless_object}.py"
                sed -e "s/OBJ/${tless_object}/g" -e "s/VAR/${tless_variant}/g" "$INPUT_FILE" > "$OUTPUT_FILE"
            done
        done

        for tless_variant in "${tless_variants[@]}"
        do
            INPUT_FILE="$SCRIPT_DIR/configs/gdrn/_a6_cPnP_tless_1_per_obj_conf.py"
            OUTPUT_FILE="$SCRIPT_DIR/configs/gdrn/${tless_variant[@]}/a6_cPnP_${tless_variant[@]}_1_per_obj.py"
            sed -e "s/VAR/${tless_variant}/g" "$INPUT_FILE" > "$OUTPUT_FILE"
        done

        for tless_variant in "${tless_variants[@]}"
        do
            for tless_object in "${tless_objects[@]}"
            do
                command="./core/gdrn_modeling/test_gdrn.sh configs/gdrn/${tless_variant[@]}/a6_cPnP_${tless_variant[@]}_${tless_object}.py 0 output/gdrn/40_epochs/${tless_variant[@]}_SO/${tless_object}/model_final.pth"
                eval "$command"
            done
        done

        for i in "${!tless_variants[@]}"
        do
            tless_variant="${tless_variants[i]}"
            tless_minus_variant="${tless_minus_variants[i]}"
            DIR="./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/csv_files"

            if [ ! -d "$DIR" ]
            then
                mkdir -p "$DIR"
            fi

            for tless_object in "${tless_objects[@]}"
            do
                command="cp ./output/gdrn/40_epochs/${tless_variant[@]}_SO/${tless_object}/inference_model_final/tless_${tless_object}_bop_test_primesense/a6-cPnP-${tless_minus_variant[@]}-${tless_object}-test-iter0_tless-test.csv ./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/csv_files/a6-cPnP-${tless_minus_variant[@]}-${tless_object}-test-iter0_tless-test.csv"
                eval "$command"
            done
        done

        for i in "${!tless_variants[@]}"
        do
            tless_variant="${tless_variants[i]}"
            tless_minus_variant="${tless_minus_variants[i]}"

            command="cp ./output/gdrn/40_epochs/concat_csv_result_files.py ./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/concat_csv_result_files.py"
            eval "$command"
            command="rm ./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/csv_files/concatenated_result_files.csv"
            eval "$command"
            command="python ./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/concat_csv_result_files.py"
            eval "$command"

            DIR="./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/inference_dummy/tless_bop_test_primesense"

            if [ ! -d "$DIR" ]
            then
                mkdir -p "$DIR"
            fi

            command="cp ./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/csv_files/concatenated_result_files.csv ./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/inference_dummy/tless_bop_test_primesense/a6-cPnP-${tless_minus_variant[@]}-1-per-obj-iter0_tless-test.csv"
            eval "$command"
            command="cp -R -u -p ./output/gdrn/40_epochs/dummy.pth ./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/dummy.pth"
            eval "$command"

        done

        for i in "${!tless_variants[@]}"
        do
            tless_variant="${tless_variants[i]}"
            tless_minus_variant="${tless_minus_variants[i]}"

            command="./core/gdrn_modeling/test_gdrn.sh configs/gdrn/${tless_variant[@]}/a6_cPnP_${tless_variant[@]}_1_per_obj.py 0 output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/dummy.pth"
            eval "$command"
        done

        command="mv ./datasets/BOP_DATASETS/tless/test_primesense ./datasets/BOP_DATASETS/tless/perturbations/${noise_type[@]}/test_primesense_${noise_type[@]}_${perturbation[@]}"
        eval "$command"

        for i in "${!tless_variants[@]}"
        do
            tless_variant="${tless_variants[i]}"
            tless_minus_variant="${tless_minus_variants[i]}"

            command="mv ./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/inference_dummy/tless_bop_test_primesense/a6-cPnP-${tless_minus_variant[@]}-1-per-obj-iter0_tless-test.csv  ./datasets/BOP_DATASETS/tless/perturbations/${noise_type[@]}/test_primesense_${noise_type[@]}_${perturbation[@]}/a6-cPnP-${tless_minus_variant[@]}-1-per-obj-iter0_tless-test.csv"
            eval "$command"
            command="mv ./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/inference_dummy/tless_bop_test_primesense/a6-cPnP-${tless_minus_variant[@]}-1-per-obj-iter0_tless-test_tab_obj_col.txt  ./datasets/BOP_DATASETS/tless/perturbations/${noise_type[@]}/test_primesense_${noise_type[@]}_${perturbation[@]}/a6-cPnP-${tless_minus_variant[@]}-1-per-obj-iter0_tless-test_tab_obj_col.txt"
            eval "$command"
            command="mv ./output/gdrn/40_epochs/${tless_variant[@]}_SO/_all/inference_dummy/tless_bop_test_primesense/a6-cPnP-${tless_minus_variant[@]}-1-per-obj-iter0_tless-test_tab_obj_row.txt  ./datasets/BOP_DATASETS/tless/perturbations/${noise_type[@]}/test_primesense_${noise_type[@]}_${perturbation[@]}/a6-cPnP-${tless_minus_variant[@]}-1-per-obj-iter0_tless-test_tab_obj_row.txt"
            eval "$command"
        done
    done
done




import os
import csv
import matplotlib.pyplot as plt
import scienceplots
import numpy as np
import string
import json

plt.style.use('science')

def read_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

if __name__ == "__main__":

    tless_directory = "./datasets/BOP_DATASETS/tless"

    perturbation_types=["gaussian_noise","shot_noise","motion_blur","brightness","gaussian_blur"]
    perturbation_types_print=["Gaussian Noise", "Shot Noise", "Motion Blur", "Brightness", "Gaussian Blur"]
    
    tless_gaussian_noise = [72.14, 11.57, 11.38, 8.02, 7.07, 6.97]
    tless_shot_noise = [72.14, 14.92, 9.08, 7.10, 6.73, 7.04]
    tless_motion_blur = [72.14, 59.02, 53.51, 41.68, 29.27, 23.14] 
    tless_brightness = [72.14, 57.39, 55.21, 47.95, 37.91, 29.78]
    tless_gaussian_blur = [72.14, 60.31, 55.05, 39.20, 25.95, 14.43]

    tless_random_gaussian_noise = [75.07, 53.96, 54.38, 49.43, 40.62, 28.01]
    tless_random_shot_noise = [75.07, 55.86, 52.37, 46.24, 35.33, 27.12]
    tless_random_motion_blur = [75.07, 56.08, 50.49, 41.55, 29.24, 24.02]
    tless_random_brightness = [75.07, 59.52, 58.76, 57.62, 54.55, 51.53]
    tless_random_gaussian_blur = [75.07, 58.07, 50.37, 34.55, 24.57, 21.10]

    X = [0, 0.2, 0.4, 0.6, 0.8, 1]

    intensities = [*range(1,6,1)]

    tless_total_ADD_list = []
    tless_random_total_ADD_list = []

    for perturbation_type in perturbation_types:
        tless_total_ADD_list.append(tless_gaussian_noise)
        tless_total_ADD_list.append(tless_shot_noise)
        tless_total_ADD_list.append(tless_motion_blur)
        tless_total_ADD_list.append(tless_brightness)
        tless_total_ADD_list.append(tless_gaussian_blur)        

        tless_random_total_ADD_list.append(tless_random_gaussian_noise)
        tless_random_total_ADD_list.append(tless_random_shot_noise)
        tless_random_total_ADD_list.append(tless_random_motion_blur)
        tless_random_total_ADD_list.append(tless_random_brightness)
        tless_random_total_ADD_list.append(tless_random_gaussian_blur)

    num_rows = 1
    num_cols = 5

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 3))

    for letter, (i, directory) in zip(string.ascii_lowercase, enumerate(perturbation_types_print)):
        row = i // num_cols
        col = i % num_cols

        if num_rows == 1:
            axis = axes[col]  # Access the single row directly
        else:
            axis = axes[row, col]  # Access the 2D array of axes

        axis.plot(X, tless_total_ADD_list[i], color='purple', marker='s', label='TLESS Original')
        axis.plot(X, tless_random_total_ADD_list[i], color='blue', marker='o', label='TLESS Random')

        axis.set_ylim(-0.05, 80)  # Set y-axis to range from 0 to 80
        axis.set_xlim(-0.05, 1.05)

        if num_rows == 1:
            axes[col].set_xlabel('Severity', fontsize=14)
            axes[0].set_ylabel('ADD(-S)', fontsize=14)
            axes[col].set_title(letter + ") " + directory, fontsize=16)
            axes[col].set_xticks(X)
        else:
            axes[row, col].set_xlabel('Severity', fontsize=14)
            axes[row, 0].set_ylabel('ADD(-S)', fontsize=14)
            axes[row, col].set_title(letter + ") " + directory, fontsize=16)
            axes[row, col].set_xticks(X)

    # Hide empty subplots
    for i in range(len(perturbation_types_print), num_rows * num_cols):
        if num_rows == 1:
            col = i
        else:
            row = i // num_cols
            col = i % num_cols
        fig.delaxes(axes[row, col])

    # Get legend handles and labels from a valid subplot
    if num_rows == 1:
        handles, labels = axes[1].get_legend_handles_labels()
    else:
        handles, labels = axes[0, 1].get_legend_handles_labels()

    fig.legend(handles, labels, fontsize=14, loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=4)
    #fig.legend(handles, labels, loc='lower right', fontsize=14, bbox_to_anchor=(1.1, 1.05))
    #fig.legend(handles, labels, fontsize=14, bbox_to_anchor=(1.05, 0))
    plt.tight_layout()
    plt.savefig(tless_directory + "/" + 'plots/grid_graphs.png', dpi=300)
    plt.show()
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

    tless_directory = "/ssd3/datasets_bop/tless"

    perturbation_types=["gaussian_noise","shot_noise","motion_blur","brightness","gaussian_blur"]
    perturbation_types_print=["Gaussian Noise", "Shot Noise", "Motion Blur", "Brightness", "Gaussian Blur"]
    
    # tless_gaussian_noise = [72.14, 11.57, 11.38, 8.02, 7.07, 6.97]
    # tless_shot_noise = [72.14, 14.92, 9.08, 7.10, 6.73, 7.04]
    # tless_motion_blur = [72.14, 59.02, 53.51, 41.68, 29.27, 23.14] 
    # tless_brightness = [72.14, 57.39, 55.21, 47.95, 37.91, 29.78]
    # tless_gaussian_blur = [72.14, 60.31, 55.05, 39.20, 25.95, 14.43]

    # tless_random_gaussian_noise = [75.07, 53.96, 54.38, 49.43, 40.62, 28.01]
    # tless_random_shot_noise = [75.07, 55.86, 52.37, 46.24, 35.33, 27.12]
    # tless_random_motion_blur = [75.07, 56.08, 50.49, 41.55, 29.24, 24.02]
    # tless_random_brightness = [75.07, 59.52, 58.76, 57.62, 54.55, 51.53]
    # tless_random_gaussian_blur = [75.07, 58.07, 50.37, 34.55, 24.57, 21.10]

    tless_shot_noise = [55.03, 15.43458404691473, 8.431729721314028, 5.161866209974572, 3.324199491411075, 2.9517878457626234]
    tless_motion_blur = [55.03, 51.05464736104624, 46.167211583372264, 36.67133738128601, 24.749286418599823, 18.439773729825106]
    tless_gaussian_blur = [55.03, 52.64834708599304, 46.67844724687322, 30.953240956977528, 14.405729409933052, 3.27531267839535]
    tless_random_motion_blur = [55.03, 49.008926254605846, 44.50329544864809, 36.307696299756095, 24.986351133945718, 18.72022419430173]
    tless_gaussian_noise = [55.03, 11.72188489283305, 11.602989257356375, 6.128288961544449, 3.6150812185375476, 2.83854896465826]
    tless_random_gaussian_blur = [55.03, 50.9334163682599, 43.497898178421295, 27.873579324303282, 13.59276558202294, 5.095074990918055]
    tless_random_gaussian_noise = [55.03, 48.424983133530546, 48.42233639524625, 43.936478281177024, 35.668742539830816, 23.606985313197367]
    tless_random_brightness = [55.03, 52.271368519383465, 51.62136073485909, 50.47693185946339, 48.01204006435207, 45.51476464788002]
    tless_brightness = [55.03, 50.26778763817531, 48.19181068036744, 42.93787949556282, 34.82910374176137, 27.57397892988738]
    tless_random_shot_noise = [55.03, 49.893455809850025, 46.60823083709586, 40.972754164720534, 30.28247444081166, 22.36462712128289]


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
        axis.plot(X, tless_random_total_ADD_list[i], color='blue', marker='o', label='TLESS Random Texture')

        axis.set_ylim(-0.05, 70)  # Set y-axis to range from 0 to 80
        axis.set_xlim(-0.05, 1.05)

        if num_rows == 1:
            axes[col].set_xlabel('Severity', fontsize=14)
            axes[0].set_ylabel('AR', fontsize=14)
            axes[col].set_title(letter + ") " + directory, fontsize=16)
            axes[col].set_xticks(X)
        else:
            axes[row, col].set_xlabel('Severity', fontsize=14)
            axes[row, 0].set_ylabel('AR', fontsize=14)
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
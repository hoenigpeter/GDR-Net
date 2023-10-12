import os
import csv
import matplotlib.pyplot as plt
import scienceplots
import numpy as np
import string

plt.style.use('science')

def read_data(filename):
    with open(filename, 'r') as f:
        header = f.readline().strip().split()
        data = {}
        for line in f:
            cols = line.strip().split()
            obj = cols[0]
            values = [float(x) for x in cols[1:]]
            data[obj] = dict(zip(header[1:], values))
    return header, data

if __name__ == "__main__":

    perturbation_types=["gaussian_noise","shot_noise","motion_blur","brightness","gaussian_blur"]
    perturbation_types_print=["Gaussian Noise", "Shot Noise", "Motion Blur", "Brightness", "Gaussian Blur"]

    X = [0, 0.2, 0.4, 0.6, 0.8, 1]

    intensities = [*range(1,6,1)]

    tless_total_ADD_list = []
    tless_random_total_ADD_list = []

    tless_directory = "./datasets/BOP_DATASETS/tless/perturbations_add_0.1"

    for perturbation_type in perturbation_types:
        directory = os.path.join(tless_directory, perturbation_type)
        print(directory)
        tless_ADD_list = []
        #tless_ADD_list.append(68.86)
        tless_ADD_list.append(84.84)

        for intensity in intensities:                                                                    #a6-cPnP-tless-1-per-obj-iter0_tless-test_tab_obj_col.txt
            filepath = os.path.join(directory, "test_primesense_" + perturbation_type + "_" + str(intensity) + '/a6-cPnP-tless-1-per-obj-iter0_tless-test_tab_obj_col.txt')
            header, data = read_data(filepath)
            tless_ADD_list.append(data['Avg(30)']['ad_10'])  

        tless_total_ADD_list.append(tless_ADD_list)

    print(tless_total_ADD_list)

    for perturbation_type in perturbation_types:
        directory = os.path.join(tless_directory, perturbation_type)
        tless_random_ADD_list = []
        #lmo_random_ADD_list.append(71.71)
        tless_random_ADD_list.append(88.87)

        for intensity in intensities:
            filepath = os.path.join(directory, "test_primesense_" + perturbation_type + "_" + str(intensity) + '/a6-cPnP-tless-random-texture-1-per-obj-iter0_tless-test_tab_obj_col.txt')
            header, data = read_data(filepath)
            tless_random_ADD_list.append(data['Avg(30)']['ad_10'])

        tless_random_total_ADD_list.append(tless_random_ADD_list)

    print(tless_random_total_ADD_list)

    for letter, (i, directory) in zip(string.ascii_lowercase, enumerate(perturbation_types)):
            plt.figure(i + 1)

            plt.plot(X, tless_total_ADD_list[i], color='red', marker='s', label='TLESS ADD(S)')

            plt.plot(X, tless_random_total_ADD_list[i], color='orange', marker='s', label='TLESS Random ADD(S)')

            plt.xlabel('Severity', fontsize=14)
            plt.ylabel('Error',fontsize=14)
            plt.title(letter + ") " + directory, fontsize=16)
            plt.xticks(X)
            plt.legend(bbox_to_anchor=(1.1, 1.05))
            plt.savefig(tless_directory + "/" + f'plots/{directory}_graph.png', dpi=300)
            plt.close()

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

        axis.plot(X, tless_total_ADD_list[i], color='green', marker='s', label='TLESS Original')
        axis.plot(X, tless_random_total_ADD_list[i], color='blue', marker='o', label='TLESS Random')

        if num_rows == 1:
            axes[col].set_xlabel('Severity', fontsize=14)
            axes[0].set_ylabel('ADD(S)', fontsize=14)
            axes[col].set_title(letter + ") " + directory, fontsize=16)
            axes[col].set_xticks(X)
        else:
            axes[row, col].set_xlabel('Severity', fontsize=14)
            axes[row, 0].set_ylabel('ADD(S)', fontsize=14)
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

    #fig.legend(handles, labels, loc='lower right', fontsize=14, bbox_to_anchor=(1.1, 1.05))
    fig.legend(handles, labels, fontsize=14, bbox_to_anchor=(1.05, 0))
    plt.tight_layout()
    plt.savefig(tless_directory + "/" + 'plots/grid_graphs.png', dpi=300)
    plt.show()
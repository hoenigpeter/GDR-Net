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

    lmo_total_ADD_list = []
    lmo_random_total_ADD_list = []

    tless_total_ADD_list = []
    tless_random_total_ADD_list = []

    lmo_directory = "./datasets/BOP_DATASETS/lmo/perturbations_add_0.1"
    tless_directory = "./datasets/BOP_DATASETS/tless/perturbations_add_0.1"

    for perturbation_type in perturbation_types:
        directory = os.path.join(lmo_directory, perturbation_type)
        print(directory)
        lmo_ADD_list = []
        lmo_ADD_list.append(99.03)

        for intensity in intensities:
            filepath = os.path.join(directory, "lmo_test_" + perturbation_type + "_" + str(intensity) + '/a6-cPnP-lmo-1-per-obj-iter0_lmo-test_tab_obj_col.txt')
            header, data = read_data(filepath)
            lmo_ADD_list.append(data['Avg(8)']['ad_10'])  

        lmo_total_ADD_list.append(lmo_ADD_list)

    print("LMO: ", lmo_total_ADD_list)

    for perturbation_type in perturbation_types:
        directory = os.path.join(lmo_directory, perturbation_type)
        lmo_random_ADD_list = []
        lmo_random_ADD_list.append(97.51)

        for intensity in intensities:
            filepath = os.path.join(directory, "lmo_test_" + perturbation_type + "_" + str(intensity) + '/a6-cPnP-lmo-random-texture-all-1-per-obj-iter0_lmo-test_tab_obj_col.txt')
            header, data = read_data(filepath)
            lmo_random_ADD_list.append(data['Avg(8)']['ad_10'])   

        lmo_random_total_ADD_list.append(lmo_random_ADD_list)

    print("LMO Random: ", lmo_random_total_ADD_list)

    for perturbation_type in perturbation_types:
        directory = os.path.join(tless_directory, perturbation_type)
        print(directory)
        tless_ADD_list = []
        tless_ADD_list.append(84.84)

        for intensity in intensities:
            filepath = os.path.join(directory, "test_primesense_" + perturbation_type + "_" + str(intensity) + '/a6-cPnP-tless-1-per-obj-iter0_tless-test_tab_obj_col.txt')
            header, data = read_data(filepath)
            tless_ADD_list.append(data['Avg(30)']['ad_10'])  

        tless_total_ADD_list.append(tless_ADD_list)

    print("TLESS: ", tless_total_ADD_list)

    for perturbation_type in perturbation_types:
        directory = os.path.join(tless_directory, perturbation_type)
        tless_random_ADD_list = []
        tless_random_ADD_list.append(88.87)

        for intensity in intensities:
            filepath = os.path.join(directory, "test_primesense_" + perturbation_type + "_" + str(intensity) + '/a6-cPnP-tless-random-texture-1-per-obj-iter0_tless-test_tab_obj_col.txt')
            header, data = read_data(filepath)
            tless_random_ADD_list.append(data['Avg(30)']['ad_10'])    

        tless_random_total_ADD_list.append(tless_random_ADD_list)

    print("TLESS Random: ", tless_random_total_ADD_list)

    num_rows = 2
    num_cols = 5

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 6))

    for letter, (i, directory) in zip(string.ascii_lowercase, enumerate(perturbation_types_print)):
        row = 0
        col = i % num_cols

        axis = axes[row, col]  # Access the 2D array of axes

        axis.plot(X, lmo_total_ADD_list[i], color='green', marker='s', label='LMO Original')
        axis.plot(X, lmo_random_total_ADD_list[i], color='red', marker='o', label='LMO Random')

        axes[row, col].set_xlabel('Severity', fontsize=14)
        axes[row, 0].set_ylabel('ADD(S)', fontsize=14)
        axes[row, col].set_title(letter + ") " + directory, fontsize=16)
        axes[row, col].set_xticks(X)
    
    for letter, (i, directory) in zip(string.ascii_lowercase[num_cols:], enumerate(perturbation_types_print)):
        row = 1
        col = i % num_cols

        axis = axes[row, col]  # Access the 2D array of axes

        axis.plot(X, tless_total_ADD_list[i], color='purple', marker='s', label='TLESS Original')
        axis.plot(X, tless_random_total_ADD_list[i], color='blue', marker='o', label='TLESS Random')

        axes[row, col].set_xlabel('Severity', fontsize=14)
        axes[row, 0].set_ylabel('ADD(S)', fontsize=14)
        axes[row, col].set_title(letter + ") " + directory, fontsize=16)
        axes[row, col].set_xticks(X)

    # # Get legend handles and labels from a valid subplot
    handles, labels = axes[0, 1].get_legend_handles_labels()

    # Get handles and labels from axes[0, 1]
    handles1, labels1 = axes[0, 1].get_legend_handles_labels()

    # Get handles and labels from axes[1, 1]
    handles2, labels2 = axes[1, 1].get_legend_handles_labels()

    # Combine the handles and labels
    all_handles = handles1 + handles2
    all_labels = labels1 + labels2

    # #fig.legend(handles, labels, loc='lower right', fontsize=14, bbox_to_anchor=(1.1, 1.05))
    # fig.legend(handles, labels, fontsize=14, bbox_to_anchor=(1.15, 0))
    fig.legend(all_handles, all_labels, fontsize=14, loc='upper center', bbox_to_anchor=(0.5, 0),
          fancybox=True, shadow=True, ncol=4)
    fig.tight_layout()
    fig.savefig('image_output.png', dpi=300, format='png', bbox_inches='tight')
    #plt.savefig(lmo_directory + "/" + 'plots/grid_graphs.png', dpi=300)
    plt.show()
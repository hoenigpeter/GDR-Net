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

#directories =  ["saturate"]

# directories=["gaussian_noise","shot_noise","impulse_noise","defocus_blur"
# "glass_blur","motion_blur","zoom_blur","snow","frost","fog"
# "brightness","contrast","elastic_transform","pixelate","jpeg_compression"
# "speckle_noise","gaussian_blur","spatter","saturate"]

if __name__ == "__main__":

    perturbation_types=["gaussian_noise","shot_noise","impulse_noise","defocus_blur",
    "glass_blur","motion_blur","zoom_blur","snow","frost","fog",
    "brightness","contrast","elastic_transform","pixelate","jpeg_compression",
    "speckle_noise","gaussian_blur","spatter","saturate"]

    perturbation_types_print=["Gaussian Noise", "Shot Noise", "Impulse Noise", "Defocus Blur",
 "Glass Blur", "Motion Blur", "Zoom Blur", "Snow", "Frost", "Fog",
 "Brightness", "Contrast", "Elastic Transform", "Pixelate", "JPEG Compression",
 "Speckle Noise", "Gaussian Blur", "Spatter", "Saturate"]

    X = [0, 0.2, 0.4, 0.6, 0.8, 1]

    intensities = [*range(1,6,1)]

    lmo_total_ADD_list = []
    lmo_random_total_ADD_list = []

    lmo_total_R_list = []
    lmo_random_total_R_list = []

    lmo_total_t_list = []
    lmo_random_total_t_list = []

    lmo_directory = "./datasets/BOP_DATASETS/lmo/test"

    with open(os.path.join(lmo_directory, 'lmo_perturbations.csv'), 'w', newline ='') as lmo_ADD_file:
        # read the first file
        for perturbation_type in perturbation_types:
            directory = os.path.join(lmo_directory, perturbation_type)
            print(directory)
            lmo_ADD_list = []
            lmo_ADD_list.append(48.98)
            lmo_R_list = []
            lmo_R_list.append(51.37)
            lmo_t_list = []
            lmo_t_list.append(85.28)
            for intensity in intensities:
                filepath = os.path.join(directory, "lmo_test_" + perturbation_type + "_" + str(intensity) + '/a6-cPnP-lmo-1-per-obj-iter0_lmo-test_tab_obj_col.txt')
                header, data = read_data(filepath)
                lmo_ADD_list.append(data['Avg(8)']['ad_0.100'])  
                lmo_R_list.append(data['Avg(8)']['reS_5'])  
                lmo_t_list.append(data['Avg(8)']['teS_5'])  
            # writer = csv.writer(lmo_ADD_file)
            # writer.writerow(lmo_ADD_list)
            lmo_total_ADD_list.append(lmo_ADD_list)
            lmo_total_R_list.append(lmo_R_list)
            lmo_total_t_list.append(lmo_t_list)

    with open(os.path.join(lmo_directory, 'lmo_random_perturbations.csv'), 'w', newline ='') as lmo_random_file:
        for perturbation_type in perturbation_types:
            directory = os.path.join(lmo_directory, perturbation_type)
            lmo_random_ADD_list = []
            lmo_random_ADD_list.append(39.07)
            lmo_random_R_list = []
            lmo_random_R_list.append(44.99)
            lmo_random_t_list = []
            lmo_random_t_list.append(76.15)
            for intensity in intensities:
                filepath = os.path.join(directory, "lmo_test_" + perturbation_type + "_" + str(intensity) + '/a6-cPnP-lmo-random-texture-all-1-per-obj-iter0_lmo-test_tab_obj_col.txt')
                header, data = read_data(filepath)
                lmo_random_ADD_list.append(data['Avg(8)']['ad_0.100'])   
                lmo_random_R_list.append(data['Avg(8)']['reS_5'])   
                lmo_random_t_list.append(data['Avg(8)']['teS_5'])   
            # writer = csv.writer(lmo_random_file)
            # writer.writerow(lmo_random_list)
            lmo_random_total_ADD_list.append(lmo_random_ADD_list)
            lmo_random_total_R_list.append(lmo_random_R_list)
            lmo_random_total_t_list.append(lmo_random_t_list)
            # writing the data into the file

    for letter, (i, directory) in zip(string.ascii_lowercase, enumerate(perturbation_types_print)):
            plt.figure(i + 1)
            #X = [0, 0.2, 0.4, 0.6, 0.8, 1]

            # plt.plot(X, lmo_total_ADD_list[i], color='g', marker='s')
            # plt.plot(X, lmo_total_R_list[i], color='g', marker='s')
            # plt.plot(X, lmo_total_t_list[i], color='g', marker='s')

            # plt.plot(X, lmo_random_total_ADD_list[i], color='b', marker='o')
            # plt.plot(X, lmo_random_total_R_list[i], color='b', marker='o')
            # plt.plot(X, lmo_random_total_t_list[i], color='b', marker='o')

            plt.plot(X, lmo_total_ADD_list[i], color='red', marker='s', label='LMO ADD(S)')
            plt.plot(X, lmo_total_R_list[i], color='green', marker='o', label='LMO RE(5°)')
            plt.plot(X, lmo_total_t_list[i], color='blue', marker='^', label='LMO TE(5cm)')

            plt.plot(X, lmo_random_total_ADD_list[i], color='orange', marker='s', label='LMO Random ADD(S)')
            plt.plot(X, lmo_random_total_R_list[i], color='purple', marker='o', label='LMO Random RE(5°)')
            plt.plot(X, lmo_random_total_t_list[i], color='cyan', marker='^', label='LMO Random TE(5cm)')

            plt.xlabel('Severity', fontsize=14)
            plt.ylabel('Error',fontsize=14)
            plt.title(letter + ") " + directory, fontsize=16)
            plt.xticks(X)
            plt.legend(bbox_to_anchor=(1.1, 1.05))
            plt.savefig(lmo_directory + "/" + f'plots/{directory}_graph.png', dpi=300)
            plt.close()

    num_rows = 4
    num_cols = 5

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 8))

    for letter, (i, directory) in zip(string.ascii_lowercase, enumerate(perturbation_types_print)):
        row = i // num_cols
        col = i % num_cols

        axes[row, col].plot(X, lmo_total_ADD_list[i], color='green', marker='s', label='LMO Original')
        #axes[row, col].plot(X, lmo_total_R_list[i], color='green', marker='o', label='LMO RE(5°)')
        #axes[row, col].plot(X, lmo_total_t_list[i], color='blue', marker='^', label='LMO TE(5cm)')
        axes[row, col].plot(X, lmo_random_total_ADD_list[i], color='blue', marker='o', label='LMO Random')
        #axes[row, col].plot(X, lmo_random_total_R_list[i], color='purple', marker='o', label='LMO Random RE(5°)')
        #axes[row, col].plot(X, lmo_random_total_t_list[i], color='cyan', marker='^', label='LMO Random TE(5cm)')

        axes[row, col].set_xlabel('Severity', fontsize=14)
        axes[row, 0].set_ylabel('ADD(S)', fontsize=14)
        axes[row, col].set_title(letter + ") " + directory, fontsize=16)
        axes[row, col].set_xticks(X)

    # Hide empty subplots
    for i in range(len(perturbation_types_print), num_rows * num_cols):
        row = i // num_cols
        col = i % num_cols
        fig.delaxes(axes[row, col])

    handles, labels = axes[1,1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower right', fontsize=14)
    plt.tight_layout() 
    plt.savefig(lmo_directory + "/" + 'plots/grid_graphs.png', dpi=300)
    plt.show()

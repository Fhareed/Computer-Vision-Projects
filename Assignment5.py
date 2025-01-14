# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1t8Sxpx5TQZSIuyOY_NpstO4-hpdTwEiz
"""

from google.colab import drive
drive.mount('/content/drive')

#Assigment 5 Start
!git clone https://github.com/jboutell/DC-DFFN.git

!pip install open3d trimesh point_cloud_utils pyhocon GPUtil CGAL

# Commented out IPython magic to ensure Python compatibility.
# %cd DC-DFFN/utils

!python npy2ply.py ../code/demo/shapenet/04256520/4bdfbfa1871f2ca114038d588fd1342f/models/model_normalized.npy model_normalized.ply

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/DC-DFFN/utils/DC-DFFN
# %cd code

!python evaluate/eval.py \
    --expname shapenet \
    --parallel \
    --exps_folder_name trained_models \
    --timestamp 2022_08_19_16_19_30 \
    --checkpoint 1500 \
    --conf ./confs/shapenet_vae.conf \
    --split ./confs/splits/shapenet/shapenet_sofa_test_files.conf \
    --resolution 100

my_path = "trained_models/shapenet_vae/2022_08_19_16_19_30/evaluation/1500/"
print(my_path)

!cd /content/DC-DFFN  # Move to the repository folder using !
!ls  # List files using !

!cd /content/DC-DFFN/utils/DC-DFFN/code
!ls evaluate

!python3 /content/DC-DFFN/code/evaluate/eval.py --expname shapenet --parallel --exps_folder_name trained_models --timestamp 2022_08_19_16_19_30 --checkpoint 1500 --conf ./confs/shapenet_vae.conf --split ./confs/splits/shapenet/shapenet_sofa_test_files.conf --resolution 100

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/DC-DFFN/utils
!python npy2ply.py ../code/demo/shapenet/04256520/1d4e0d1e5935091f78b03575bb54dfd4/models/model_normalized.npy model_normalized_2.ply

from google.colab import files
files.download("/content/DC-DFFN/utils/model_normalized_2.ply")

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/DC-DFFN/
!find . -name "shapenet_sofa_test_files.json"

!cat ./code/confs/splits/shapenet/shapenet_sofa_test_files.json

import json

# Path to the JSON file
file_path = "./code/confs/splits/shapenet/shapenet_sofa_test_files.json"

# Load the JSON file
with open(file_path, 'r') as f:
    data = json.load(f)

# Replace the ID
old_id = "4bdfbfa1871f2ca114038d588fd1342f"
new_id = "1d4e0d1e5935091f78b03575bb54dfd4"
if old_id in data["shapenet"]["04256520"]:
    data["shapenet"]["04256520"][new_id] = data["shapenet"]["04256520"].pop(old_id)

# Save the updated JSON file
with open(file_path, 'w') as f:
    json.dump(data, f, indent=4)

print("JSON file updated successfully.")

import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/DC-DFFN/code
!python evaluate/eval.py --expname shapenet --parallel \
--exps_folder_name trained_models --timestamp 2022_08_19_16_19_30 --checkpoint 1500 \
--conf ./confs/shapenet_vae.conf --split ./confs/splits/shapenet/shapenet_sofa_test_files.conf --resolution 100

import numpy as np

# Load the latent vectors
latent_vector_1 = np.loadtxt("/content/sample_data/latent_vector.csv", delimiter=",")
latent_vector_2 = np.loadtxt("/content/sample_data/latent_vector_2.csv", delimiter=",")

# Compute the arithmetic mean
mean_vector = (latent_vector_1 + latent_vector_2) / 2

# Save the mean vector to a new .csv file
mean_vector_path = "/content/DC-DFFN/code/mean_latent_vector.csv"
np.savetxt(mean_vector_path, mean_vector, delimiter=",", fmt="%.6f")

print(f"Mean latent vector saved to {mean_vector_path}")

from google.colab import files
files.download(mean_vector_path)
# Print the row vector
print("Mean Vector (Row Format):")
print(mean_vector)

!ls /content/DC-DFFN/trained_models/shapenet_vae/2022_08_19_16_19_30/evaluation/1500/nonuniform_iteration_1500_1d4e0d1e5935091f78b03575bb54dfd4_model_normalized_id.ply

!ls /content/DC-DFFN/utils/

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/DC-DFFN/code/
!python training/exp_runner.py --nepoch 1001 --batch_size 1 --conf ./confs/recon_vae.conf

!python evaluate/eval.py --expname shapenet --exps_folder_name exps \
--timestamp 2024_12_22_15_59_42 --checkpoint 1000 --conf ./confs/recon_vae.conf \
--resolution 100 --recon_only

!ls /content/DC-DFFN/exps/recon_vae/
!ls /content/DC-DFFN/exps/recon_vae/2024_12_22_15_59_42/evaluation/1000/

mesh_path = "/content/DC-DFFN/exps/recon_vae/2024_12_22_15_59_42/evaluation/1000/reconstructed_mesh.ply"
from google.colab import files
files.download(mesh_path)
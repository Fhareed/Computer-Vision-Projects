# -*- coding: utf-8 -*-
"""MLCompVision Assigment1

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tV9ZwGKoAQc95_d4YXfzJk_8qthEuUvI
"""

from google.colab import drive
drive.mount('/content/drive')

!unzip /content/drive/MyDrive/Colab Notebooks/CIFAR10-mini.zip

import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Dense, Flatten
from tensorflow.keras.models import Model
from keras.utils import to_categorical
from PIL import Image

import zipfile
import os
zip_ref = zipfile.ZipFile("/content/drive/MyDrive/ColabNotebooks/CIFAR10-mini.zip", 'r')
zip_ref.extractall("/tmp")
zip_ref.close()
def inspect_zipfile(zip_filepath):
    # Extract the zip file
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall('CIFAR10-mini')

    # Define paths to training and testing folders
    training_folder = os.path.join('CIFAR10-mini', 'training')
    testing_folder = os.path.join('CIFAR10-mini', 'testing')

    # Get the list of files in each folder
    training_files = os.listdir(training_folder)
    testing_files = os.listdir(testing_folder)

    # Count the number of files
    num_training_files = len(training_files)
    num_testing_files = len(testing_files)

    print(f"Number of files in training folder: {num_training_files}")
    print(f"Number of files in testing folder: {num_testing_files}")

    # Optionally, list the first few files for inspection
    print(f"Sample files in training folder: {training_files[:5]}")
    print(f"Sample files in testing folder: {testing_files[:5]}")

# Call the function with your CIFAR10-mini.zip file path
inspect_zipfile('/content/drive/MyDrive/ColabNotebooks/CIFAR10-mini.zip')

os.listdir('CIFAR10-mini/testing')


##Assigment 2 start
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader
from PIL import Image
# Function to load images
def load_images(folder, image_count, image_size):
    array_shape = (image_count, image_size[0], image_size[1], image_size[2])  # Original shape: B✕H✕W✕C
    imageset = np.empty(array_shape, dtype='float32')
    for i in range(image_count):
        image = Image.open(f"{folder}/image_{i:04d}.png").resize((image_size[1], image_size[0]))  # Ensure resizing to target H, W
        imageset[i] = np.asarray(image) / 255.0  # Normalize to [0,1]
    # Transpose to PyTorch format (B✕C✕H✕W)
    imageset = np.transpose(imageset, (0, 3, 1, 2))  # Transpose to (batch, channels, height, width)
    return imageset
# Function to load labels
def load_labels(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    labels = np.array([int(line.strip()) for line in lines], dtype='int')
    return labels
# Function to normalize images to the range [-1, 1]
def normalize_dataset(images):
    return images * 2.0 - 1.0  # Scale to [-1, 1] range
def one_hot_encode_labels(labels, num_classes=10):
    return to_categorical(labels, num_classes=num_classes)
# Function to split data into test and validation sets
def split_test_val(data, split_point):
    return data[:split_point], data[split_point:]

# Assuming load_images, load_labels, normalize_dataset, and split_test_val are already defined
# Load and preprocess the data
Y_test = load_labels('testing/labels.csv')
X_test = load_images('testing', len(Y_test), (32,32,3))
X_test = normalize_dataset(X_test)
y_train = load_labels('training/labels.csv')
x_train = load_images('training', len(y_train), (32,32,3))
x_train = normalize_dataset(x_train)
# Split test data into test and validation sets
split_point = 3000
x_test, x_val = split_test_val(X_test, split_point)
y_test, y_val = split_test_val(Y_test, split_point)
#create one hot labels
y_train = one_hot_encode_labels(y_train, num_classes=10)
y_val = one_hot_encode_labels(y_val, num_classes=10)
y_test = one_hot_encode_labels(y_test, num_classes=10)
# Convert data arrays to PyTorch tensors
train_images_tensor = torch.Tensor(x_train)  # Training images tensor
train_labels_tensor = torch.Tensor(y_train).long()  # Training labels tensor
val_images_tensor = torch.Tensor(x_val)  # Validation images tensor
val_labels_tensor = torch.Tensor(y_val).long()  # Validation labels tensor
test_images_tensor = torch.Tensor(x_test)  # Test images tensor
test_labels_tensor = torch.Tensor(y_test).long()  # Test labels tensor
# Create TensorDatasets
train_dataset = TensorDataset(train_images_tensor, train_labels_tensor)
val_dataset = TensorDataset(val_images_tensor, val_labels_tensor)
test_dataset = TensorDataset(test_images_tensor, test_labels_tensor)
# Define DataLoaders with appropriate batch sizes and shuffling options
batch_size = 64
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

from torch.utils.data import DataLoader, TensorDataset

# Assuming x_val, y_val, x_test, and y_test are the validation and test datasets
# Convert numpy arrays to PyTorch tensors if they aren't already
x_val_tensor = torch.Tensor(x_val).to("cuda")
y_val_tensor = torch.LongTensor(y_val).to("cuda")

x_test_tensor = torch.Tensor(x_test).to("cuda")
y_test_tensor = torch.LongTensor(y_test).to("cuda")

# Create TensorDataset and DataLoader for validation and test sets
validation_dataset = TensorDataset(x_val_tensor, y_val_tensor)
validation_loader = DataLoader(validation_dataset, batch_size=32, shuffle=False)

test_dataset = TensorDataset(x_test_tensor, y_test_tensor)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# Now, you can run the validation/test loop using validation_loader or test_loader as needed.

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # Convolutional layers
        self.conv1 = nn.Conv2d(3, 32, 3, stride=1, padding='same')  # Input channels=3, Output channels=32
        self.conv2 = nn.Conv2d(32, 64, 3, stride=1, padding='same')  # Input=32, Output=64
        self.conv3 = nn.Conv2d(64, 128, 3, stride=1, padding='same')  # Input=64, Output=128
        # Fully connected (Linear) layers
        self.fc1 = nn.Linear(128 * 4 * 4, 128)  # 128 feature maps with 4x4 each
        self.fc2 = nn.Linear(128, 10)  # Output layer with 10 classes (e.g., CIFAR-10)
    def forward(self, x):
        # First convolutional layer
        x = self.conv1(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        # Second convolutional layer
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        # Third convolutional layer
        x = self.conv3(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        # Flattening the output for the fully connected layers
        x = torch.flatten(x, 1)
        # First fully connected layer
        x = self.fc1(x)
        x = F.relu(x)
        # Output layer
        output = self.fc2(x)
        output = F.log_softmax(output, dim=1)  # Log softmax for classification
        return output

# Initialize the model and move it to GPU
my_nn = Net().to("cuda")
from torchsummary import summary
summary(my_nn, (3, 32, 32))
# Define the loss function
loss_fn = nn.CrossEntropyLoss()
# Define the optimizer
optimizer = optim.Adam(my_nn.parameters(), lr=2e-4)
# Training loop
num_epochs = 50  # Adjust as needed
for epoch in range(num_epochs):
    for x_batch, y_batch in train_loader:  # train_loader should already be defined
        # Move data to GPU
        x_batch = x_batch.to("cuda")
        y_batch = y_batch.to("cuda")
        # Convert one-hot encoded labels to class indices
        y_batch = torch.argmax(y_batch, dim=1) #This line is added to convert one-hot to class indices
        # Forward pass
        y_pred = my_nn(x_batch)
        loss = loss_fn(y_pred, y_batch)  # Compute the loss
        # Backward pass and optimization
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    # Optional: Print loss for tracking progress
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}")

# Validation/Test loop
correct_labels = 0
total_label_count = 0

# Set the model to evaluation mode
my_nn.eval()

# Disable gradient computation for validation/test
with torch.no_grad():
    for x_batch, y_batch in validation_loader:  # Replace 'validation_loader' with 'test_loader' for testing
        # Move data to GPU
        x_batch = x_batch.to("cuda")
        y_batch = y_batch.to("cuda")

        # Forward pass
        validation_outputs = my_nn(x_batch)

        # Get predictions
        _, predicted_labels = torch.max(validation_outputs.data, 1)

        # Convert one-hot encoded labels to class indices before comparison
        actual_labels = torch.argmax(y_batch, dim=1)

        # Update the total and correct label counts
        total_label_count += y_batch.size(0)
        correct_labels += (predicted_labels == actual_labels).sum().item() # Compare with actual_labels

# Calculate accuracy
accuracy = (correct_labels / total_label_count) * 100
print(f"Validation/Test Accuracy: {accuracy:.2f}%")

# Training loop
num_epochs = 50  # Adjust as needed
for epoch in range(num_epochs):
    my_nn.train()  # Set the model to training mode
    running_loss = 0.0

    for x_batch, y_batch in train_loader:
        # Move data to GPU
        x_batch = x_batch.to("cuda")
        y_batch = y_batch.to("cuda")

        # Convert one-hot encoded labels to class indices
        y_batch = torch.argmax(y_batch, dim=1) #This line is added to convert one-hot to class indices

        # Forward pass
        outputs = my_nn(x_batch)
        loss = loss_fn(outputs, y_batch)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Accumulate loss
        running_loss += loss.item()

    print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {running_loss / len(train_loader):.4f}")

# Validation loop
correct_labels = 0
total_label_count = 0

# Set the model to evaluation mode
my_nn.eval()

with torch.no_grad():
    for x_batch, y_batch in validation_loader:
        # Move data to GPU
        x_batch = x_batch.to("cuda")
        y_batch = y_batch.to("cuda")

        # Forward pass
        outputs = my_nn(x_batch)

        # Get predictions
        _, predicted_labels = torch.max(outputs, 1)

        # Convert one-hot encoded labels to class indices before comparison
        actual_labels = torch.argmax(y_batch, dim=1)

        # Update total and correct counts
        total_label_count += y_batch.size(0)
        correct_labels += (predicted_labels == actual_labels).sum().item() # Compare with actual_labels

validation_accuracy = (correct_labels / total_label_count) * 100
print(f"Validation Accuracy: {validation_accuracy:.2f}%")

# Testing loop
correct_labels = 0
total_label_count = 0

# Set the model to evaluation mode
my_nn.eval()

with torch.no_grad():
    for x_batch, y_batch in test_loader:
        # Move data to GPU
        x_batch = x_batch.to("cuda")
        y_batch = y_batch.to("cuda")

        # Forward pass
        outputs = my_nn(x_batch)

        # Get predictions
        _, predicted_labels = torch.max(outputs, 1)

        # Convert one-hot encoded labels to class indices before comparison
        actual_labels = torch.argmax(y_batch, dim=1) # Convert y_batch to class indices

        # Update total and correct counts
        total_label_count += y_batch.size(0)
        correct_labels += (predicted_labels == actual_labels).sum().item() # Compare with actual_labels

test_accuracy = (correct_labels / total_label_count) * 100
print(f"Test Accuracy: {test_accuracy:.2f}%")
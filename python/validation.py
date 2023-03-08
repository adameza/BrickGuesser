from __future__ import print_function
from __future__ import division
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
from PIL import Image
import copy

input_size = 224

data_dir = "/home/adam/OneDrive/SeniorProjectData/normalized/val"

model_path = "/home/adam/Poly/SeniorProject/python/trained_model.pth"

batch_size = 5


def initialize_model():
  # Initialize these variables which will be set in this if statement. Each of these
  #   variables is model specific.

  model_ft = models.mobilenet_v2(pretrained=True)
  num_ftrs = 1280
  model_ft.classifier = nn.Linear(num_ftrs, 1)

  return model_ft

def main():
  
  model = initialize_model()

  data_transforms =transforms.Compose([
          transforms.Resize(input_size),
          transforms.CenterCrop(input_size),
          transforms.ToTensor(),
          transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
  
  image_datasets = datasets.ImageFolder(data_dir, data_transforms)
  
  val_labels_list = []
  print(len(image_datasets.classes))
  for label in image_datasets.classes:
      # image_datasets[key].classes[label_index] = (float(image_datasets[key].classes[label_index]) / 21000)
      val_labels_list.append(float(label) / 23000)
      
  dataloader = torch.utils.data.DataLoader(image_datasets, batch_size=batch_size, shuffle=False, num_workers=4)
  
  model.load_state_dict(torch.load(model_path)) # Load trained model
  
  for inputs, labels in dataloader:
    expected = torch.Tensor([[val_labels_list[labels[0].item()]],
                            [val_labels_list[labels[1].item()]],
                            [val_labels_list[labels[2].item()]],
                            [val_labels_list[labels[3].item()]],
                            [val_labels_list[labels[4].item()]]])
    actual = model(inputs)
    for val in expected:
      print(f"Expected = {val.item() * 23000}")
    for val in actual:
      print(f"actual = {val.item() * 23000}")


if __name__ == "__main__":
  main()
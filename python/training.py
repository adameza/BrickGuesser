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
import pyautogui
import copy

print("PyTorch Version: ",torch.__version__)
print("Torchvision Version: ",torchvision.__version__)

# Top level data directory. Here we assume the format of the directory conforms
#   to the ImageFolder structure
data_dir = "/home/adam/OneDrive/SeniorProjectData/normalized"

# Number of classes in the dataset
num_outputs = 1

# Batch size for training (change depending on how much memory you have)
batch_size = 5

# Number of epochs to train for
num_epochs = 3

Learning_Rate = 0.12


# Flag for feature extracting. When False, we finetune the whole model,
#   when True we only update the reshaped layer params
feature_extract = True


def train_model(model, dataloaders, criterion, optimizer, num_epochs=25, is_inception=False, train_labels_list=None, val_labels_list=None):
    since = time.time()

    val_acc_history = []
    running_corrects = 0

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0
    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        # Each epoch has a training and validation phase
        train_index = 0
        val_index = 0
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0
            # Iterate over data.
            for inputs, labels in dataloaders[phase]:
                # inputs = inputs.to(device)
                # labels = labels.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    # Get model outputs and calculate loss
                    # Special case for inception because in training it has an auxiliary output. In train
                    #   mode we calculate the loss by summi1.000000ng the final output and the auxiliary output
                    #   but in testing we only consider the final output.
                    if is_inception and phase == 'train':
                        # From https://discuss.pytorch.org/t/how-to-optimize-inception-model-with-auxiliary-classifiers/7958
                        outputs, aux_outputs = model(inputs)
                        loss1 = criterion(outputs, labels)
                        loss2 = criterion(aux_outputs, labels)
                        loss = loss1 + 0.4*loss2
                    else:
                        outputs = model(inputs)
                        if phase == 'train':
                            # print(labels[0].item())
                            expected = torch.Tensor([[train_labels_list[labels[0].item()]],
                                                    [train_labels_list[labels[1].item()]],
                                                    [train_labels_list[labels[2].item()]],
                                                    [train_labels_list[labels[3].item()]],
                                                    [train_labels_list[labels[4].item()]]])
                        else:
                            expected = torch.Tensor([[val_labels_list[labels[0].item()]],
                                                    [val_labels_list[labels[1].item()]],
                                                    [val_labels_list[labels[2].item()]],
                                                    [val_labels_list[labels[3].item()]],
                                                    [val_labels_list[labels[4].item()]]])
                        loss = criterion(outputs, expected)
                        # print(outputs)
                        # print(expected)

                    _, preds = torch.max(outputs, 1)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # statistics
                # print(f"my loss = {loss.item()}")
                running_loss += loss.item() * inputs.size(0)
                for output in torch.le(torch.abs(torch.sub(outputs, expected)), 0.03):
                    if output == True:
                        running_corrects+=1

            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            epoch_acc = float(running_corrects) / len(dataloaders[phase].dataset)

            print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))

            # deep copy the model
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
            if phase == 'val':
                best_model_wts = copy.deepcopy(model.state_dict())
                val_acc_history.append(epoch_acc)

        print()

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
    print('Best val Acc: {:4f}'.format(best_acc))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model, optimizer

def set_parameter_requires_grad(model, feature_extracting):
    if feature_extracting:
        for param in model.parameters():
            param.requires_grad = False
            
def initialize_model(num_outputs, feature_extract, use_pretrained=True):
    # Initialize these variables which will be set in this if statement. Each of these
    #   variables is model specific.

    model_ft = models.mobilenet_v3_small(pretrained=use_pretrained)
    set_parameter_requires_grad(model_ft, feature_extract)
    num_ftrs = 576
    model_ft.classifier = nn.Linear(num_ftrs, num_outputs)
    input_size = 350
    #360 by 240 try making bigger

    return model_ft, input_size

def img_loader(path: str):
    with open(path, "rb") as f:
        img = Image.open(f)
        return img.convert("RGB")



def main():
    
    # # Initialize the model for this run
    model_ft, input_size = initialize_model(num_outputs, feature_extract, use_pretrained=True)

    # # Print the model we just instantiated
    # print(model_ft)
    
    # # Data augmentation and normalization for training
    # # Just normalization for validation
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(input_size),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize(input_size),
            transforms.CenterCrop(input_size),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }   

    print("Initializing Datasets and Dataloaders...")

    # Create training and validation datasets
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x]) for x in ['train', 'val']}
    train_labels_list = []
    val_labels_list = []
    print(len(image_datasets['train'].classes))
    print(len(image_datasets['val'].classes))
    for label in image_datasets['train'].classes:
        # image_datasets[key].classes[label_index] = (float(image_datasets[key].classes[label_index]) / 21000)
        train_labels_list.append(float(label) / 23000)
    for label in image_datasets['val'].classes:
        # image_datasets[key].classes[label_index] = (float(image_datasets[key].classes[label_index]) / 21000)
        val_labels_list.append(float(label) / 23000)

    # print(train_labels_list)
    # print(val_labels_list)
    # Create training and validation dataloaders
    dataloaders_dict = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=batch_size, shuffle=False, num_workers=5) for x in ['train', 'val']}
    # print(len(dataloaders_dict['train'].dataset))
    # print(len(dataloaders_dict['val'].dataset))
    # for inputs, labels in dataloaders_dict['train']:
        # print(labels)
        # print(len(inputs))
    # # Detect if we have a GPU available
    # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


    # # Send the model to GPU
    # model_ft = model_ft.to(device)

    # Gather the parameters to be optimized/updated in this run. If we are
    #  finetuning we will be updating all parameters. However, if we are
    #  doing feature extract method, we will only update the parameters
    #  that we have just initialized, i.e. the parameters with requires_grad
    #  is True.
    params_to_update = model_ft.parameters()
    print("Params to learn:")
    if feature_extract:
        params_to_update = []
        for name,param in model_ft.named_parameters():
            if param.requires_grad == True:
                params_to_update.append(param)
                print("\t",name)
    else:
        for name,param in model_ft.named_parameters():
            if param.requires_grad == True:
                print("\t",name)
                
    # Observe that all parameters are being optimized
    optimizer_ft = torch.optim.Adagrad(params=model_ft.parameters(), lr=Learning_Rate) 
    
    # Setup the loss fxn
    criterion = nn.MSELoss()
    
    # print(model_ft)
    
    checkpoint = torch.load('/home/adam/Poly/SeniorProject/python/trained_model_mobilenet_v3_big.pth')
    model_ft.load_state_dict(checkpoint['model_state_dict'])
    optimizer_ft.load_state_dict(checkpoint['optimizer_state_dict'])

    # Train and evaluate
    model_ft, optimizer_ft = train_model(model_ft, dataloaders_dict, criterion, optimizer_ft, num_epochs=num_epochs, is_inception=False, train_labels_list=train_labels_list, val_labels_list=val_labels_list)
    # # print(model_ft)
    
    torch.save({
                'model_state_dict': model_ft.state_dict(),
                'optimizer_state_dict': optimizer_ft.state_dict(),
                }, "/home/adam/Poly/SeniorProject/python/trained_model_mobilenet_v3_big_again")
    
    # print(model_ft(data_transforms['val'][0]) * 2100)
    # print(model_ft)
    
if __name__ == "__main__":
    main()

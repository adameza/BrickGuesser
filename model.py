from torchvision import transforms
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from torch.optim import SGD


class BrickGuessModel(nn.Module):
    def __init__(self):
        super(BrickGuessModel, self).__init__()

        # pull pretrained mobilenetv2 model
        self.model = models.mobilenet_v2(weights='IMAGENET1K_V2')

        # TO-DO: Should it be a weight or a bias? Or do we need both?
        # final weight
        """ this weight corresponds to the final layer that is being added onto the
            pre-trained mobilenet_v2 model.

            it is responsible for being optimized to guess the number of lego blocks in the image

            it will range from 0-1 (linear)

            it is initialized to zero and will need to be trained
        """
        self.weight = nn.Parameter(torch.tensor(0.), requires_grad=True)

    def train(self, training_set, expected):

        # TO-DO: Is this the right method for optimizing the weight?
        optimizer = SGD(self.model.parameters(), lr=0.1)

        for epoch in range(100):
            total_loss = 0

            for i in range(len(training_set)):
                training_i = training_set[i]
                training_j = training_set[i]



    def forward(self, inputs):
        """ 
            @param inputs: a tensor of input images
        """
        pass

        # preprocess the images into mobilenet_v2's expected format
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        


# testing
model = BrickGuessModel()

from torch import nn
import torch
import torch.nn.functional as F

class FireModule(nn.Module):
    def __init__(self, in_channels, s1x1, e1x1, e3x3):
        super(FireModule, self).__init__()
        self.squeeze = nn.Conv2d(in_channels=in_channels, out_channels=s1x1, kernel_size=1, stride=1)
        self.expand1x1 = nn.Conv2d(in_channels=s1x1, out_channels=e1x1, kernel_size=1, stride=1)
        self.expand3x3 = nn.Conv2d(in_channels=s1x1, out_channels=e3x3, kernel_size=3, stride=1, padding=1)
        
    def forward(self, x):
        x = F.relu(self.squeeze(x))
        x1 = F.relu(self.expand1x1(x))
        x2 = F.relu(self.expand3x3(x))
        x = torch.cat((x1, x2), dim=1)
        return x
    
class SqueezeNet(nn.Module):
    def __init__(self, out_channels):
        super(SqueezeNet, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=96, kernel_size=3, stride=2)
        self.max_pool1 = nn.MaxPool2d(kernel_size=3, stride=2)
        
        self.fire2 = FireModule(in_channels=96, s1x1=16, e1x1=64, e3x3=64)
        self.fire3 = FireModule(in_channels=128, s1x1=16, e1x1=64, e3x3=64)
        self.fire4 = FireModule(in_channels=128, s1x1=32, e1x1=128, e3x3=128)
        self.max_pool2 = nn.MaxPool2d(kernel_size=3, stride=2)
        
        self.fire5 = FireModule(in_channels=256, s1x1=32, e1x1=128, e3x3=128)
        self.fire6 = FireModule(in_channels=256, s1x1=48, e1x1=192, e3x3=192)
        self.fire7 = FireModule(in_channels=384, s1x1=48, e1x1=192, e3x3=192)
        self.fire8 = FireModule(in_channels=384, s1x1=64, e1x1=256, e3x3=256)
        self.max_pool3 = nn.MaxPool2d(kernel_size=3, stride=2)
        
        self.fire9 = FireModule(in_channels=512, s1x1=64, e1x1=256, e3x3=256)
        self.dropout = nn.Dropout(p=0.5)
        self.conv10 = nn.Conv2d(in_channels=512, out_channels=out_channels, kernel_size=1, stride=1)
        self.avg_pool = nn.AvgPool2d(kernel_size=13, stride=13)
        
    def forward(self, x):

        x = self.conv1(x) #
        x = F.relu(x) #

        x = self.max_pool1(x) #

        x = self.fire2(x) #

        x = self.fire3(x) #

        x = self.max_pool2(x) #

        x = self.fire4(x) #

        x = self.fire5(x) #

        x = self.max_pool3(x) #
        
        x = self.fire6(x) #

        x = self.fire7(x) #

        x = self.fire8(x) #

        x = self.fire9(x) #

        x = self.dropout(x) #
        #x = torch.nn.functional.dropout(x, p=0.5)

        x = self.conv10(x)
        x = F.relu(x)

        x = self.avg_pool(x)

        # x = torch.flatten(x, start_dim=1)
        #x = x.unsqueeze(2).unsqueeze(2) # make shape from [1, out_channels] (2 dim) to [1, out_channels, 1, 1] (4 dim)
        return x

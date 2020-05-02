
import torch
import torch.nn as nn
import numpy as np

import torch.nn.functional as F



class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet,self).__init__()
        
        
        activation=nn.ReLU()       
        pool_1 = nn.MaxPool1d(kernel_size=8,stride=8) #Size=8
        pool_2 = nn.MaxPool1d(kernel_size=4,stride=4) #Size=4
        pool_3 = nn.MaxPool1d(kernel_size=2,stride=2) #Size=2
        
      
        self.drop_out = nn.Dropout()
        
      
        
        conv1_f=nn.Conv1d(1,64,kernel_size=400, stride=50,padding=1)
        self.conv2_f=nn.Conv1d(64, 128, kernel_size=6,stride=1,padding=1)
        self.conv3_f=nn.Conv1d(128,128, kernel_size=6,stride=1,padding=1)
        conv4_f=nn.Conv1d(128,128, kernel_size=6,stride=1,padding=1)
        
        
       
        
        self.layer1_f=nn.Sequential(conv1_f, activation, pool_4)
        self.layer2_f=nn.Sequential(conv4_f, activation, pool_2)
        
        self.layer=nn.Sequential(nn.Linear(256,5,bias=False),activation)
        
        
        
        
   
    def forward(self,x):
      
        
        out_f=self.layer1_f(x)
        out_f=self.conv2_f(out_f)
        out_f=self.conv3_f(out_f)
        out_f=self.layer2_f(out_f)

       
        out=out_f.view(-1,256)
        
        out=self.layer(out)
        
        
        return out
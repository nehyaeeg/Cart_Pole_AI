import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

# NN network
class Qnet(nn.Module):
    
    def __init__(self, input_len, hidden_layer_len, output_len): # variabels are dims 
        super().__init__()
        self.linear_layer1 = nn.Linear(input_len, hidden_layer_len) # for linear transformation from input to hidden layer
        self.linear_layer2 = nn.Linear(hidden_layer_len,output_len) # for linear transformation from hidden layer to output layer
        
    # forward iteration transformation
    # input is the state
    def forward(self,state): 
        hidden = F.relu(self.linear_layer1(state))
        output = self.linear_layer2(hidden) # no softmax, will ruin Q values as probabilities(should be able to go above 1)
        return output # action vector



class Q_training():
    def __init__(self, model:Qnet,lr, gamma):
        self.model = model
        self.lr = lr
        self.gamma = gamma
        self.optimizer = optim.Adam(self.model.parameters(), lr) # adam for SGD 
        self.loss = nn.MSELoss() # (Qt-Q)**2
        
    def train_step(self,state,action, reward, new_state, isOver):
        state = torch.tensor(state, dtype=torch.float)
        new_state = torch.tensor(new_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        
        # if 1 sample is inputted
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            new_state = torch.unsqueeze(new_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            isOver = (isOver, )
            
            
        Q = self.model(state) # raw action vector not converted to 0,1. Shows Q values/forward is called
        new_Q = Q.clone()
        
        for index in range(len(state)):
            # if a terminal case
            if isOver[index]:
                temp = reward[index]
            else:
                temp = reward[index] + self.gamma * torch.max(self.model(new_state[index])) # reward  + max Q_new value(which must be predicted again)
                
            new_Q[index][torch.argmax(action[index]).item()] = temp # correct the  entry reflecting max Q, the rest statys the same to not affect loss/learnring
        
        self.optimizer.zero_grad() # zero out gradient to prevent accum
        loss = self.loss(new_Q, Q) # inout for loss
        loss.backward() # get gradeints of loss wrt model.parameters 
        self.optimizer.step() # update the 
    
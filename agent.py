import random
import torch
from game import cart_pole
from model import Q_training, Qnet
from collections import deque

MEMORY_SIZE = 10000
BATCH_SIZE = 1000 # for SGD
ALPHA = 0.001 # learning rate for NN SGD
    
class agent():
    
    def __init__(self, game:cart_pole):
        self.game = game
        self.mem = deque(maxlen= MEMORY_SIZE)
        self.gamma = 0.9 # discount rate
        self.model = Qnet(2,256,2) # 2 in, 256, hidden, 2:out
        self.trainer = Q_training(self.model, ALPHA, self.gamma)
        
        

    def get_state(self):
        deltax = self.game.pole_end[0] - self.game.pole_begin[0]
        if deltax <0:
            return [1,0]
        elif deltax > 0 :
            return [0,1]
        else:
            return [0,0]
    
    
    def get_action(self, state):
        action = [0,0]
        state_input = torch.tensor(state, dtype=torch.float) # convert state to tensor to input to model
        high_index = torch.argmax( self.model(state_input)).item() # index of highest  in action vector //uses Qnet model for a forward iteration
        action[high_index] = 1 # set which action to take
        return action
    
    def store(self, current_state, action, reward, next_state,isOver):
        self.mem.append((current_state,action, reward, next_state,isOver))
        
        
       
    # for target network: Experience replay
    def train_1(self):
        
        if len(self.mem) > BATCH_SIZE: # if more than needed, select a sample
            sample = random.sample(self.mem, BATCH_SIZE) # take a sample of batchsize
        else:
            sample = self.mem # whole memory

        
        states,actions, rewards, new_states, isOvers = zip(*sample) # unpack and group
        self.trainer.train_step(states,actions, rewards, new_states, isOvers) # train on all samples elements
    
    #for short-term predictor
    def traint_2(self,state,action, reward, new_state, isOver):
        self.trainer.train_step(state,action, reward, new_state, isOver) # train with each step taken
        
        

def main():
    game = cart_pole()
    agent_player = agent(game)
    
    while(True):
        current_state = agent_player.get_state()
        action = agent_player.get_action(current_state)
        isOver , reward = game.play_step(action)
        next_state = agent_player.get_state()
        agent_player.store(current_state,action, reward, next_state, isOver)
        agent_player.traint_2(current_state,action, reward, next_state, isOver)
        if isOver:
            agent_player.train_1() # train by experiecne replay of the whole episode
            #plot
            game.reset()
        
        
    
    
if __name__ == "__main__":
    main()
    
    
    
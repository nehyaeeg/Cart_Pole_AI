import math
import random
import pygame

pygame.init()

BLACK = (0,0,0)
WHITE = (255,255,255) 
BLOCK_WIDTH = 30
WIDTH = 800
HEIGHT = 600
FRAME_RATE = 20
POLE_LENGHT = 200

class cart_pole():
    
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Navid's Cart_Pole Balancing AI") #give title
        self.clock = pygame.time.Clock() # for keeping time
        self.reset()
        
    def reset(self):
        print("Reset Called")
        self.x = WIDTH //2
        self.y = HEIGHT //2
        self.pole_begin = [self.x+BLOCK_WIDTH,self.y]
        self.pole_end = [self.x+BLOCK_WIDTH,self.y - POLE_LENGHT]
        self.pole_end[1] +=random.randint(1,5)
        offset =random.randint(1,10)
        if offset<5:
            self.pole_end[0] = 0 -math.sqrt(POLE_LENGHT**2 - (self.pole_end[1] - self.pole_begin[1])**2) + self.pole_begin[0]
        else:
            self.pole_end[0] = 0 +math.sqrt(POLE_LENGHT**2 - (self.pole_end[1] - self.pole_begin[1])**2) + self.pole_begin[0]
        self.number_of_games = 0
            
    def play_step(self, action):
        self.number_of_games += 1
        
        # state = [tilted to left, tilted to right],
        state =[0,0]
        #reward = -10 if pole hits the gound | +10 if pole is vertical| -5 if increasing angle | +5 if decreasing angle
        reward = 0
        
        isOver = False
            
            # Right
        if action[1]==1:
            self.x += 3
            self.pole_begin = [self.x+BLOCK_WIDTH,self.y]
            delta_x = self.pole_end[0] - self.pole_begin[0]
            delta_y = self.pole_end[1] - self.pole_begin[1]
            if delta_x ==0:
                reward = 10
                self.pole_end[1] +=0.5
                if self.pole_end[1] <= 100:
                    self.pole_end[1] = 100
                self.pole_end[0] = 0 -math.sqrt(POLE_LENGHT**2 - (self.pole_end[1] - self.pole_begin[1])**2) + self.pole_begin[0]
            elif delta_x < 0 :
                reward = -10
                self.pole_end[1] += (0.5 + abs(delta_y)//350)
                if self.pole_end[1] <= 100:
                    self.pole_end[1] = 100
                self.pole_end[0] = 0 -math.sqrt(POLE_LENGHT**2 - (self.pole_end[1] - self.pole_begin[1])**2) + self.pole_begin[0]
            else:
                reward = 0
                self.pole_end[1] -= (0.5 + abs(delta_y)//350)
                if self.pole_end[1] <= 100:
                    self.pole_end[1] = 100
                self.pole_end[0] = 0 +math.sqrt(POLE_LENGHT**2 - (self.pole_end[1] - self.pole_begin[1])**2) + self.pole_begin[0]
                
        # Left
        elif action[0]==1:
            self.x -= 3
            self.pole_begin = [self.x+BLOCK_WIDTH,self.y]
            delta_x = self.pole_end[0] - self.pole_begin[0]
            delta_y = self.pole_end[1] - self.pole_begin[1]         
            if delta_x ==0:
                reward = 10
                self.pole_end[1] +=0.5
                if self.pole_end[1] <= 100:
                    self.pole_end[1] = 100
                self.pole_end[0] = 0 -math.sqrt(POLE_LENGHT**2 - (self.pole_end[1] - self.pole_begin[1])**2) + self.pole_begin[0]               
            elif delta_x > 0 :
                reward = -10
                self.pole_end[1] += (0.5 + abs(delta_y)//350)
                if self.pole_end[1] <= 100:
                    self.pole_end[1] = 100
                self.pole_end[0] = 0 +math.sqrt(POLE_LENGHT**2 - (self.pole_end[1] - self.pole_begin[1])**2) + self.pole_begin[0]
                
            else:
                reward = 0
                self.pole_end[1] -= (0.5 + abs(delta_y)//350)
                if self.pole_end[1] <= 100:
                    self.pole_end[1] = 100
                self.pole_end[0] = 0 -math.sqrt(POLE_LENGHT**2 - (self.pole_end[1] - self.pole_begin[1])**2) + self.pole_begin[0]
                
        delta_x = self.pole_end[0] - self.pole_begin[0]
        delta_y = self.pole_end[1] - self.pole_begin[1]
        
        if delta_x < 0:
            self.pole_end[1] += (0.15+ 0.0045*abs(delta_x))
            self.pole_end[0] = 0 -math.sqrt((POLE_LENGHT**2 - (self.pole_end[1] - self.pole_begin[1])**2)) + self.pole_begin[0]       
        elif delta_x >0:   
            self.pole_end[1] += (0.15+ 0.0045*abs(delta_x))
            self.pole_end[0] = 0 +math.sqrt((POLE_LENGHT**2 - (self.pole_end[1] - self.pole_begin[1])**2)) + self.pole_begin[0]  
            
        if self.pole_end[1] >= self.y:
            isOver = True
            
        if self.x >= WIDTH - 2*BLOCK_WIDTH or self.x <= 2*BLOCK_WIDTH or self.number_of_games>200:
            reward = -10
            isOver = True
            
        self.update_screen()
        self.clock.tick(FRAME_RATE)
        return isOver, reward
            
            
            

    def update_screen(self):
        
        self.window.fill(BLACK)
        pygame.draw.rect(self.window, WHITE, pygame.Rect(self.x, self.y, BLOCK_WIDTH*2, BLOCK_WIDTH))
        pygame.draw.line(self.window, WHITE, tuple(self.pole_begin), tuple(self.pole_end), width=5)
        pygame.display.flip()
        
        
    
    
                    
            
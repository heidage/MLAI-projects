import tensorflow as tf
import random
import numpy as np
from collections import deque
from model import LinearQnet, QTrainer
from SnakeGame import SnakeGameAI, Direction, Point

MEMORY_SIZE = 100_000
BATCH_SIZE = 1000
LR = 0.001
NUM_STEPS_FOR_UPDATE = 4

#store game and model
class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 #randomness
        self.gamma = 0.9 #discount rate
        self.memory = deque(maxlen=MEMORY_SIZE)
        self.model = LinearQnet(11,256,3)
        self.trainer = QTrainer(self.model,lr=LR,gamma=self.gamma)

    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
            ]

        return np.array(state, dtype=int)

    def remember(self,state,action,reward,next_state, done):
        return self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory,BATCH_SIZE) #list of tuples
        else:
            mini_sample = self.memory
        
        states,actions,rewards,next_states,dones = zip(*mini_sample)
        self.trainer.train_step(states,actions,rewards,next_states,dones)

    def train_short_memory(self,state,action,reward,next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        #random moves: tradeoff exploration/exploitation
        self.epsilon = 200 - self.n_games
        final_move = 0
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
        else:
            state0 = tf.convert_to_tensor(state, dtype=tf.float32)
            state0 = np.expand_dims(state,axis=0)
            prediction = self.model.predict(state0)
            move = np.argmax(prediction)
        final_move = move
        return final_move

    def check_update_condition(self,t,num_steps_upd):
        if (t + 1) % num_steps_upd == 0:
            return True
        else:
            return False
        
def train():
    max_num_timesteps = 1000
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        # get current state
        state_curr = agent.get_state(game)
        
        # get move
        action = agent.get_action(state_curr)

        #perform move and get new state
        reward, done, score = game.play_step(action)
        state_new = agent.get_state(game)

        #train short memory
        agent.train_short_memory(state_curr,action,reward,state_new,done)
        
        #remember
        agent.remember(state_curr,action,reward,state_new,done)
                
        if done:
            game.reset()
            agent.n_games+=1
            # train long memory(Experience replay) & plot result
            agent.train_long_memory()
            
            if score > record:
                    record = score
                    agent.model.save()

            print('Game:',agent.n_games,'Score:',score,'Record:',record)
            
if __name__ == '__main__':
    train()

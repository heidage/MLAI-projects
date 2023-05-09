import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.optimizers import Adam
import numpy as np


class LinearQnet:
    def __init__(self,input_size,hidden_size,output_size):
        self.q_network = Sequential([
            Input(shape=(input_size,)),
            Dense(hidden_size,activation='relu'),
            Dense(output_size,activation='linear')
            ])
        self.target_q_network = Sequential([
            Input(shape=(input_size,)),
            Dense(hidden_size,activation='relu'),
            Dense(output_size,activation='linear')
            ])
    def predict(self,state):
        return self.q_network.predict(state)
    def save(self):
        self.q_network.save('Snake.h5')
        
class QTrainer:
    def __init__(self,model,lr,gamma):
        self.lr = lr
        self.gamma = gamma
        self.optimizer = Adam(self.lr)
        self.model = model
        
    def compute_loss(self,gamma, q_network,target_q_network,state, action, reward, next_state, done):
        #predicted Q value at current state
        if(len(tf.shape(state))==1):
            state = np.expand_dims(state,axis=0)
            next_state = np.expand_dims(next_state,axis=0)
            action = np.expand_dims(action,axis=0)

        y = q_network(state)
        y = tf.gather_nd(y, tf.stack([tf.range(y.shape[0]),tf.cast(action,tf.int32)],axis=1))
        y_target = tf.identity(y)
        #set y=R if episode terminates, otherwise set y=R+gamma*max Q^(s,a).
        if not done:
            y_target = reward
        else:
            max_qsa = tf.reduce_max(target_q_network(next_state),axis=-1)
            y_target = reward + gamma*max_qsa
            
        loss = MeanSquaredError()
        loss_value = loss(np.expand_dims(y_target,axis=0),y)
        return loss_value

    def agent_learn(self,state, action, reward, next_state, done):
        with tf.GradientTape() as tape:
            loss = self.compute_loss(self.gamma,self.model.q_network,self.model.target_q_network,state,action,reward,next_state,done)

        # Get the gradients of the loss with respect to the weights.
        gradients = tape.gradient(loss, self.model.q_network.trainable_variables)
        
        # Update the weights of the q_network.
        self.optimizer.apply_gradients(zip(gradients, self.model.q_network.trainable_variables))

        # update the weights of target q_network.
        for target_weights, q_net_weights in zip(self.model.target_q_network.weights,self.model.q_network.weights):
            target_weights.assign(0.001*q_net_weights + (1.0-0.001)*target_weights)
            
    def train_step(self, state, action, reward, next_state, done):
        state = tf.convert_to_tensor(state,dtype=tf.float32)
        next_state = tf.convert_to_tensor(next_state,dtype=tf.float32)
        action = tf.convert_to_tensor(action,dtype=tf.double)
        reward = tf.convert_to_tensor(reward, dtype=tf.float32)

        self.agent_learn(state,action,reward,next_state,done)

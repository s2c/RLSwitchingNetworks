import numpy as np
import random
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import backend as K
# https://towardsdatascience.com/proximal-policy-optimization-tutorial-part-1-actor-critic-method-d53f9afffbf6
from collections import deque


clipping_val = 0.2
critic_discount = 0.5
entropy_beta = 0.001
gamma = 0.99
lmbda = 0.95


class PPO:
    def __init__(self, env):
        self.env = env
        self.actor = self.create_actor()
        self.critic = self.create_critic()

        def create_actor(self):
            input_dims = self.env.observation_space.shape
            output_dims = self.env.action_space.n
            state_input = Input(shape=input_dims)
            oldpolicy_probs = Input(shape=(1, output_dims,))
            advantages = Input(shape=(1, 1,))
            rewards = Input(shape=(1, 1,))
            values = Input(shape=(1, 1,))

            x = Dense(24, activation='relu', name='fc1')(state_input)
            x = Dense(48, activation='relu', name='fc2')(x)
            out_actions = Dense(self.env.action_space.n,
                                activation='softmax', name='predictions')(x)

            model = Model(inputs=[state_input, oldpolicy_probs, advantages, rewards, values],
                          outputs=[out_actions])
            model.compile(optimizer=Adam(lr=1e-4), loss=[ppo_loss(
                oldpolicy_probs=oldpolicy_probs,
                advantages=advantages,
                rewards=rewards,
                values=values)])

        def create_critic(self):
            input_dims = self.env.observation_space.shape
            state_input = Input(shape=input_dims)

            # Classification block
            x = Dense(24, activation='relu', name='fc1')(state_input)
            x = Dense(48, activation='relu', name='fc2')(x)
            out_actions = Dense(1, activation='tanh')(x)

            model = Model(inputs=[state_input], outputs=[out_actions])
            model.compile(optimizer=Adam(lr=1e-4), loss='mse')
            # model.summary()
            return model

        def get_advantages(values, masks, rewards):
            returns = []
            gae = 0
            for i in reversed(range(len(rewards))):
                delta = rewards[i] + gamma * \
                    values[i + 1] * masks[i] - values[i]
                gae = delta + gamma * lmbda * masks[i] * gae
                returns.insert(0, gae + values[i])

            adv = np.array(returns) - values[:-1]
            return returns, (adv - np.mean(adv)) / (np.std(adv) + 1e-10)

        def ppo_loss(oldpolicy_probs, advantages, rewards, values):
            def loss(y_true, y_pred):
                newpolicy_probs = y_pred
                ratio = K.exp(K.log(newpolicy_probs + 1e-10) -
                              K.log(oldpolicy_probs + 1e-10))
                p1 = ratio * advantages
                p2 = K.clip(ratio, min_value=1 - clipping_val,
                            max_value=1 + clipping_val) * advantages
                actor_loss = -K.mean(K.minimum(p1, p2))
                critic_loss = K.mean(K.square(rewards - values))
                total_loss = critic_discount * critic_loss + actor_loss - entropy_beta * K.mean(
                    -(newpolicy_probs * K.log(newpolicy_probs + 1e-10)))
                return total_loss

            return loss

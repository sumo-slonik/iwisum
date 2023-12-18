import os
import random

import numpy as np
import tensorflow as tf

from src.maze import Maze
from src.mouse import Mouse


class Solver:
    def __init__(self, map_file_path: str):
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "99"
        tf.get_logger().setLevel("ERROR")
        tf.autograph.set_verbosity(0)
        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
        tf.keras.utils.disable_interactive_logging()

        self.num_actions = 4
        self.learning_rate = 0.1
        self.discount_factor = 0.8
        self.epsilon = 0.6
        self.epsilon_decrease = 0.999
        self.min_epsilon = 0.1
        self.num_episodes = 1000

        self.maze = Maze(map_file_path)
        self.model = self.create_model()

    def create_model(self) -> tf.keras.models.Sequential:
        model = tf.keras.models.Sequential()
        model.add(
            tf.keras.layers.Dense(
                self.maze.width * self.maze.height * self.num_actions,
                input_shape=(2,),
                activation="relu",
            )
        )
        model.add(
            tf.keras.layers.Dense(self.maze.width * self.maze.height, activation="relu")
        )
        model.add(tf.keras.layers.Dense(self.num_actions))
        model.compile(
            loss="mse",
            optimizer=tf.keras.optimizers.legacy.RMSprop(
                learning_rate=self.learning_rate
            ),
        )

        return model

    def get_action(self, state) -> Mouse.Moves:
        if np.random.rand() < self.epsilon:
            return random.choice(list(Mouse.Moves))
        return Mouse.Moves.num_to_move(
            np.argmax(self.model.predict(state.reshape(1, -1)))
        )

    def update_q_table(self, state, action: Mouse.Moves, reward, next_state):
        q_values = self.model.predict(state.reshape(1, -1))
        q_values_next = self.model.predict(next_state.reshape(1, -1))
        max_q_value_next = np.max(q_values_next[0])
        q_values[0, action.value] = (1 - self.learning_rate) * q_values[
            0, action.value
        ] + self.learning_rate * (reward + self.discount_factor * max_q_value_next)
        self.model.fit(state.reshape(1, -1), q_values)

    def start_learning(self):
        for episode in range(self.num_episodes):
            self.maze.draw()
            done = False

            while not done:
                state = np.array([self.maze.mouse.row, self.maze.mouse.column]).reshape(
                    1, 2
                )
                action = self.get_action(state)

                reward = self.maze.mouse.move(action)

                self.maze.draw()

                next_state = np.array(
                    [self.maze.mouse.row, self.maze.mouse.column]
                ).reshape(1, 2)
                self.update_q_table(state, action, reward, next_state)

                if reward < 0:
                    self.maze.mouse.reset()
                    done = True

            if episode % 10 == 0 and self.epsilon > self.min_epsilon:
                self.epsilon *= self.epsilon_decrease

        print("Training complete.")

    def predict(self):
        done = False

        while not done:
            state = np.array([self.maze.mouse.row, self.maze.mouse.column]).reshape(
                1, 2
            )
            action = self.get_action(state)

            reward = self.maze.mouse.move(action)
            if reward < 0:
                done = True
            elif reward == 10:
                print("The target has been reached!")
                done = True

        print("Final position:", (self.maze.mouse.row, self.maze.mouse.column))

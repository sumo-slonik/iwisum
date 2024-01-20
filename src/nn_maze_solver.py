import random

import numpy as np
import tensorflow as tf

from src.maze import Maze
from src.mouse import Mouse
from src.rewards import Reward

import matplotlib.pyplot as plt
from collections import defaultdict


class Solver:
    def __init__(self, map_file_path: str):
        tf.keras.utils.disable_interactive_logging()

        self.num_actions = 4
        self.learning_rate = 0.8
        self.discount_factor = 0.8
        self.epsilon = 0.5
        self.epsilon_decrease = 0.999
        self.min_epsilon = 0.01
        self.num_episodes = 500

        self.maze = Maze(map_file_path)

        self.max_moves = self.maze.height * self.maze.width

        self.rewards = []

        self.q_table = defaultdict(lambda: defaultdict(lambda: 0))

    def get_action(self, state, predict_only=False) -> Mouse.Moves:
        if not predict_only and np.random.rand() < self.epsilon:
            return random.choice(list(Mouse.Moves))
        up, down, left, right = (
            self.q_table[tuple(state[0])][Mouse.Moves.UP],
            self.q_table[tuple(state[0])][Mouse.Moves.DOWN],
            self.q_table[tuple(state[0])][Mouse.Moves.LEFT],
            self.q_table[tuple(state[0])][Mouse.Moves.RIGHT],
        )
        return Mouse.Moves.num_to_move(np.argmax([up, down, left, right]))

    def update_q_table(self, state, action: Mouse.Moves, reward, next_state):
        q_values = self.q_table[tuple(state[0])]
        q_values_next = self.q_table[tuple(next_state[0])]

        max_q_value_next = (
            max(q_values_next.values()) if len(q_values_next.values()) > 0 else 0
        )

        q_values[action] = (
            1
            - self.learning_rate * q_values[action]
            + self.learning_rate * (reward + self.discount_factor * max_q_value_next)
        )

    def start_learning(self):
        for episode in range(self.num_episodes):
            print(episode)
            total_reward = 0
            self.maze.draw()

            while self.maze.mouse.tries < self.max_moves:
                state = np.array([self.maze.mouse.row, self.maze.mouse.column]).reshape(
                    1, -1
                )
                action = self.get_action(state)
                reward = self.maze.mouse.move(action)
                total_reward += reward

                self.maze.draw()

                next_state = np.array(
                    [self.maze.mouse.row, self.maze.mouse.column]
                ).reshape(1, -1)
                self.update_q_table(state, action, reward, next_state)

                if reward == Reward.FINISH.value:
                    print("Reached the target")
                    self.epsilon *= 0.5
                    self.learning_rate *= 0.8
                    self.maze.mouse.reset(target_reached=True)
                    break

            else:
                self.maze.mouse.reset(target_reached=False)

            self.rewards.append(total_reward)

            if episode % 10 == 0 and self.epsilon > self.min_epsilon:
                self.epsilon *= self.epsilon_decrease

        print("Training complete.")
        x = range(len(self.rewards))
        plt.plot(x, self.rewards)
        plt.xlabel("Epoch")
        plt.ylabel("Total reward")

        plt.title("Total rewards by epoch")
        plt.show()

    def predict(self):
        self.maze.draw()

        while self.maze.mouse.tries < self.max_moves:
            state = np.array([self.maze.mouse.row, self.maze.mouse.column]).reshape(
                1, -1
            )
            action = self.get_action(state, predict_only=True)
            reward = self.maze.mouse.move(action)

            self.maze.draw()

            if reward == Reward.FINISH.value:
                print("The target has been reached!")
                break

        print("Final position:", (self.maze.mouse.row, self.maze.mouse.column))

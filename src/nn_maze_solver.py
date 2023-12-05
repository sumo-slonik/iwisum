import numpy as np
import os
import tensorflow as tf

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "99"
tf.get_logger().setLevel("ERROR")
tf.autograph.set_verbosity(0)
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# TODO:
# - read data from json
# - add enums for map and move direction
# - integrate it with maze and mouse modules

width = 5
height = 5
num_actions = 4
learning_rate = 0.1
discount_factor = 0.8
epsilon = 0.6
epsilon_decrease = 0.999
min_epsilon = 0.1
num_episodes = 10000

maze = np.array(
    [
        [2, 0, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1],
        [1, 1, 1, 0, 3],
    ]
)

model = tf.keras.models.Sequential()
model.add(
    tf.keras.layers.Dense(
        width * height * num_actions, input_shape=(2,), activation="relu"
    )
)
model.add(tf.keras.layers.Dense(width * height, activation="relu"))
model.add(tf.keras.layers.Dense(num_actions))
model.compile(
    loss="mse", optimizer=tf.keras.optimizers.RMSprop(learning_rate=learning_rate)
)


def get_action(state):
    if np.random.rand() < epsilon:
        return np.random.randint(num_actions)
    else:
        return np.argmax(model.predict(state.reshape(1, -1)))


def update_q_table(state, action, reward, next_state):
    q_values = model.predict(state.reshape(1, -1))
    q_values_next = model.predict(next_state.reshape(1, -1))
    max_q_value_next = np.max(q_values_next[0])
    q_values[0, action] = (1 - learning_rate) * q_values[0, action] + learning_rate * (
        reward + discount_factor * max_q_value_next
    )
    model.fit(state.reshape(1, -1), q_values)


for episode in range(num_episodes):
    row, col = 0, 0
    done = False
    total_reward = 0

    while not done:
        state = np.array([row, col]).reshape(1, 2)
        action = get_action(state)

        if action == 0:
            next_row, next_col = row - 1, col
        elif action == 1:
            next_row, next_col = row + 1, col
        elif action == 2:
            next_row, next_col = row, col - 1
        elif action == 3:
            next_row, next_col = row, col + 1

        if next_row < 0 or next_row >= height or next_col < 0 or next_col >= width:
            reward = -10
            done = True
        elif maze[next_row, next_col] == 1:
            reward = -5
            done = True
        elif maze[next_row, next_col] == 3:
            reward = 10
            done = True
        else:
            reward = 1

        next_state = np.array([next_row, next_col]).reshape(1, 2)
        update_q_table(state, action, reward, next_state)

        row, col = next_row, next_col
        total_reward += reward

    if episode % 10 == 0 and epsilon > min_epsilon:
        epsilon *= epsilon_decrease

print("Training complete.")

row, col = 0, 0
done = False

while not done:
    state = np.array([row, col]).reshape(1, 2)
    action = np.argmax(model.predict(state.reshape(1, -1)))

    print(action)

    if action == 0:
        next_row, next_col = row - 1, col
    elif action == 1:
        next_row, next_col = row + 1, col
    elif action == 2:
        next_row, next_col = row, col - 1
    elif action == 3:
        next_row, next_col = row, col + 1

    if next_row < 0 or next_row >= height or next_col < 0 or next_col >= width:
        done = True
    elif maze[next_row, next_col] == 1:
        done = True
    elif maze[next_row, next_col] == 3:
        print("The target has been reached!")
        done = True
    else:
        row, col = next_row, next_col

print("Final position:", (row, col))

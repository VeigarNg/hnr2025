import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import random

class State:
    def __init__(self, number_of_state):
        self.num = number_of_state
        self.state = np.identity(number_of_state)[0]

    def normalize_state(self):
        self.state = self.state / np.linalg.norm(self.state)

    def update_probabilities(self):
        """Returns the probabilities for each state as a pandas DataFrame."""
        probabilities = [np.abs(amplitude) ** 2 for amplitude in self.state]
        data = {
            "State": [f"State {i + 1}" for i in range(self.num)],
            "Probability": probabilities,
        }
        return pd.DataFrame(data)

    def right(self):
        right = np.array([
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
        ])
        self.state = np.matmul(right, self.state)

    def left(self):
        left = np.array([
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
        ])
        self.state = np.matmul(left, self.state)

    def top(self):
        top = np.array([
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0],
        ])
        self.state = np.matmul(top, self.state)

    def bottom(self):
        bottom = np.array([
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
        ])
        self.state = np.matmul(bottom, self.state)

    def half_right(self):
        half_right = np.array([
            [1, 0, 0, 0, 0, 1j],
            [0, 1, 0, 0, 1j, 0],
            [0, 0, 1 + 1j, 0, 0, 0],
            [0, 0, 0, 1 + 1j, 0, 0],
            [0, 1j, 0, 0, 1, 0],
            [1j, 0, 0, 0, 0, 1],
        ])
        self.state = np.matmul(half_right, self.state) / np.sqrt(2)

    def half_right_inverse(self):
        half_right = np.array([
            [1, 0, 0, 0, 0, -1j],
            [0, 1, 0, 0, -1j, 0],
            [0, 0, 1 - 1j, 0, 0, 0],
            [0, 0, 0, 1 - 1j, 0, 0],
            [0, -1j, 0, 0, 1, 0],
            [-1j, 0, 0, 0, 0, 1],
        ])
        self.state = np.matmul(half_right, self.state) / np.sqrt(2)

    def half_left(self):
        half_left = np.array([
            [1, 0, 0, 0, 1j, 0],
            [0, 1, 0, 0, 0, 1j],
            [0, 0, 1 + 1j, 0, 0, 0],
            [0, 0, 0, 1 + 1j, 0, 0],
            [1j, 0, 0, 0, 1, 0],
            [0, 1j, 0, 0, 0, 1],
        ])
        self.state = np.matmul(half_left, self.state) / np.sqrt(2)

    def half_left_inverse(self):
        half_left = np.array([
            [1, 0, 0, 0, -1j, 0],
            [0, 1, 0, 0, 0, -1j],
            [0, 0, 1 - 1j, 0, 0, 0],
            [0, 0, 0, 1 - 1j, 0, 0],
            [-1j, 0, 0, 0, 1, 0],
            [0, -1j, 0, 0, 0, 1],
        ])
        self.state = np.matmul(half_left, self.state) / np.sqrt(2)

    def half_top(self):
        half_top = np.array([
            [1 + 1j, 0, 0, 0, 0, 0],
            [0, 1 + 1j, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 1j],
            [0, 0, 0, 1, 1j, 0],
            [0, 0, 0, 1j, 1, 0],
            [0, 0, 1j, 0, 0, 1],
        ])
        self.state = np.matmul(half_top, self.state) / np.sqrt(2)

    def half_top_inverse(self):
        half_top = np.array([
            [1 - 1j, 0, 0, 0, 0, 0],
            [0, 1 - 1j, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, -1j],
            [0, 0, 0, 1, -1j, 0],
            [0, 0, 0, -1j, 1, 0],
            [0, 0, -1j, 0, 0, 1],
        ])
        self.state = np.matmul(half_top, self.state) / np.sqrt(2)

    def half_bottom(self):
        half_bottom = np.array([
            [1 + 1j, 0, 0, 0, 0, 0],
            [0, 1 + 1j, 0, 0, 0, 0],
            [0, 0, 1, 0, 1j, 0],
            [0, 0, 0, 1, 0, 1j],
            [0, 0, 1j, 0, 1, 0],
            [0, 0, 0, 1j, 0, 1],
        ])
        self.state = np.matmul(half_bottom, self.state) / np.sqrt(2)

    def half_bottom_inverse(self):
        half_bottom = np.array([
            [1 - 1j, 0, 0, 0, 0, 0],
            [0, 1 - 1j, 0, 0, 0, 0],
            [0, 0, 1, 0, -1j, 0],
            [0, 0, 0, 1, 0, -1j],
            [0, 0, -1j, 0, 1, 0],
            [0, 0, 0, -1j, 0, 1],
        ])
        self.state = np.matmul(half_bottom, self.state) / np.sqrt(2)

    def display_probabilities(self):
        return np.abs(self.state)**2

    def scramble_cube(self):
        operations = [
            self.right, self.left, self.top, self.bottom,
            self.half_right, self.half_left, self.half_top, self.half_bottom
        ]
        for _ in range(20):
            random.choice(operations)()

# Streamlit App
st.title("Quantum Rubik's Cube Visualizer")

# Initialize cube state
if "cube" not in st.session_state:
    st.session_state.cube = State(6)

# Sidebar for buttons
with st.sidebar:
    st.markdown("### Cube Operations")
    cont1 = st.container()
    col1,col2,col3 = cont1.columns(3)
    if col1.button("R"):
        st.session_state.cube.right()
    if col1.button("L"):
        st.session_state.cube.left()

    if col1.button("U"):
        st.session_state.cube.top()
    if col1.button("D"):
        st.session_state.cube.bottom()

    if col2.button("HR"):
        st.session_state.cube.half_right()
    if col3.button("HR'"):
        st.session_state.cube.half_right_inverse()

    if col2.button("HL"):
        st.session_state.cube.half_left()
    if col3.button("HL'"):
        st.session_state.cube.half_left_inverse()

    if col2.button("HU"):
        st.session_state.cube.half_top()
    if col3.button("HU'"):
        st.session_state.cube.half_top_inverse()

    if col2.button("HD"):
        st.session_state.cube.half_bottom()
    if col3.button("HD'"):
        st.session_state.cube.half_bottom_inverse()

    cont2 = st.container(key="cont2")
    cont2_col = cont2.columns(2)
    if cont2_col[0].button("Initialize"):
        st.session_state.cube = State(6)
    if cont2_col[1].button("Scramble"):
        st.session_state.cube.scramble_cube()

    st.markdown("### State Probabilities")
    probabilities = st.session_state.cube.display_probabilities()
    data = {
        "State": [f"State {i + 1}" for i in range(6)],
        "Probability": probabilities,
    }
    st.dataframe(pd.DataFrame(data))

# Display six separate complex planes with colored quadrants
st.write("### Complex Plane Representation for Each State")
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes = axes.flatten()

# Define color schemes for each state based on Rubik's Cube states
color_map = {
    1: ['yellow', 'yellow', 'blue', 'blue'],  # Quadrant 1 and 2 Yellow
    2: ['blue', 'blue', 'yellow', 'yellow'],  # Quadrant 3 and 4 Yellow
    3: ['yellow', 'blue', 'blue', 'yellow'],  # Quadrant 1 and 4 Yellow
    4: ['blue', 'yellow', 'yellow', 'blue'],  # Quadrant 2 and 3 Yellow
    5: ['yellow', 'blue', 'yellow', 'blue'],  # Quadrant 1 and 3 Yellow
    6: ['blue', 'yellow', 'blue', 'yellow'],  # Quadrant 2 and 4 Yellow
}

for i in range(6):
    # Fill each quadrant individually using fill()
    axes[i].fill([-1, 0, 0, -1], [-1, -1, 0, 0], color=color_map[i+1][2])  # Quadrant 1
    axes[i].fill([0, 1, 1, 0], [-1, -1, 0, 0], color=color_map[i+1][3])  # Quadrant 2
    axes[i].fill([-1, 0, 0, -1], [0, 0, 1, 1], color=color_map[i+1][1])  # Quadrant 3
    axes[i].fill([0, 1, 1, 0], [0, 0, 1, 1], color=color_map[i+1][0])  # Quadrant 4

    # Plot axis and grid
    axes[i].scatter(np.real(st.session_state.cube.state[i]), np.imag(st.session_state.cube.state[i]), color="red")
    axes[i].axhline(0, color='black', linewidth=0.5)
    axes[i].axvline(0, color='black', linewidth=0.5)
    axes[i].set_xlim([-1, 1])
    axes[i].set_ylim([-1, 1])
    axes[i].set_title(f"State {i+1}: {round(st.session_state.cube.display_probabilities()[i],2)}")
    axes[i].set_xlabel("Real Part")
    axes[i].set_ylabel("Imaginary Part")
    axes[i].grid()

plt.tight_layout()
st.pyplot(fig)

st.write(f"Score: {round(np.linalg.norm(st.session_state.cube.display_probabilities()),4)}")

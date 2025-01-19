import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import random
from full import State

# Streamlit App
st.title("Advanced Visualizer")

# Sidebar for buttons
with st.sidebar:
    st.markdown("### Cube Operations")
    cont1 = st.container()
    col1,col2,col3 = cont1.columns(3)
    if col1.button("R"):
        st.session_state.puzzle.right()
    if col1.button("L"):
        st.session_state.puzzle.left()

    if col1.button("U"):
        st.session_state.puzzle.top()
    if col1.button("D"):
        st.session_state.puzzle.bottom()

    if col2.button("HR"):
        st.session_state.puzzle.half_right()
    if col3.button("HR'"):
        st.session_state.puzzle.half_right_inverse()

    if col2.button("HL"):
        st.session_state.puzzle.half_left()
    if col3.button("HL'"):
        st.session_state.puzzle.half_left_inverse()

    if col2.button("HU"):
        st.session_state.puzzle.half_top()
    if col3.button("HU'"):
        st.session_state.puzzle.half_top_inverse()

    if col2.button("HD"):
        st.session_state.puzzle.half_bottom()
    if col3.button("HD'"):
        st.session_state.puzzle.half_bottom_inverse()

    st.markdown("### State Probabilities")
    probabilities = st.session_state.puzzle.prob
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
    1: ['yellow', 'yellow', 'cyan', 'cyan'],  # Quadrant 1 and 2 Yellow
    2: ['cyan', 'cyan', 'yellow', 'yellow'],  # Quadrant 3 and 4 Yellow
    3: ['yellow', 'cyan', 'cyan', 'yellow'],  # Quadrant 1 and 4 Yellow
    4: ['cyan', 'yellow', 'yellow', 'cyan'],  # Quadrant 2 and 3 Yellow
    5: ['yellow', 'cyan', 'yellow', 'cyan'],  # Quadrant 1 and 3 Yellow
    6: ['cyan', 'yellow', 'cyan', 'yellow'],  # Quadrant 2 and 4 Yellow
}

for i in range(6):
    # Fill each quadrant individually using fill()
    axes[i].fill([-1, 0, 0, -1], [-1, -1, 0, 0], color=color_map[i+1][2])  # Quadrant 1
    axes[i].fill([0, 1, 1, 0], [-1, -1, 0, 0], color=color_map[i+1][3])  # Quadrant 2
    axes[i].fill([-1, 0, 0, -1], [0, 0, 1, 1], color=color_map[i+1][1])  # Quadrant 3
    axes[i].fill([0, 1, 1, 0], [0, 0, 1, 1], color=color_map[i+1][0])  # Quadrant 4

    # Plot axis and grid
    axes[i].scatter(np.real(st.session_state.puzzle.state[i]), np.imag(st.session_state.puzzle.state[i]), color="red")
    axes[i].axhline(0, color='black', linewidth=0.5)
    axes[i].axvline(0, color='black', linewidth=0.5)
    axes[i].set_xlim([-1, 1])
    axes[i].set_ylim([-1, 1])
    axes[i].set_title(f"State {i+1}: {round(st.session_state.puzzle.prob[i],2)}")
    axes[i].set_xlabel("Real Part")
    axes[i].set_ylabel("Imaginary Part")
    axes[i].grid()

plt.tight_layout()
st.pyplot(fig)

st.write(f"Score: {round(np.linalg.norm(st.session_state.puzzle.prob),4)}")

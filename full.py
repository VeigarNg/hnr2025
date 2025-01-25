import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random

class State:
    def __init__(self, number_of_state):
        self.num = number_of_state
        self.state = np.identity(number_of_state)[0]
        self.plotter = np.zeros(16)
        self.prob = np.abs(self.state)**2

    def normalize_state(self):
        self.state = self.state / np.linalg.norm(self.state)

    def update_plotter(self):
        re = self.state.real**2
        im = self.state.imag**2
        self.plotter[0] = np.sum(re[[0,2,4]])
        self.plotter[1] = np.sum(re[[1,3,5]])
        self.plotter[2] = np.sum(im[[1,3,5]])
        self.plotter[3] = np.sum(im[[0,2,4]])
        #
        self.plotter[4] = np.sum(im[[0,3,5]])
        self.plotter[5] = np.sum(im[[1,2,4]])
        self.plotter[6] = np.sum(re[[1,2,4]])
        self.plotter[7] = np.sum(re[[0,3,5]])
        #
        self.plotter[8] = np.sum(re[[1,3,4]])
        self.plotter[9] = np.sum(re[[0,2,5]])
        self.plotter[10] = np.sum(im[[0,2,5]])
        self.plotter[11] = np.sum(im[[1,3,4]])
        #
        self.plotter[12] = np.sum(im[[1,2,5]])
        self.plotter[13] = np.sum(im[[0,3,4]])
        self.plotter[14] = np.sum(re[[0,3,4]])
        self.plotter[15] = np.sum(re[[1,2,5]])
        self.plotter = np.around(self.plotter,4)

    def update_prob(self):
        self.prob = np.abs(self.state)**2
        data = {
            "State": [f"State {i + 1}" for i in range(self.num)],
            "Probability": self.prob,
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
        self.update_plotter()
        self.update_prob()

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
        self.update_plotter()
        self.update_prob()

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
        self.update_plotter()
        self.update_prob()

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
        self.update_plotter()
        self.update_prob()

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
        self.update_plotter()
        self.update_prob()

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
        self.update_plotter()
        self.update_prob()

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
        self.update_plotter()
        self.update_prob()

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
        self.update_plotter()
        self.update_prob()

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
        self.update_plotter()
        self.update_prob()

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
        self.update_plotter()
        self.update_prob()

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
        self.update_plotter()
        self.update_prob()

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
        self.update_plotter()
        self.update_prob()

    def scramble_cube(self,scramble):
        k = 0
        sR,sL,sU,sD = lambda:self.right(),lambda:self.left(),lambda:self.top(),lambda:self.bottom()
        hR,hL,hU,hD = lambda:self.half_right(),lambda:self.half_left(),lambda:self.half_top(),lambda:self.half_bottom()

        if scramble == "Easy":
            k = 5
        elif scramble == "Medium":
            k = 10
        else:
            k = 20
            
        operations = [sR,sL,sU,sD,hR,hL,hU,hD]
        for _ in range(k):
            act = random.choice(operations)
            act()

def Menu():
    st.title("Welcome!")
    with st.container(border=True):
        st.header("Rules")
        st.text("Here are the steps to start the game!")
        st.text("1. Press 'Initialize' to initialize the puzzle.")
        st.text("2. Choose a difficulty and press 'Scramble', the computer will scramble the puzzle according to your selected difficulty.")
        st.text("3. Have fun solving!")
        st.header("Guides")
        st.text("In a scrambled puzzle, Yellow and Blue represent the part of the puzzle that is real, while their complementary " +
                "(Purple and Orange, respectively) represent the part of the puzzle that is imaginary. The puzzle itself is actually " +
                "a pie chart, so the proportion represents how much of the color (or state) is mixed inside.")
        st.image("Picture 1.1.png")
        st.text("Here's a picture of the solved state")
        st.image("Picture 1.2.png")
        st.header("References")
        st.text("- Lordi, N., Trank-Greene, M., Kyle, A., Combes, J. (2024). Quantum permutation puzzles with indistinguishable particles. arXiv. "+
                "https://doi.org/10.48550/arXiv.2410.22287")

if 'puzzle' not in st.session_state:
    st.session_state.puzzle = State(6)
    st.session_state.puzzle.update_plotter()

pages = {
    "Main" : [
        st.Page(Menu)
    ],
    "Game": [
        st.Page("game.py",title="Quantum Rubik's Puzzle"),
        st.Page("advanced.py",title="Advanced Visualizer")
    ]
    }

pg = st.navigation(pages)
pg.run()

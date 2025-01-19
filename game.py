import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random as rd

class State:
    def __init__(self, number_of_state):
        self.num = number_of_state
        self.state = np.identity(number_of_state)[0]
        self.plotter = np.zeros(16)

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

st.title("Quantum Rubik's Puzzle")
st.columns(2)
cont_int = st.container(border=False)
col_int = cont_int.columns(2)
cont_act = st.container(border=True)
col_cont1 = cont_act.columns(4)
cont_plot = st.container(border=True)
t = np.arange(0,2*np.pi+0.1,0.1)
x = np.cos(t)
y = np.sin(t)
fig, ax = plt.subplots()
ax.spines["left"].set_position("zero")
ax.spines["top"].set_color("none")
ax.spines["right"].set_color("none")
ax.spines["bottom"].set_position("zero")
ax.set_aspect("equal")
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.plot(x,y,"black")

color = ["yellow","blue","orange","purple"]
if 'pie' not in st.session_state:
    st.session_state.pie = ["none"]*16

if 'puzzle' not in st.session_state:
    st.session_state.puzzle = State(6)

with cont_act:
    if col_cont1[0].button("Left"):
        st.session_state.puzzle.left()
        ax.pie(st.session_state.puzzle.plotter,colors=st.session_state.pie,radius=1,center=(0,0),frame=True)

    if col_cont1[0].button("Half-Left"):
        st.session_state.puzzle.half_left()
        ax.pie(st.session_state.puzzle.plotter,colors=st.session_state.pie,radius=1,center=(0,0),frame=True)
        
    if col_cont1[1].button("Right"):
        st.session_state.puzzle.right()
        ax.pie(st.session_state.puzzle.plotter,colors=st.session_state.pie,radius=1,center=(0,0),frame=True)
        
    if col_cont1[1].button("Half-Right"):
        st.session_state.puzzle.half_right()
        ax.pie(st.session_state.puzzle.plotter,colors=st.session_state.pie,radius=1,center=(0,0),frame=True)
        
    if col_cont1[2].button("Top"):
        st.session_state.puzzle.top()
        ax.pie(st.session_state.puzzle.plotter,colors=st.session_state.pie,radius=1,center=(0,0),frame=True)
        
    if col_cont1[2].button("Half-Top"):
        st.session_state.puzzle.half_top()
        ax.pie(st.session_state.puzzle.plotter,colors=st.session_state.pie,radius=1,center=(0,0),frame=True)
        
    if col_cont1[3].button("Bottom"):
        st.session_state.puzzle.bottom()
        ax.pie(st.session_state.puzzle.plotter,colors=st.session_state.pie,radius=1,center=(0,0),frame=True)

    if col_cont1[3].button("Half-Bottom"):
        st.session_state.puzzle.half_bottom()
        ax.pie(st.session_state.puzzle.plotter,colors=st.session_state.pie,radius=1,center=(0,0),frame=True)

sL = lambda:st.session_state.puzzle.left()
sR = lambda:st.session_state.puzzle.right()
sU = lambda:st.session_state.puzzle.top()
sD = lambda:st.session_state.puzzle.bottom()
hL = lambda:st.session_state.puzzle.half_left()
hR = lambda:st.session_state.puzzle.half_right()
hU = lambda:st.session_state.puzzle.half_top()
hD = lambda:st.session_state.puzzle.half_bottom()
moves = [sL,sR,sU,sD,hL,hR,hU,hD]

scramble = col_int[0].selectbox(
    "Difficulty",
    ("Easy", " Medium", "Hard"),
    )

solved = State(6)
solved.update_plotter()

@st.dialog("Congratulations! You have solved the puzzle!")
def congrats():
    return

if cont_int.button("Intialize",use_container_width=True):
    st.session_state.puzzle = State(6)
    for i in range(0,8):
        if i < 4:
            st.session_state.pie[i] = color[i%4]
            st.session_state.pie[7-i] = color[i%4]  
        else:
            st.session_state.pie[i+4] = color[i%4]
            st.session_state.pie[19-i] = color[i%4]

if col_int[1].button("Scramble",use_container_width=True):
    if scramble == "Easy":
        k = 5
    elif scramble == "Medium":
        k = 10
    else:
        k = 20

    for i in range(k):
        m = rd.choice(moves)
        m()
    ax.pie(st.session_state.puzzle.plotter,colors=st.session_state.pie,radius=1,center=(0,0),frame=True)

if np.array_equal(st.session_state.puzzle.plotter,solved.plotter):
    congrats()

st.pyplot(fig)

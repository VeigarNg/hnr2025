import streamlit as st
import time
import matplotlib.pyplot as plt
import numpy as np

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

st.title("QUANTUM RUBIK'S CUBE")
c1,c2,c3,c4,c5 = st.columns(5)
t = np.arange(0,2*np.pi+0.1,0.1)
x = np.cos(t)
y = np.sin(t)
fig, ax = plt.subplots()
ax.spines["left"].set_position("zero")
ax.spines["top"].set_color("none")
ax.spines["right"].set_color("none")
ax.spines["bottom"].set_position("zero")
ax.set_aspect("equal")
ax.plot(x,y,"black",linestyle="dotted")

color = ["yellow","blue","orange","purple"]
if 'pie' not in st.session_state:
    st.session_state.pie = ["none"]*16

if 'puzzle' not in st.session_state:
    st.session_state.puzzle = State(6)

if 'plo' not in st.session_state:
    st.session_state.plo = ""

def rotate_half_left():
    st.session_state.puzzle.half_left()
    for i in range(4,8):
        st.session_state.pie[i],st.session_state.pie[15-i] = st.session_state.pie[15-i],st.session_state.pie[i]
    ax.pie(st.session_state.puzzle.plotter,colors=st.session_state.pie,radius=1,center=(0,0),frame=True)

def rotate_half_top():
    st.session_state.puzzle.half_top()
    for i in range(0,4):
        st.session_state.pie[i],st.session_state.pie[7-i] = st.session_state.pie[7-i],st.session_state.pie[i]
    ax.pie(st.session_state.puzzle.plotter,colors=st.session_state.pie,radius=1,center=(0,0),frame=True)
    
def rotate_half_bottom():
    st.session_state.puzzle.half_bottom()
    for i in range(8,12):
        st.session_state.pie[i],st.session_state.pie[23-i] = st.session_state.pie[23-i],st.session_state.pie[i]
    ax.pie(st.session_state.puzzle.plotter,colors=st.session_state.pie,radius=1,center=(0,0),frame=True)
    
if c1.button("Intialize"):
    st.session_state.puzzle = State(6)
    st.session_state.puzzle.update_plotter()
    for i in range(0,8):
        if i < 4:
            st.session_state.pie[i] = color[i%4]
            st.session_state.pie[7-i] = color[i%4]
        else:
            st.session_state.pie[i+4] = color[i%4]
            st.session_state.pie[19-i] = color[i%4]
    ax.pie(st.session_state.puzzle.plotter,colors=st.session_state.pie,radius=1,center=(0,0),frame=True)
    st.session_state.plo = ",".join(list(map(str,st.session_state.puzzle.plotter)))
    st.text(st.session_state.plo)

if c2.button("Left"):
    st.session_state.puzzle.left()
    ax.pie(st.session_state.puzzle.plotter,colors=st.session_state.pie,radius=1,center=(0,0),frame=True)
    st.session_state.plo = ",".join(list(map(str,st.session_state.puzzle.plotter)))
    st.text(st.session_state.plo)

if c2.button("Half-Left"):
    rotate_half_left()
    st.session_state.plo = ",".join(list(map(str,st.session_state.puzzle.plotter)))
    st.text(st.session_state.plo)
    
if c3.button("Right"):
    st.session_state.puzzle.right()
    for i in range(0,4):
        st.session_state.pie[i],st.session_state.pie[15-i] = st.session_state.pie[15-i],st.session_state.pie[i]
    ax.pie(st.session_state.puzzle.plotter,colors=st.session_state.pie,radius=1,center=(0,0),frame=True)
    st.text(st.session_state.plo)
    
if c3.button("Half-Right"):
    st.session_state.puzzle.half_right()
    ax.pie(st.session_state.puzzle.plotter,colors=st.session_state.pie,radius=1,center=(0,0),frame=True)
    st.session_state.plo = ",".join(list(map(str,st.session_state.puzzle.plotter)))
    st.text(st.session_state.plo)
    
if c4.button("Top"):
    st.session_state.puzzle.top()
    for i in range(0,4):
        st.session_state.pie[i],st.session_state.pie[7-i] = st.session_state.pie[7-i],st.session_state.pie[i]
    ax.pie(st.session_state.puzzle.plotter,colors=st.session_state.pie,radius=1,center=(0,0),frame=True)
    st.session_state.plo = ",".join(list(map(str,st.session_state.puzzle.plotter)))
    st.text(st.session_state.plo)
    
if c4.button("Half-Top"):
    rotate_half_top()
    st.session_state.plo = ",".join(list(map(str,st.session_state.puzzle.plotter)))
    st.text(st.session_state.plo)
    
if c5.button("Bottom"):
    st.session_state.puzzle.bottom()
    for i in range(8,12):
        st.session_state.pie[i],st.session_state.pie[23-i] = st.session_state.pie[23-i],st.session_state.pie[i]
    ax.pie(st.session_state.puzzle.plotter,colors=st.session_state.pie,radius=1,center=(0,0),frame=True)
    st.session_state.plo = ",".join(list(map(str,st.session_state.puzzle.plotter)))
    st.text(st.session_state.plo)
    
if c5.button("Half-Bottom"):
    rotate_half_bottom()
    st.session_state.plo = ",".join(list(map(str,st.session_state.puzzle.plotter)))
    st.text(st.session_state.plo)
    
st.pyplot(fig)

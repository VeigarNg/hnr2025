import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random as rd
from full import State

st.title("Quantum Rubik's Puzzle")
st.columns(2)
cont_int = st.container(border=False)
col_int = cont_int.columns(2)
cont_act = st.container(border=True)
col_cont1 = cont_act.columns(4)
cont_plot = st.container(border=True)

with cont_act:
    if col_cont1[0].button("Left"):
        st.session_state.puzzle.left()
        
    if col_cont1[0].button("Half-Left"):
        st.session_state.puzzle.half_left()
        
    if col_cont1[1].button("Right"):
        st.session_state.puzzle.right()
        
    if col_cont1[1].button("Half-Right"):
        st.session_state.puzzle.half_right()
        
    if col_cont1[2].button("Top"):
        st.session_state.puzzle.top()
        
    if col_cont1[2].button("Half-Top"):
        st.session_state.puzzle.half_top()
        
    if col_cont1[3].button("Bottom"):
        st.session_state.puzzle.bottom()

    if col_cont1[3].button("Half-Bottom"):
        st.session_state.puzzle.half_bottom()

scramble = col_int[0].selectbox(
    "Difficulty",
    ("Easy", " Medium", "Hard"),
    )

solved = State(6)
solved.update_plotter()

@st.dialog("Congratulations! You have solved the puzzle!")
def congrats():
    return

if 'initial' not in st.session_state:
    st.session_state.initial = True

if cont_int.button("Intialize",use_container_width=True):
    st.session_state.initial = True
    st.session_state.puzzle = State(6)
    st.session_state.puzzle.update_plotter()

if col_int[1].button("Scramble",use_container_width=True):
    st.session_state.initial = False
    st.session_state.puzzle.scramble_cube(scramble)

if not st.session_state.initial:
    if np.array_equal(st.session_state.puzzle.plotter,solved.plotter):
        congrats()

t = np.arange(0,2*np.pi+0.1,0.1)
x = np.cos(t)
y = np.sin(t)
fig, ax = plt.subplots()

color = ["yellow","cyan","darkturquoise","gold"]
pie = ["none"]*16
for i in range(0,8):
    if i < 4:
        pie[i] = color[i%4]
        pie[7-i] = color[i%4]  
    else:
        pie[i+4] = color[i%4]
        pie[19-i] = color[i%4]

ax.spines["left"].set_position("zero")
ax.spines["top"].set_color("none")
ax.spines["right"].set_color("none")
ax.spines["bottom"].set_position("zero")
ax.set_aspect("equal")
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.plot(x,y,"black")
ax.plot([-1,1],[0,0],color="black")
ax.plot([0,0],[-1,1],color="black")
ax.pie(st.session_state.puzzle.plotter,colors=pie,radius=1,center=(0,0))
plot = st.container(border=True,height=5)
plot.pyplot(fig)

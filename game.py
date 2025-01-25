import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random as rd
import pandas as pd
from full import State

st.set_page_config(
        page_title = "Quantum Rubik's Cube",
        page_icon = "Logo.png"
    )
st.title("The Puzzle")
cont_pa = st.container()
col_cont_pa = cont_pa.columns([1,2])
cont_int = col_cont_pa[0].container(border=True)
cont_act = col_cont_pa[0].container(border=True)
cont_plot = col_cont_pa[1].container(border=True)
col_cont1 = cont_act.columns(2)
col_cont2 = cont_act.columns(2)

with cont_act:
    if col_cont1[0].button("L"):
        st.session_state.puzzle.left()
        
    if col_cont1[0].button("HL"):
        st.session_state.puzzle.half_left()

    if col_cont1[0].button("HL'"):
        st.session_state.puzzle.half_left_inverse()
        
    if col_cont1[1].button("R"):
        st.session_state.puzzle.right()
        
    if col_cont1[1].button("HR"):
        st.session_state.puzzle.half_right()

    if col_cont1[1].button("HR'"):
        st.session_state.puzzle.half_right_inverse()
        
    if col_cont2[0].button("U"):
        st.session_state.puzzle.top()
        
    if col_cont2[0].button("HU"):
        st.session_state.puzzle.half_top()

    if col_cont2[0].button("HU'"):
        st.session_state.puzzle.half_top_inverse()
        
    if col_cont2[1].button("D"):
        st.session_state.puzzle.bottom()

    if col_cont2[1].button("HD"):
        st.session_state.puzzle.half_bottom()
    
    if col_cont2[1].button("HD'"):
        st.session_state.puzzle.half_bottom_inverse()

scramble = cont_int.selectbox(
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

if cont_int.button("Scramble",use_container_width=True):
    st.session_state.initial = False
    st.session_state.puzzle = State(6)
    st.session_state.puzzle.update_plotter()
    st.session_state.puzzle.scramble_cube(scramble)

if cont_int.button("Intialize",use_container_width=True):
    st.session_state.initial = True
    st.session_state.puzzle = State(6)
    st.session_state.puzzle.update_plotter()

if not st.session_state.initial:
    if np.array_equal(st.session_state.puzzle.plotter,solved.plotter):
        congrats()

t = np.arange(0,2*np.pi+0.1,0.1)
x = np.cos(t)
y = np.sin(t)
fig, ax = plt.subplots(layout="constrained")

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
plt.tight_layout()
fig.subplots_adjust(
    top = 1,
    bottom = 0.5,
    left = 0.5,
    right = 1
)
cont_plot.pyplot(fig,use_container_width=False)

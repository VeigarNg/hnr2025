import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

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
        st.header("References")
        st.text("- Lordi, N., Trank-Greene, M., Kyle, A., Combes, J. (2024). Quantum permutation puzzles with indistinguishable particles. arXiv. "+
                "https://doi.org/10.48550/arXiv.2410.22287")
    
pages = {
    "Main" : [
        st.Page(Menu)
    ],
    "Game": [
        st.Page("game.py",title="Quantum Rubik's Puzzle"),
        st.Page("streamlit3.py",title="Advanced Visualizer")
    ]
    }

pg = st.navigation(pages)
pg.run()

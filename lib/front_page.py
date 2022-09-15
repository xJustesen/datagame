import streamlit as st


def front_page():
    st.title("Datagames!")
    st.markdown(
        '''
        To get started, pick the game you wan't to play from the sidebar. Your 
        options are:
        - **Guess the Distribution** Can you guess which distribution the samples shown are drawn from?
        - **Guess R-squared?** What is the R-squared value of the straight line fitted to the datapoints?
        Have fun!
        '''
    )

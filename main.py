import streamlit as st

from lib.front_page import front_page
from lib.guess_distribution import guess_distribution
from lib.guess_r_squared import guess_r_squared

# Dictionary where the keys are the page-names and
# the values are functions containing the code to generate
# the page
page_names_to_funcs = {
    "Front Page": front_page,
    "Guess the distribution": guess_distribution,
    "Guess R-squared": guess_r_squared,
}

# Add a drop-down box in the sidebar with a list of pages (front-page + games).
# By default the first item in "page_names_to_funcs" is shown.
selected_page = st.sidebar.selectbox("Select a game", page_names_to_funcs.keys())

# show the selected page
page_names_to_funcs[selected_page]()

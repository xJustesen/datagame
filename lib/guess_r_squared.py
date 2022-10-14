import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import streamlit as st


def guess_r_squared():
    # global vars
    N_SAMPLES = 20

    # function defs
    def get_samples():
        a_ = 2 * np.random.rand() - 1
        b_ = 0
        x_ = 5 * np.random.rand(N_SAMPLES)
        noise = 2.0 * np.random.rand(N_SAMPLES)
        y_ = a_ * x_ + b_ + noise
        return x_, y_, a_, b_

    def fit_curve(x_, y_):
        res = sp.stats.linregress(x_, y_)
        r_squared = res.rvalue**2
        return res.slope, res.intercept, r_squared

    def add_guess(name_: str, guess_: float):
        st.session_state["guesses"].append((name_, guess_))

    # initialise session states
    if "data" not in st.session_state:
        st.session_state["data"] = {
            "x": -100,
            "y": -100,
            "a": -100,
            "b": 0,
            "ahat": -99,
            "bhat": -99,
            "r2": 0,
        }

    if "guesses" not in st.session_state:
        st.session_state["guesses"] = []

    # Page-title and sidebar-header
    st.sidebar.markdown(
        """
            The objective of this game is to guess what the R-squared value of 
            the linear least-squares regression! 
            
            Push the "Generate data!" button to generate 20 (noisy) 
            data-points and a fitted line. Enter your name and guess in the 
            grey-boxes and add them to the table. When all participants 
            have added their guesses push the "Determine Winner" button to,
            you guessed it, determine the winner!
            
            Have fun!
        """
    )
    st.title("Guess R-squared!")

    # On putton press, the following happens:
    #   1) Samples are generated
    #   2) Linear poly is fitted
    #   3) Session-state is updated
    if st.button("Generate data!", key="generate_data"):
        x, y, a, b = get_samples()
        ahat, bhat, r2 = fit_curve(x, y)
        st.session_state["data"]["x"] = x
        st.session_state["data"]["y"] = y
        st.session_state["data"]["a"] = a
        st.session_state["data"]["b"] = b
        st.session_state["data"]["ahat"] = ahat
        st.session_state["data"]["bhat"] = bhat
        st.session_state["data"]["r2"] = r2
        st.session_state["guesses"] = []

    # Display the data and the fitted line
    fig = plt.figure()
    plt.plot(
        st.session_state["data"]["x"], st.session_state["data"]["y"], "o", label="Data"
    )
    plt.plot(
        np.linspace(0, 5),
        st.session_state["data"]["ahat"] * np.linspace(0, 5)
        + st.session_state["data"]["bhat"],
        label="Fit",
    )
    x_offset = 1e-3
    plt.ylim([-8, 8])
    plt.xlim([-x_offset, 5 + x_offset])
    plt.legend(loc="upper right")
    st.pyplot(fig)

    # Allow a user to add a guess (name + number)
    name = st.text_input("Your Name:", value=" ").strip()
    guess = st.number_input("Your guess:", min_value=0.0, max_value=1.0, step=0.001)

    # On button press the state is updated with the new guess
    if st.button("Add guess"):
        add_guess(name, guess)

    # Display the guesses in the current state
    st.table(st.session_state["guesses"])

    # On button press the existing guesses are cleared from the current state
    if st.button("Clear guesses"):
        st.session_state["guesses"] = []

    # On button press the following happens:
    #  1) The fitted paramters and R2 values are displayed, along with the true
    #     values
    #  2) The winner is determined and displayed
    if st.button("Determine winner"):
        # determine best guess
        guesses_arr = np.array(st.session_state["guesses"])
        diffs = [
            abs(x[1] - st.session_state["data"]["r2"])
            for x in st.session_state["guesses"]
        ]
        try:
            best_guess = np.argmin(diffs)
            winner = guesses_arr[best_guess]
        except ValueError:
            winner = ["", ""]

        # Print winning guess
        st.markdown(f"### The winner is: *{winner[0]}*, with a guess of {winner[1]}!")

        # Display fitted and true paramters as well as R2
        st.markdown(
            f"""
        ### Value of R-squared {st.session_state["data"]["r2"]:.2f}

        #### Fitted parameters:
        - Slope: {st.session_state["data"]["ahat"]:.2f}
        - Intercept: {st.session_state["data"]["bhat"]:.2f}

        #### Actual parameters:
        - Slope: {st.session_state["data"]["a"]:.2f}
        - Intercept:  {st.session_state["data"]["b"]:.2f}
        """
        )

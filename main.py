import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.special import gamma
import scipy as sp


def front_page():
    st.title("Datagames!")
    st.markdown(
        '''
        Pick the game you wan't to play from the sidebar. Your options are:
        - **Guess the Distribution** Can you guess which distribution the samples shown are drawn from?
        - **Guess R-squared?** What is the R-squared value of the straight line fitted to the datapoints?
        Good luck!
        '''
    )


def guess_distribution():
    DISTRIBUTIONS = {
        1: ('normal', lambda x: np.random.normal(0, 0.1, x)),
        2: ('Lorentz', np.random.standard_cauchy),
        3: ('power', lambda x: np.random.power(5, x)),
        4: ('uniform', lambda x: np.random.uniform(0, 5, x)),
        5: ('gamma', lambda x: np.random.gamma(2, 2, x))
    }

    np.random.seed(314)

    @st.cache(suppress_st_warning=True)
    def get_samples(sampler, n_samples_, key):
        samples = sampler(n_samples_)
        if key == 2:  # limit samples for better plotting
            samples = samples[(samples > -25) & (samples < 25)]
        return samples


    def get_pdf(key, x):
        if key == 1:
            rv = norm(loc=0, scale=0.1)
            return rv.pdf(x)
        elif key == 2:
            return 1 / (np.pi * (1 + x**2))
        elif key == 3:
            return 5 * np.power(x, 4)
        elif key == 4:
            return [0.20] * len(x)
        elif key == 5:
            return x*np.exp(-x/2)/(4*gamma(2))
        else:
            raise NotImplementedError


    def plot_distribution(samples, plot_pdf):
        fig, ax = plt.subplots()
        _, bins, _ = ax.hist(samples, bins=100, density=True)
        if plot_pdf:
            ax.plot(bins, get_pdf(distribution_key, bins))
        return fig

    st.sidebar.markdown(
        '''
            The objective of this game is to guess which distribution is shown.
            You can increase the number of samples drawn from the distribution
            to increase your chances!
        '''
    )
    st.title('Guess the Distribution!')

    # set input parameters
    # make radio buttons appear horizontal and centered on the page
    st.write(
        '<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center}</style>',
        unsafe_allow_html=True
    )
    distribution_key = st.radio(
        label='Select one of the five secret distributions:',
        options=DISTRIBUTIONS.keys(),
        index=0,
    )
    n_samples = st.slider(
        'Select the number of samples:',
        min_value=100,
        max_value=10000,
        value=100,
        step=100
    )

    # sample distribution
    name, _sampler = DISTRIBUTIONS[distribution_key]
    _samples = get_samples(_sampler, n_samples, distribution_key)

    # get guess and determine if it is correct or not
    guess = st.text_input('Input the name of the distribution you think it is:', value="").strip()
    if guess.lower() == name.lower():
        reveal = True
        st.write(f'Congratulations! You guessed *{guess}* distribution, which is correct!')
    else:
        reveal = False
        if guess == "":
            st.write('Please write a guess in the box above!')
        else:
            st.write(f'You guessed *{guess}* distribution, which is incorrect :(. Please guess again!')

    # plot distribution
    _fig = plot_distribution(_samples, reveal)
    st.pyplot(_fig)


def guess_r_squared():
    # global vars
    N_SAMPLES = 15

    # function defs
    def get_samples():
        a_ = 2 * np.random.rand() - 1
        b_ = 0
        x_ = 5 * np.random.rand(N_SAMPLES)
        noise = 2. * np.random.rand(N_SAMPLES)
        y_ = a_*x_ + b_ + noise
        return x_, y_, a_, b_


    def fit_curve(x_, y_):
        res = sp.stats.linregress(x_, y_)
        return res.slope, res.intercept, res.rvalue**2


    def add_guess(name_: str, guess_: float):
        st.session_state["guesses"].append((name_, guess_))


    # initialise session states
    if "data" not in st.session_state:
        st.session_state["data"] = {
            "x": -100,
            'y': -100,
            "a": -100,
            "b": 0,
            "ahat": -99,
            "bhat": -99,
            "r2": 0
        }

    if "guesses" not in st.session_state:
        st.session_state["guesses"] = []


    # Page-title and sidebar-header
    st.sidebar.markdown(
        '''
            The objective of this game is to guess the value of R-squared of
            the fitted 1st order polynomial! Generating new datapoints will
            clear existing guesses.
        '''
    )
    st.title('Guess R-squared!')


    # On putton press, the following happens:
    #   1) Samples are generated
    #   2) Linear poly is fitted
    #   3) Session-state is updated

    if st.button("Generate data!", key="generate_data"):
        x, y, a, b = get_samples()
        ahat, bhat, r2 = fit_curve(x, y)
        st.session_state["data"]["x"] = x
        st.session_state["data"]['y'] = y
        st.session_state["data"]["a"] = a
        st.session_state["data"]["b"] = b
        st.session_state["data"]["ahat"] = ahat
        st.session_state["data"]["bhat"] = bhat
        st.session_state["data"]["r2"] = r2
        st.session_state["guesses"] = []

    # Display the data and the fitted line
    fig = plt.figure()
    plt.plot(
        st.session_state["data"]["x"],
        st.session_state["data"]['y'],
        'o',
        label="Data"
    )
    plt.plot(
        np.linspace(0, 5),
        st.session_state["data"]["ahat"]*np.linspace(0, 5) + st.session_state["data"]["bhat"],
        label="Fit"
    )
    plt.ylim([-8, 8])
    plt.xlim([-0.25, 5.25])
    plt.legend(loc="upper right")
    st.pyplot(fig)


    # Allow a user to add a guess (name + number)
    name = st.text_input("Your Name:", value=" ").strip()
    guess = st.number_input("Your guess:", min_value=0., max_value=1., step=0.001)

    # On button press the state is updated with the new guess
    if st.button("Add guess"):
        add_guess(name, guess)

    # Display the guesses in the current state
    st.table(st.session_state["guesses"])

    # On button press the following happens:
    #  1) The fitted paramters and R2 values are displayed, along with the true
    #     values
    #  2) The winner is determined and displayed
    if st.button("Determine winner"):
        # Display fitted and true paramters as well as R2
        st.markdown(f'''
        ### Value of R-squared {st.session_state["data"]["r2"]:.2f}

        #### Fitted parameters:
        - Slope: {st.session_state["data"]["ahat"]:.2f}
        - Intercept: {st.session_state["data"]["bhat"]:.2f}

        #### Actual parameters:
        - Slope:{st.session_state["data"]["a"]:.2f}
        - Intercept:  {st.session_state["data"]["b"]:.2f}
        ''')

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
        st.markdown(
            f"### And the winner is: *{winner[0]}*, with a guess of {winner[1]}!"
        )

    # On button press the existing guesses are cleared from the current state
    if st.button("Clear guesses"):
        st.session_state["guesses"] = []


page_names_to_funcs = {
    "Front Page": front_page,
    "Guess the distribution": guess_distribution,
    "Guess R-squared": guess_r_squared,
}
selected_page = st.sidebar.selectbox("Select a game", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

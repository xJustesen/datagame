import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.special import gamma


DISTRIBUTIONS = {
    1: ('normal', lambda x: np.random.normal(0, 0.1, x)),
    2: ('Lorentz', lambda x: np.random.standard_cauchy(x)),
    3: ('power', lambda x: np.random.power(5, x)),
    4: ('uniform', lambda x: np.random.uniform(0, 5, x)),
    5: ('gamma', lambda x: np.random.gamma(2, 2, x))
}

np.random.seed(314)


@st.cache(suppress_st_warning=True)
def get_samples(sampler, n, key):
    s = sampler(n)
    if key == 2:  # limit samples for better plotting
        s = s[(s > -25) & (s < 25)]
    return s


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


st.title('Guess the Distribution!')

# set input parameters
# make radio buttons appear horizontal and centered on the page
st.write(
    '<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center}</style>', unsafe_allow_html=True
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
        st.write(f'Please write a guess in the box above!')
    else:
        st.write(f'You guessed *{guess}* distribution, which is incorrect :(. Please guess again!')

# plot distribution
_fig = plot_distribution(_samples, reveal)
st.pyplot(_fig)

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
    if key == 2:
        _samples = sampler(n)
        _samples = _samples[(_samples > -25) & (_samples < 25)]
        return _samples
    else:
        return sampler(n)


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


def plot_distribution(_samples, _reveal):
    fig, ax = plt.subplots()
    _, bins, _ = ax.hist(_samples, bins=50, density=True)
    if _reveal:
        ax.plot(bins, get_pdf(distribution_key, bins))
    return fig


st.title('Guess the Distribution!')

# set input parameters
distribution_key = st.selectbox(
    'Select a distribution!',
    DISTRIBUTIONS.keys()
)
st.write('You selected distribution: ', distribution_key)
n_samples = st.slider(
    'Select the number of samples:',
    min_value=0,
    max_value=1000,
    value=0,
    step=100
)
st.write(f'You selected {n_samples} number of samples')

# sample distribution
name, _sampler = DISTRIBUTIONS[distribution_key]
samples = get_samples(_sampler, n_samples, distribution_key)

# reveal answer
reveal = st.checkbox('Reveal Distribution?')
if reveal:
    st.write('It was a '+name+' distribution!')

fig = plot_distribution(samples, reveal)
st.pyplot(fig)

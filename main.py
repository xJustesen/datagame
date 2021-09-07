import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title('Guess the Distribution!')

# set input parameters
distributions = {
    1: ('normal', lambda x: np.random.normal(0, 0.1, x)),
    2: ('poisson', lambda x: np.random.poisson(50, x)),
    3: ('power', lambda x: np.random.power(5, x)),
    4: ('uniform', lambda x: np.random.uniform(0, 5, x)),
    5: ('gamma', lambda x: np.random.gamma(2, 2, x))
}

distribution_key = st.selectbox(
    'Select a distribution!',
    distributions.keys()
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
name, sampler = distributions[distribution_key]
samples = sampler(n_samples)

# plot the samples
fig = plt.figure()
plt.hist(samples, bins=30, density=True)
st.pyplot(fig)

# reveal answer
reveal = st.checkbox('Reveal Distribution?')
if reveal:
    st.write('It was a '+name+' distribution!')

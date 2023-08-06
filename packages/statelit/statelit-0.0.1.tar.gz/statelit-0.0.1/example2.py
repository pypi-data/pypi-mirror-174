# Requires `pip install matplotlib numpy`
from pydantic import BaseModel
from statelit import StateManager
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


class AppState(BaseModel):
    seed: int = 372193
    size: int = 10_000
    mu: float = 5.0
    sigma: float = 5.0
    log: bool = False


state_manager = StateManager(AppState)

with st.expander("State"):
    state = state_manager.form()

np.random.seed(state.seed)

arr = np.random.normal(state.mu, state.sigma, size=state.size)

if state.log:
    arr = np.log(arr)

fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)

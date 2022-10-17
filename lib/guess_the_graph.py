import plotly.graph_objects as go
import streamlit as st
from copy import deepcopy
import numpy as np

PROPERTIES = {
    "xlabel": "",
    "ylabel": "",
    "xticks": [],
    "yticks": [],
    "trace": go.Scatter(),
    "title": ""
}


class Figure:

    def __init__(self, **kwargs):
        for prop in PROPERTIES:
            if prop not in kwargs:
                kwargs[prop] = PROPERTIES[prop]

        # set figure properties
        self.xlabel = kwargs["xlabel"]
        self.ylabel = kwargs["ylabel"]
        self.xticks = kwargs["xticks"]
        self.yticks = kwargs["yticks"]
        self.trace = kwargs["trace"]
        self.title = kwargs["title"]

        # create empty figure object
        self.figure = go.Figure()
        self.figure.update_layout(
            xaxis={"showticklabels": False},
            yaxis={"showticklabels": False}
        )

    def add_title(self):
        self.figure.update_layout(title_text=self.title)

    def add_trace(self):
        self.figure.add_trace(self.trace)

    def add_xlabel(self):
        self.figure.update_layout(xaxis_title=self.xlabel)

    def add_ylabel(self):
        self.figure.update_layout(yaxis_title=self.ylabel)

    def add_xticks(self):
        self.figure.update_layout(
            xaxis={
                "tickmode": "array",
                "tickvals": [x[1] for x in self.xticks],
                "ticktext": [x[0] for x in self.xticks],
                "showticklabels": True
            }
        )

    def get_plotly_chart(self):
        return self.figure

    def add_yticks(self):
        self.figure.update_layout(
            yaxis={
                "tickmode": "array",
                "tickvals": [y[1] for y in self.yticks],
                "ticktext": [y[0] for y in self.yticks],
                "showticklabels": True
            }
        )


FIGURES = [
    Figure(
        xlabel="Bank",
        ylabel="DKK",
        xticks=[
            ("Danske Bank", 0),
            ("Sydbank", 1),
            ("Nordea", 2),
            ("Vestjysk Bank", 3),
            ("Lunar", 4),
        ],
        yticks=[(0, 0), (2500, 2500), (5000, 5000)],
        trace=go.Bar(x=[0, 1, 2, 3, 4], y=[4000, 3895, 4800, 5000, 0.0]),
        title="Business Account Origination Fee"
    ),
    Figure(
        xlabel="Time",
        ylabel="Percentage of Questioned (%)",
        xticks=[
            ("Juni '21", 0),
            ("Sep '21", 1),
            ("Dec '21", 2),
            ("Mar '22", 3),
        ],
        yticks=[("1%", 1), ("2%", 2), ("3%", 3), ("4%", 4)],
        trace=go.Scatter(
            x=[0, 1, 2, 3], y=[1.2, 1.75, 2.25, 3.5],
        ),
        title="Organic Knowledge of Lunar Bank (Voxmeter)"
    ),
    Figure(
        xlabel="Country",
        ylabel="Count",
        xticks=[("Denmark", 0), ("Sweden", 1)],
        yticks=[(str(x), x) for x in np.arange(0, 12, 1)],
        trace=go.Bar(
            x=[0, 1], y=[7, 11],
            marker_color=["rgb(200, 16, 46)", "rgb(0, 106, 167)"]
        ),
        title="Win Record in Dano-Swedish Wars since 1523"
    )
]

EMPTY_FIGURE = Figure()


def update_figure_state(figure_index):
    st.session_state["figure"] = deepcopy(FIGURES[figure_index])
    st.session_state["reveal_order"] = [
        st.session_state["figure"].add_trace,
        st.session_state["figure"].add_xlabel,
        st.session_state["figure"].add_ylabel,
        st.session_state["figure"].add_xticks,
        st.session_state["figure"].add_yticks,
        st.session_state["figure"].add_title
    ]
    st.session_state["reveal_index"] = 0
    st.session_state["n_reveals"] = len(st.session_state["reveal_order"])


def reset_state():
    for prop in st.session_state.keys():
        del st.session_state[prop]


def guess_the_graph():
    st.title("Guess the Figure!")
    st.markdown("""
      Given the information available can you guess what the figure is showing?
    """)
    st.write(
        "<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center}</style>",
        unsafe_allow_html=True,
    )
    figure_index = st.radio(
        label="Select a figure", options=list(range(len(FIGURES))), index=0,
        on_change=reset_state
    )

    if "figure" not in st.session_state:
        update_figure_state(figure_index)

    if st.button("Reveal property"):
        if st.session_state["reveal_index"] >= st.session_state["n_reveals"]:
            st.markdown("No more properties to display")
        else:
            index_ = st.session_state["reveal_index"]
            reveal_func = st.session_state["reveal_order"][index_]
            reveal_func()
            st.session_state["reveal_index"] += 1
        fig_ = st.session_state["figure"].get_plotly_chart()
    else:
        fig_ = EMPTY_FIGURE.get_plotly_chart()

    st.plotly_chart(fig_)

    if st.button("Reset State"):
        reset_state()

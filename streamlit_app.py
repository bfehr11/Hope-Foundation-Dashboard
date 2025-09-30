import streamlit as st
import pandas as pd

def home():
    st.title("Hope Foundation Dashboard")

pages = {
    "The Hope Foundation": [
        st.Page("home.py", title="Home")
    ],
    "Applications": [
        st.Page("ready_for_review.py", title="What applications are ready for review?"),
    ],
    "Our Support": [
        st.Page("support_stats.py", title="How much support do we give?"),
        st.Page("request_acceptance.py", title="How long does it take for us to send support?"),
    ],
    "Grant Usage": [
        st.Page("grant_usage.py", title="How many patients still have a balance on their grant?")
    ], 
    "Our Past Year": [
        st.Page("past_year_stats.py", title="What impact have we made in the past year?")
    ]
}

pg = st.navigation(pages, position="top")
pg.run()

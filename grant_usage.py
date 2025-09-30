import streamlit as st
import pandas as pd
import numpy as np

# read in data
data = pd.read_excel("UNO Service Learning Data Sheet De-Identified Version.xlsx")
data = data[data['Remaining Balance'] > 0] 

st.title("What patients still have a balance?")

filter = st.sidebar.radio("Application Year __",
                 np.sort(data['App Year'].unique()))

print(data.columns)
data = data[data['App Year'] == filter][['Patient ID#', 'Remaining Balance']]
total_balance = data['Remaining Balance'].sum()
st.write(f'{len(data)} patient(s) have a remaining balance totaling ${total_balance}')

st.dataframe(data, hide_index=True, 
    column_config = {
        "Remaining Balance": st.column_config.NumberColumn(format="$%.2f")
})


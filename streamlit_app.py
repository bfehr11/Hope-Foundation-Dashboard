import streamlit as st
import pandas as pd

# read in data
data = pd.read_excel("UNO Service Learning Data Sheet De-Identified Version.xlsx")

# filter the data for only rows where there is no Reason and Request Status is "Pending"
page1_data = data[data['Reason - Pending/No'].isna()]
page1_data = page1_data[page1_data['Request Status'] == 'Pending'][['Patient ID#', 'Grant Req Date', 'Application Signed?']] # Filter out columns so that only necessary information will be visible
page1_data['Application Signed?'] = "No" # All of the remaining rows have NaN as their Application Signed? value so replace it NaN with something readable

st.title("Applications Ready to be Reviewed")
st.dataframe(page1_data)

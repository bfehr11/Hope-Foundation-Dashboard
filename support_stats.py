import streamlit as st
import pandas as pd

# read in data
data = pd.read_excel("UNO Service Learning Data Sheet De-Identified Version.xlsx")

st.title("How much support do we give if ...?")

data = data[data['Request Status'] == "Approved"]
data['Amount'] = pd.to_numeric(data['Amount'], errors="coerce")

filter = st.sidebar.radio("Filter by",
                 ("You live in ...", "Your gender is ...", "Your income is ...", "You have _____ insurance", "Your age is ..."))

if filter == "You live in ...":
    data['Pt City'] = data['Pt City'].str.upper()
    data['Pt State'] = data['Pt State'].str.upper()
    data = data.groupby(["Pt City", "Pt State"])['Amount'].mean().reset_index()
    data = data.rename(columns={'Amount': 'Average Support Given'})
elif filter == "Your gender is ...":
    for i in range(len(data)):
        if data.iloc[i, data.columns.get_loc("Gender")] == "Transgender Female":
            data.iloc[i, data.columns.get_loc("Gender")] = "Female"
    data['Gender'] = data['Gender'].str.capitalize()
    data = data[(data['Gender'] == "Male") | (data['Gender'] == "Female")]
    data = data.groupby("Gender")['Amount'].mean().reset_index()
    data = data.rename(columns={'Amount': 'Average Support Given'})
elif filter=="Your income is ...":
    data['Total Household Gross Monthly Income'] = pd.to_numeric(data['Total Household Gross Monthly Income'], errors="coerce")
    data['Total Household Gross Monthly Income'] = data['Total Household Gross Monthly Income'] * 12
    temp = pd.DataFrame(columns=['Income Bracket', 'Average Support Given'])
    temp.loc[len(temp)] = ['$0-$60,0000', data[data['Total Household Gross Monthly Income'] <= 60000]['Amount'].mean()]
    temp.loc[len(temp)] = ['$60,000-$100,000', data[(data['Total Household Gross Monthly Income'] <= 100000) & (data['Total Household Gross Monthly Income'] > 60000)]['Amount'].mean()]
    temp.loc[len(temp)] = ['$100,000-$200,000', data[(data['Total Household Gross Monthly Income'] <= 200000) & (data['Total Household Gross Monthly Income'] > 100000)]['Amount'].mean()]
    temp.loc[len(temp)] = ['$200,000-$300,000', data[(data['Total Household Gross Monthly Income'] <= 300000) & (data['Total Household Gross Monthly Income'] > 200000)]['Amount'].mean()]
    temp.loc[len(temp)] = ['$300,000+', data[data['Total Household Gross Monthly Income'] > 300000]['Amount'].mean()]
    temp['Average Support Given'] = temp['Average Support Given'].map("${:.2f}".format)
    data = temp

st.dataframe(data, hide_index=True, 
    column_config = {
        "Average Support Given": st.column_config.NumberColumn(format="$%.2f")
})
import streamlit as st
import pandas as pd

def get_location_stats(data):
    data['Pt City'] = data['Pt City'].str.upper()
    data['Pt State'] = data['Pt State'].str.upper()
    data = data.groupby(["Pt City", "Pt State"])['Amount'].mean().reset_index()
    return data.rename(columns={'Amount': 'Average Support Given'})

def get_gender_stats(data):
    for i in range(len(data)):
        if data.iloc[i, data.columns.get_loc("Gender")] == "Transgender Female":
            data.iloc[i, data.columns.get_loc("Gender")] = "Female"
    data['Gender'] = data['Gender'].str.capitalize()
    data = data[(data['Gender'] == "Male") | (data['Gender'] == "Female")]
    data = data.groupby("Gender")['Amount'].mean().reset_index()
    return data.rename(columns={'Amount': 'Average Support Given'})

def get_income_stats(data):
    data['Total Household Gross Monthly Income'] = pd.to_numeric(data['Total Household Gross Monthly Income'], errors="coerce")
    data['Total Household Gross Monthly Income'] = data['Total Household Gross Monthly Income'] * 12
    temp = pd.DataFrame(columns=['Income Bracket', 'Average Support Given'])
    temp.loc[len(temp)] = ['$0-$60,0000', data[data['Total Household Gross Monthly Income'] <= 60000]['Amount'].mean()]
    temp.loc[len(temp)] = ['$60,000-$100,000', data[(data['Total Household Gross Monthly Income'] <= 100000) & (data['Total Household Gross Monthly Income'] > 60000)]['Amount'].mean()]
    temp.loc[len(temp)] = ['$100,000-$200,000', data[(data['Total Household Gross Monthly Income'] <= 200000) & (data['Total Household Gross Monthly Income'] > 100000)]['Amount'].mean()]
    temp.loc[len(temp)] = ['$200,000-$300,000', data[(data['Total Household Gross Monthly Income'] <= 300000) & (data['Total Household Gross Monthly Income'] > 200000)]['Amount'].mean()]
    temp.loc[len(temp)] = ['$300,000+', data[data['Total Household Gross Monthly Income'] > 300000]['Amount'].mean()]
    temp['Average Support Given'] = temp['Average Support Given'].map("${:.2f}".format)
    return temp

def get_insurance_stats(data):
    data['Insurance Type'] = data['Insurance Type'].str.title().str.strip()
    for i in range(len(data)):
        if data.iloc[i, data.columns.get_loc("Insurance Type")] == "Uninsurred":
            data.iloc[i, data.columns.get_loc("Insurance Type")] = "Uninsured"
        if data.iloc[i, data.columns.get_loc("Insurance Type")] == "Unisured":
            data.iloc[i, data.columns.get_loc("Insurance Type")] = "Uninsured"
    data = data[(data['Insurance Type'] != "Missing") & (data['Insurance Type'] != 'Unknown')]
    data = data.groupby(["Insurance Type"])['Amount'].mean().reset_index()
    return data.rename(columns={'Amount': 'Average Support Given'})

def get_age_stats(data):
    data['DOB'] = pd.to_datetime(data['DOB'], errors="coerce")
    data['Age'] = pd.Timestamp.now().year - data['DOB'].dt.year
    data = data[data['Age'] > -1]
    temp = pd.DataFrame(columns=['Age', 'Average Support Given'])
    temp.loc[len(temp)] = ['0-9', data[data['Age'] <= 9]['Amount'].mean()]
    temp.loc[len(temp)] = ['10-19', data[(data['Age'] <= 19) | (data['Age'] >= 10)]['Amount'].mean()]
    temp.loc[len(temp)] = ['20-29', data[(data['Age'] <= 29) | (data['Age'] >= 20)]['Amount'].mean()]
    temp.loc[len(temp)] = ['30-39', data[(data['Age'] <= 39) | (data['Age'] >= 30)]['Amount'].mean()]
    temp.loc[len(temp)] = ['40-49', data[(data['Age'] <= 49) | (data['Age'] >= 40)]['Amount'].mean()]
    temp.loc[len(temp)] = ['50-59', data[(data['Age'] <= 59) | (data['Age'] >= 50)]['Amount'].mean()]
    temp.loc[len(temp)] = ['60-69', data[(data['Age'] <= 69) | (data['Age'] >= 60)]['Amount'].mean()]
    temp.loc[len(temp)] = ['70-79', data[(data['Age'] <= 79) | (data['Age'] >= 70)]['Amount'].mean()]
    temp.loc[len(temp)] = ['80-89', data[(data['Age'] <= 89) | (data['Age'] >= 80)]['Amount'].mean()]
    temp.loc[len(temp)] = ['90+', data[data['Age'] >= 90]['Amount'].mean()]
    return temp

def get_expenses_stats(data):
    data['Type of Assistance (CLASS)'] = data['Type of Assistance (CLASS)'].str.title().str.strip()
    data = data[(data['Type of Assistance (CLASS)'] != "Other") & (data['Type of Assistance (CLASS)'] != 'Multiple')]
    data = data.groupby(["Type of Assistance (CLASS)"])['Amount'].mean().reset_index()
    return data.rename(columns={'Amount': 'Average Support Given'})

# read in data
data = pd.read_excel("UNO Service Learning Data Sheet De-Identified Version.xlsx")

st.title("How much support do we give if ...?")

data = data[data['Request Status'] == "Approved"]
data['Amount'] = pd.to_numeric(data['Amount'], errors="coerce")

filter = st.sidebar.radio("Filter by",
                 ("You live in ...", "Your gender is ...", "Your income is ..."
                  , "You have _____ insurance", "Your age is ...", "You have _____ to pay for"))

if filter == "You live in ...":
    data = get_location_stats(data)
elif filter == "Your gender is ...":
    data = get_gender_stats(data)
elif filter=="Your income is ...":
    data = get_income_stats(data)
elif filter=="You have _____ insurance":
    data = get_insurance_stats(data)
elif filter=="Your age is ...":
    data = get_age_stats(data)
elif filter=="You have _____ to pay for":
    data = get_expenses_stats(data)

st.dataframe(data, hide_index=True, 
    column_config = {
        "Average Support Given": st.column_config.NumberColumn(format="$%.2f")
})
import streamlit as st
import pandas as pd

def get_location_stats(data):
    data['Pt City'] = data['Pt City'].str.upper()
    data['Pt State'] = data['Pt State'].str.upper()
    data = data.groupby(["Pt City", "Pt State"])['Length of Waiting Period'].mean().reset_index()
    return data.rename(columns={'Length of Waiting Period': 'Average Length of Waiting Period'})

def get_gender_stats(data):
    for i in range(len(data)):
        if data.iloc[i, data.columns.get_loc("Gender")] == "Transgender Female":
            data.iloc[i, data.columns.get_loc("Gender")] = "Female"
    data['Gender'] = data['Gender'].str.capitalize()
    data = data[(data['Gender'] == "Male") | (data['Gender'] == "Female")]
    data = data.groupby("Gender")['Length of Waiting Period'].mean().reset_index()
    return data.rename(columns={'Length of Waiting Period': 'Average Length of Waiting Period'})

def get_income_stats(data):
    data['Total Household Gross Monthly Income'] = pd.to_numeric(data['Total Household Gross Monthly Income'], errors="coerce")
    data['Total Household Gross Monthly Income'] = data['Total Household Gross Monthly Income'] * 12
    temp = pd.DataFrame(columns=['Income Bracket', 'Average Length of Waiting Period'])
    temp.loc[len(temp)] = ['$0-$60,0000', data[data['Total Household Gross Monthly Income'] <= 60000]['Length of Waiting Period'].mean()]
    temp.loc[len(temp)] = ['$60,000-$100,000', data[(data['Total Household Gross Monthly Income'] <= 100000) & (data['Total Household Gross Monthly Income'] > 60000)]['Length of Waiting Period'].mean()]
    temp.loc[len(temp)] = ['$100,000-$200,000', data[(data['Total Household Gross Monthly Income'] <= 200000) & (data['Total Household Gross Monthly Income'] > 100000)]['Length of Waiting Period'].mean()]
    temp.loc[len(temp)] = ['$200,000-$300,000', data[(data['Total Household Gross Monthly Income'] <= 300000) & (data['Total Household Gross Monthly Income'] > 200000)]['Length of Waiting Period'].mean()]
    temp.loc[len(temp)] = ['$300,000+', data[data['Total Household Gross Monthly Income'] > 300000]['Length of Waiting Period'].mean()]
    print(temp['Average Length of Waiting Period'])
    return temp

def get_insurance_stats(data):
    data['Insurance Type'] = data['Insurance Type'].str.title().str.strip()
    for i in range(len(data)):
        if data.iloc[i, data.columns.get_loc("Insurance Type")] == "Uninsurred":
            data.iloc[i, data.columns.get_loc("Insurance Type")] = "Uninsured"
        if data.iloc[i, data.columns.get_loc("Insurance Type")] == "Unisured":
            data.iloc[i, data.columns.get_loc("Insurance Type")] = "Uninsured"
    data = data[(data['Insurance Type'] != "Missing") & (data['Insurance Type'] != 'Unknown')]
    data = data.groupby(["Insurance Type"])['Length of Waiting Period'].mean().reset_index()
    return data.rename(columns={'Length of Waiting Period': 'Average Length of Waiting Period'})

def get_age_stats(data):
    data['DOB'] = pd.to_datetime(data['DOB'], errors="coerce")
    data['Age'] = pd.Timestamp.now().year - data['DOB'].dt.year
    data = data[data['Age'] > -1]
    temp = pd.DataFrame(columns=['Age', 'Average Length of Waiting Period'])
    temp.loc[len(temp)] = ['0-9', data[data['Age'] <= 9]['Length of Waiting Period'].mean()]
    temp.loc[len(temp)] = ['10-19', data[(data['Age'] <= 19) | (data['Age'] >= 10)]['Length of Waiting Period'].mean()]
    temp.loc[len(temp)] = ['20-29', data[(data['Age'] <= 29) | (data['Age'] >= 20)]['Length of Waiting Period'].mean()]
    temp.loc[len(temp)] = ['30-39', data[(data['Age'] <= 39) | (data['Age'] >= 30)]['Length of Waiting Period'].mean()]
    temp.loc[len(temp)] = ['40-49', data[(data['Age'] <= 49) | (data['Age'] >= 40)]['Length of Waiting Period'].mean()]
    temp.loc[len(temp)] = ['50-59', data[(data['Age'] <= 59) | (data['Age'] >= 50)]['Length of Waiting Period'].mean()]
    temp.loc[len(temp)] = ['60-69', data[(data['Age'] <= 69) | (data['Age'] >= 60)]['Length of Waiting Period'].mean()]
    temp.loc[len(temp)] = ['70-79', data[(data['Age'] <= 79) | (data['Age'] >= 70)]['Length of Waiting Period'].mean()]
    temp.loc[len(temp)] = ['80-89', data[(data['Age'] <= 89) | (data['Age'] >= 80)]['Length of Waiting Period'].mean()]
    temp.loc[len(temp)] = ['90+', data[data['Age'] >= 90]['Length of Waiting Period'].mean()]
    return temp

def get_expenses_stats(data):
    data['Type of Assistance (CLASS)'] = data['Type of Assistance (CLASS)'].str.title().str.strip()
    data = data[(data['Type of Assistance (CLASS)'] != "Other") & (data['Type of Assistance (CLASS)'] != 'Multiple')]
    data = data.groupby(["Type of Assistance (CLASS)"])['Length of Waiting Period'].mean().reset_index()
    return data.rename(columns={'Length of Waiting Period': 'Average Length of Waiting Period'})

# read in data
data = pd.read_excel("UNO Service Learning Data Sheet De-Identified Version.xlsx")
data['Grant Req Date'] = pd.to_datetime(data['Grant Req Date'], errors="coerce")
data['Payment Submitted?'] = pd.to_datetime(data['Payment Submitted?'], errors="coerce")
data = data[data[["Grant Req Date", "Payment Submitted?"]].notna().all(axis=1)]
data['Length of Waiting Period'] = (data['Payment Submitted?'] - data['Grant Req Date']).dt.days

st.title("How long does it take to receive support if ...")

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
        "Average Length of Waiting Period": st.column_config.NumberColumn(format="%d days")
})
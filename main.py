import streamlit as st
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from PIL import Image


# @st.cache
# def load_data_from_csv() -> pd.DataFrame:
#     df = pd.read_csv('Sleep_health_and_lifestyle_dataset.csv', index_col='Person ID')
#     return df

data = pd.read_csv('Sleep_health_and_lifestyle_dataset.csv', index_col='Person ID')
data["BMI Category"].replace(['Normal Weight'], ['Normal'], inplace=True)

# ---------SIDEBAR-START---------

st.sidebar.title("Options")
sex = st.sidebar.radio("Choose male/female", ['All', 'Male', 'Female'])
st.sidebar.title("Choose profession")

nurse = st.sidebar.checkbox("Nurse")
doctor = st.sidebar.checkbox("Doctor")
engineer = st.sidebar.checkbox("Engineer")
lawyer = st.sidebar.checkbox("Lawyer")
teacher = st.sidebar.checkbox("Teacher")
accountant = st.sidebar.checkbox("Accountant")
salesp = st.sidebar.checkbox("Sales Person")

if len(data) > 0:
    num = st.sidebar.slider("Choose number of people", 1, len(data), len(data))
else:
    num = 0

if sex == 'Male':
    sorted_data = data[data['Gender'] == 'Male']
elif sex == 'Female':
    sorted_data = data[data['Gender'] == 'Female']
else:
    sorted_data = data

selected_occupations = []
if nurse:
    selected_occupations.append('Nurse')
if doctor:
    selected_occupations.append('Doctor')
if engineer:
    selected_occupations.append('Engineer')
if lawyer:
    selected_occupations.append('Lawyer')
if teacher:
    selected_occupations.append('Teacher')
if accountant:
    selected_occupations.append('Accountant')
if salesp:
    selected_occupations.append('Sales Person')

if selected_occupations:
    sorted_data = sorted_data[sorted_data['Occupation'].isin(selected_occupations)]

# -----------SIDEBAR-END--------------


st.markdown("## Sleep insights")
image = Image.open('dataset-cover.jpg')
st.image(image)

# Deviding into 2 columns
col1, col2 = st.columns((1, 1))

col1.write(sorted_data.head(num))

bmi_counts = data["BMI Category"].value_counts()

fig1 = plt.figure()
plt.bar(bmi_counts.index, bmi_counts.values)
plt.xlabel("BMI Category")
plt.ylabel("Counts")
plt.title("Distribution of BMI Categories")
plt.xticks(rotation=45)
col1.pyplot(fig1)

prof_counts = data["Occupation"].value_counts().sort_values(ascending=False)
prof_counts = prof_counts[prof_counts > 30]

fig2 = plt.figure()
plt.bar(prof_counts.index, prof_counts.values)
plt.xlabel("Occupation")
plt.ylabel("Counts")
plt.title("Distribution of professions")
plt.xticks(rotation=45)
caption = "There are lots of nurses, doctors and engineers."
plt.figtext(0.5, -0.2, caption, wrap=True, horizontalalignment='center', fontsize=10)
col2.pyplot(fig2)

fig3 = plt.figure()
data_new = data[data['Sleep Disorder'] != "None"]
sorted_prof = data["Occupation"].value_counts()
plt.bar(sorted_prof.index, sorted_prof.values)
plt.xlabel("Professions")
plt.ylabel("Sleep disorders")
plt.title("Distribution of sleep disorders")
plt.xticks(rotation=45)
col2.pyplot(fig3)

fig, ax = plt.subplots()
data_numerized = data
for col_name in data_numerized.columns:
    if data_numerized[col_name].dtype == 'object':
        data_numerized[col_name] = data_numerized[col_name].astype('category')
        data_numerized[col_name] = data_numerized[col_name].cat.codes

correlation_matr = data_numerized.corr(method='pearson')
high_correlation = correlation_matr[(correlation_matr > 0.5) & (correlation_matr < 1)]
st.title('Correlation Matrix Heatmap')
st.write('Correlations greater than 0.5 using Pearson method')
sns.heatmap(high_correlation, annot=True, ax=ax)
ax.set_title('Correlation matrix for correlations > 0.5')
caption = "You'll see that 'Sleep disorder' positively correlated with 'BMI' and 'Blood preasure'. So you better walk " \
          "more :)"
st.caption(caption)
st.pyplot(fig)

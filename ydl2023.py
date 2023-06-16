import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import seaborn as sns
tips = sns.load_dataset("tips")


@st.cache
def load_data_from_excel() -> pd.DataFrame:
    df = pd.read_excel("data.xlsx")
    return df

# -------------- SIDE BAR BEGIN

st.sidebar.title("YDL 2023 Sidebar!")
st.sidebar.write("Filters")

smokers = st.sidebar.checkbox("Smokers only")

a = st.sidebar.radio("Choose one two three", [1, 2, 3], index=2)
print(a, type(a))

sb = st.sidebar.selectbox("Select something", ["Almaty", "Astana", "Karagandy"])
print(sb, type(sb))

tips_choice = list(tips["time"].unique())
time_choice = st.sidebar.multiselect("Time", tips_choice, tips_choice)
print(time_choice, type(time_choice))

tips = tips[tips["time"].isin(time_choice)]

if smokers:
    tips = tips[tips["smoker"] == "Yes"]


if len(tips) > 0:
    st.sidebar.header("Sliders!")
    top_n = st.sidebar.slider("Top n", 1, len(tips), len(tips))
else:
    top_n = 0

# -------------- SIDE BAR END

st.markdown("## Hello YDL $20^{23}$!")

st.code(f"""
tips_choice = list(tips["time"].unique())
time_choice = st.sidebar.multiselect("Time", tips_choice, tips_choice)
print(time_choice, type(time_choice))

tips = tips[tips["time"].isin(time_choice)]

if smokers:
    tips = tips[tips["smoker"] == "Yes"]


if len(tips) > 0:
    st.sidebar.header("Sliders!")
    top_n = st.sidebar.slider("Top n", 1, len(tips), len(tips))
else:
    top_n = 0
""", language='python')

st.markdown("---")

st.line_chart(tips["total_bill"])

fig = plt.figure()
a = sns.barplot(data=tips, x="day", y="total_bill")
#plt.bar([1,2,3], height=3)
st.pyplot(fig)

fig = plt.figure()
sns.scatterplot(x="total_bill", y="tip", hue="smoker", data=tips)
st.pyplot(fig)

st.markdown("---")

col1, col2 = st.columns((2,1))

if smokers:
    col2.write("Smokers only!")

if sb != "Karagandy":
    col1.write(tips.head(top_n))

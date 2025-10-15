import streamlit as st
import pandas as pd
import json 

with open("data.json" , "r" , encoding="utf-8") as f:
    jobs = json.load(f)

df = pd.DataFrame(jobs)

df["job_id"] = df["link"].astype(str).str.extract(r"jk=([a-zA-Z0-9]+)")

df["link"] = "https://www.indeed.com/viewjob?jk=" + df["job_id"]

st.title("job Listining Dashboard")
st.sidebar.header("filter job")
keyword = st.sidebar.text_input("search by key word")
location = st.sidebar.text_input("filter by location")
filtered = df.copy()

if keyword :
    filtered =   filtered[filtered['title'].str.contains(keyword,   case= False ,  na= False)]
if location: 
    filtered =   filtered[filtered['location'].str.contains(location , case= False,  na = False)]
st.write(f'### Total job found : {len(filtered)}')
st.dataframe(filtered)

st.write("open job Link:")
for _,  row in filtered.iterrows():
    st.markdown(f'{row["title"] }, {row["location"]}, {row["link"]},  {row["company"]}')
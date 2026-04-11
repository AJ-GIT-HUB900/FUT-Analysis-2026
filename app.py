import streamlit as st
import pandas as pd

# 1. Set up the page
st.set_page_config(page_title="FUT 26 Market Dashboard", layout="centered")

# 2. Add a Title and some text
st.title("📈 FUT 26 Market Dashboard")
st.write("Welcome to your personal EA FC Ultimate Team market tracker!")

# 3. Load our existing Mbappe CSV file
try:
    # Read the data just like we did in our analyzer script
    df = pd.read_csv('mbappe_prices.csv')
    df['date'] = pd.to_datetime(df['date'])
    
    st.subheader("Kylian Mbappé - Price History")
    
    # 4. DRAW THE CHART! Streamlit does this in exactly one line of code:
    st.line_chart(data=df, x='date', y='price')
    
    # 5. Add a dropdown to look at the raw numbers
    with st.expander("View Raw Data"):
        st.dataframe(df)

except FileNotFoundError:
    st.error("Uh oh! Could not find mbappe_prices.csv. Make sure it is in the same folder.")

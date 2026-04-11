import streamlit as st
import pandas as pd
import base64

# 1. Page Setup
st.set_page_config(page_title="EA FC 26 Player Database", layout="wide")
def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read())
    
    # This injects custom CSS to set the wallpaper
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

try:
    # Trigger the background function! (Make sure the filename matches)
    add_bg_from_local('background.jpg')
except FileNotFoundError:
    st.warning("Could not find background.jpg, using default theme.")

st.title("⚽ EA FC 26 Player Database")

# 2. Load Your Exact CSV
@st.cache_data
def load_data():
    # Make sure your file is named EXACTLY this (case-sensitive!)
    df = pd.read_csv('EAFC26-Men.csv') 
    return df

try:
    df = load_data()

    st.sidebar.header("Filter Players")
    
    # 3. Create the Filters based on your ACTUAL columns
    search_name = st.sidebar.text_input("Search by Name:")
    
    # OVR Slider
    min_rating = st.sidebar.slider(
        "Minimum OVR Rating", 
        int(df['OVR'].min()), 
        int(df['OVR'].max()), 
        int(df['OVR'].min())
    )
    
    # Position Dropdown (Grabs all unique positions from your CSV)
    positions = ["All"] + list(df['Position'].dropna().unique())
    selected_position = st.sidebar.selectbox("Select Position:", positions)

    # 4. Apply the Filters
    # Start with the OVR filter
    filtered_df = df[df['OVR'] >= min_rating]
    
    # Apply name filter if they typed something
    if search_name:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(search_name, case=False, na=False)]
        
    # Apply position filter if they didn't leave it on "All"
    if selected_position != "All":
        filtered_df = filtered_df[filtered_df['Position'] == selected_position]

    # 5. Display the Database!
    st.write(f"Showing {len(filtered_df)} players matching your criteria:")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

except FileNotFoundError:
    st.error("Could not find 'EAFC26-Men.csv'. Make sure the exact file name is correct and it is in the same folder as app.py!")
import streamlit as st
import pandas as pd
import base64
import plotly.express as px
import numpy as np
from sklearn.neighbors import NearestNeighbors

# 1. Page Setup
st.set_page_config(page_title="EA FC 26 Scout", layout="wide")

def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as file:
            encoded_string = base64.b64encode(file.read())
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
    except FileNotFoundError:
        pass

add_bg_from_local('background.jpg')
st.title("EA FC 26 Scout Database")

@st.cache_data
def load_data():
    return pd.read_csv('EAFC26-Men.csv')

try:
    df = load_data()

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Filter Players")
    search_name = st.sidebar.text_input("Search by Name:")
    
    if 'OVR' in df.columns:
        min_rating = st.sidebar.slider(
            "Minimum OVR Rating", 
            int(df['OVR'].min()), int(df['OVR'].max()), int(df['OVR'].min())
        )
    else:
        min_rating = 0

    positions = ["All"] + list(df['Position'].dropna().unique())
    selected_position = st.sidebar.selectbox("Select Position:", positions)

    # PlayStyle Filter Logic
    all_styles = set()
    for s in df['play style'].dropna():
        styles = s.replace("[", "").replace("]", "").replace("'", "").split(", ")
        all_styles.update(styles)
    selected_style = st.sidebar.selectbox("Filter by PlayStyle:", ["All"] + sorted(list(all_styles)))

    # --- FILTERING LOGIC ---
    filtered_df = df[df['OVR'] >= min_rating].copy()
    
    if search_name:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(search_name, case=False, na=False)]
        
    if selected_position != "All":
        filtered_df = filtered_df[filtered_df['Position'] == selected_position]

    if selected_style != "All":
        filtered_df = filtered_df[filtered_df['play style'].str.contains(selected_style, na=False)]

    # --- MAIN DISPLAY ---
    st.write(f"Showing {len(filtered_df)} players matching your criteria:")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    # --- ADVANCED SCOUTING & COMPARISON ---
    st.divider() 
    
    if not filtered_df.empty:
        st.subheader("Advanced Scouting & AI Comparison")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            filtered_df['Selector_Label'] = filtered_df['Name'] + " (ID: " + filtered_df['ID'].astype(str) + ")"
            p1_label = st.selectbox("Select Player 1:", filtered_df['Selector_Label'].unique(), key="p1")
            p1_data = filtered_df[filtered_df['Selector_Label'] == p1_label].iloc[0]
            
            st.image(p1_data['card'], width=200)
            compare_mode = st.checkbox("🆚 Compare with another player?")
            
            p2_data = None
            if compare_mode:
                p2_label = st.selectbox("Select Player 2:", filtered_df['Selector_Label'].unique(), key="p2")
                p2_data = filtered_df[filtered_df['Selector_Label'] == p2_label].iloc[0]
                st.image(p2_data['card'], width=200)

        with col2:
            stats_cols = ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY']
            
            # Radar Chart
            fig = px.line_polar(line_close=True, range_r=[0, 100])
            
            fig.add_trace(px.line_polar(
                r=[float(p1_data[s]) for s in stats_cols],
                theta=stats_cols,
                line_close=True
            ).data[0])
            fig.data[0].name = p1_data['Name']
            fig.data[0].fill = 'toself'
            fig.data[0].line.color = '#00FF00'
            
            if compare_mode and p2_data is not None:
                fig.add_trace(px.line_polar(
                    r=[float(p2_data[s]) for s in stats_cols],
                    theta=stats_cols,
                    line_close=True
                ).data[0])
                fig.data[1].name = p2_data['Name']
                fig.data[1].fill = 'toself'
                fig.data[1].line.color = '#FFFFFF'
            
            fig.update_layout(template="plotly_dark", showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
            
            # Metrics
            m_col1, m_col2 = st.columns(2)
            p1_total = sum([float(p1_data[s]) for s in stats_cols])
            m_col1.metric(f"{p1_data['Name']} Total Stats", int(p1_total))
            
            if compare_mode and p2_data is not None:
                p2_total = sum([float(p2_data[s]) for s in stats_cols])
                m_col2.metric(f"{p2_data['Name']} Total Stats", int(p2_total), delta=int(p2_total - p1_total))

            # --- AI SIMILARITY SCOUT (Inside col2) ---
            st.divider()
            st.subheader("Similarity Scout")
            
            # Prepare the AI
            features = ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY']
            ai_data = df.dropna(subset=features).copy()
            X = ai_data[features].values

            knn = NearestNeighbors(n_neighbors=4, metric='euclidean')
            knn.fit(X)

            p1_stats = np.array([float(p1_data[s]) for s in features]).reshape(1, -1)
            distances, indices = knn.kneighbors(p1_stats)

            rec_cols = st.columns(3)
            for i in range(1, 4):
                neighbor_idx = indices[0][i]
                neighbor_data = ai_data.iloc[neighbor_idx]
                with rec_cols[i-1]:
                    st.image(neighbor_data['card'], width=130)
                    st.write(f"**{neighbor_data['Name']}**")
                    score = round(100 - distances[0][i], 1)
                    st.caption(f"Stats Match: {score}%")

    else:
        st.warning("No players found with those filters.")

except Exception as e:
    st.error(f"Something went wrong: {e}")
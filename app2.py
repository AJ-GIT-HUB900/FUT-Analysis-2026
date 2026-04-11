import streamlit as st
import pandas as pd
import math

# ==========================================
# 1. PAGE SETUP & THEMING
# ==========================================
st.set_page_config(page_title="FC 26 Chemistry AI Optimizer", layout="wide")

st.markdown("""
<style>
    .ai-card {
        background: rgba(57, 255, 20, 0.05);
        border-left: 5px solid #39FF14;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 5px;
    }
    .metric-box {
        background: rgba(0,0,0,0.5);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #d4af37;
    }
</style>
""", unsafe_allow_html=True)

st.title("FUT 26 Chemistry Lab: AI Optimizer")
st.write("Build your team. Let the AI find the missing links to hit 33/33.")

# ==========================================
# 2. DATA ENGINE
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv('EAFC26-Men.csv')
    
    # Blank Slate Placeholder
    placeholder = pd.DataFrame([{
        'Name': '--- Select Player ---', 'Nation': 'None', 'Team': 'None', 
        'League': 'None', 'OVR': 0, 'ID': 0,
        'card': 'https://futbin.com/design/themes/fut24/img/cards/gold_rare.png'
    }])
    
    df = pd.concat([placeholder, df], ignore_index=True)
    # Row-by-row label creation to prevent ambiguity errors
    df['Selector'] = df.apply(lambda x: f"{x['Name']} ({x['Nation']})" if x['ID'] > 0 else x['Name'], axis=1)
    return df

# ==========================================
# 3. SQUAD BUILDING INTERFACE
# ==========================================
try:
    df = load_data()
    
    st.subheader("Build Your Starting XI")
    cols = st.columns(4)
    squad = []

    # Create 11 slots for the team
    for i in range(11):
        with cols[i % 4]:
            choice = st.selectbox(f"Slot {i+1}", df['Selector'], key=f"slot_{i}", label_visibility="collapsed")
            p_data = df[df['Selector'] == choice].iloc[0]
            
            if p_data['ID'] > 0:
                squad.append(p_data)
                st.image(p_data['card'], width=100)
            else:
                st.caption(f"Empty Slot {i+1}")

    st.divider()

    # ==========================================
    # 4. ADVANCED CHEMISTRY & AI LOGIC
    # ==========================================
    if len(squad) > 0:
        squad_df = pd.DataFrame(squad)
        
        # Calculate current link counts
        nations = squad_df['Nation'].value_counts().to_dict()
        leagues = squad_df['League'].value_counts().to_dict()
        teams = squad_df['Team'].value_counts().to_dict()

        total_chem = 0
        audit_results = []

        # Calculate Individual Chemistry
        for _, p in squad_df.iterrows():
            n_c, l_c, t_c = nations[p['Nation']], leagues[p['League']], teams[p['Team']]
            
            # Threshold Math
            n_pts = 3 if n_c >= 8 else 2 if n_c >= 5 else 1 if n_c >= 3 else 0
            l_pts = 3 if l_c >= 8 else 2 if l_c >= 5 else 1 if l_c >= 3 else 0
            t_pts = 3 if t_c >= 7 else 2 if t_c >= 4 else 1 if t_c >= 2 else 0
            
            p_total = min(3, n_pts + l_pts + t_pts)
            total_chem += p_total # FIXED: Correct syntax for adding to total
            
            audit_results.append({
                "Player": p['Name'],
                "Nation (Links)": f"{n_pts}pt ({n_c})",
                "League (Links)": f"{l_pts}pt ({l_c})",
                "Club (Links)": f"{t_pts}pt ({t_c})",
                "Total Chem": p_total
            })

        # --- DISPLAY RESULTS ---
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
            st.metric("TOTAL SQUAD CHEM", f"{total_chem}/33")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if total_chem == 33:
                st.balloons()
                st.success("Perfect Synergy! 💎")

            # --- AI OPTIMIZER SECTION ---
            st.subheader("AI Optimization")
            st.write("Targeting links that are 1 player away from a point...")

            ai_recs = []
            
            # AI Logic: Find "Near-Miss" Nations/Leagues (counts of 2, 4, 7)
            for nation, count in nations.items():
                if count in [2, 4, 7]:
                    # Find highest OVR player of this nation NOT in the squad
                    best_match = df[(df['Nation'] == nation) & (~df['ID'].isin(squad_df['ID']))].sort_values('OVR', ascending=False).iloc[0]
                    ai_recs.append({"Type": "Nation", "Target": nation, "Player": best_match})

            for league, count in leagues.items():
                if count in [2, 4, 7]:
                    best_match = df[(df['League'] == league) & (~df['ID'].isin(squad_df['ID']))].sort_values('OVR', ascending=False).iloc[0]
                    ai_recs.append({"Type": "League", "Target": league, "Player": best_match})

            # Display top AI suggestions
            if not ai_recs:
                st.write("No obvious 'one-player' fixes found. Your core is solid!")
            else:
                for rec in ai_recs[:3]:
                    st.markdown(f"""
                    <div class="ai-card">
                        <strong>Missing {rec['Type']} Link:</strong> Add 1 more player from <b>{rec['Target']}</b> 
                        to boost chemistry for all related players.
                    </div>
                    """, unsafe_allow_html=True)
                    st.write(f"**Recommended:** {rec['Player']['Name']} ({rec['Player']['OVR']} OVR)")
                    st.image(rec['Player']['card'], width=80)

        with res_col2:
            st.subheader("Chemistry Audit")
            st.dataframe(pd.DataFrame(audit_results), use_container_width=True, hide_index=True)

    else:
        st.info("The Lab is empty. Start selecting players to activate the AI Optimizer.")

except Exception as e:
    st.error(f"System Error: {e}")
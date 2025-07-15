import math
import streamlit as st

# --- App Title and Description ---
st.set_page_config(page_title="Tibia Melee Skill Tracker")
st.title("🗡️ Tibia Melee Skill Tracker")
st.markdown("Track your melee skill progress, points remaining, and estimated training time based on loyalty bonus and training method.")

# --- User Input Form ---
with st.form("skill_form"):
    skill = st.number_input("What is your current melee skill level?", min_value=10, max_value=200, value=102)
    percent_left = st.number_input("What is the % left to next level?", min_value=0.0, max_value=100.0, value=19.0)
    loyalty_bonus = st.number_input("What is your loyalty bonus %?", min_value=0.0, max_value=50.0, value=5.0)

    training_type = st.selectbox(
        "Training Method",
        [
            "Online Training (monster combat)",
            "Offline Training (stamina bed)",
            "Dummy Training (training weapon at dummy)"
        ]
    )

    submitted = st.form_submit_button("Calculate")

# --- Define hit rates based on training type ---
HIT_RATES = {
    "Online Training (monster combat)": 7200,      # ~2 hits/sec
    "Offline Training (stamina bed)": 3000,        # estimated average
    "Dummy Training (training weapon at dummy)": 2400  # ~1.5s swing speed
}

# --- Calculation Logic ---
if submitted:
    A = 50      # Melee skill constant
    b = 1.1     # Knight vocation constant
    c = 10      # Skill offset

    hit_rate_per_hour = HIT_RATES.get(training_type, 2000)

    progress_left = percent_left / 100
    progress_done = 1 - progress_left

    Tp_current = A * (b ** (skill - c) - 1) / (b - 1)
    P_next = A * (b ** (skill - c))
    points_done = P_next * progress_done
    Tp_total_now = Tp_current + points_done
    Tp_next = A * (b ** (skill + 1 - c) - 1) / (b - 1)

    # Loyalty bonus reduces required training effort
    raw_points_remaining = P_next * progress_left
    adjusted_points_remaining = raw_points_remaining * (1 - loyalty_bonus / 100)
    hours_remaining = adjusted_points_remaining / hit_rate_per_hour if hit_rate_per_hour > 0 else 0

    # --- Display Results ---
    st.markdown("### 📊 Results")
    st.write(f"**Skill Level:** {skill}")
    st.write(f"**Progress Done:** {progress_done * 100:.2f}%")
    st.write(f"**Points Accumulated in Current Level:** {points_done:,.0f}")
    st.write(f"**Total Skill Points So Far:** {Tp_total_now:,.0f}")
    st.write(f"**Points Needed for Next Level:** {P_next:,.0f}")
    st.write(f"**Raw Points Remaining:** {raw_points_remaining:,.0f}")
    st.write(f"**Loyalty Bonus Applied ({loyalty_bonus:.1f}%):** -{(raw_points_remaining - adjusted_points_remaining):,.0f} points")
    st.write(f"**Effective Points Remaining:** {adjusted_points_remaining:,.0f}")
    st.write(f"**Estimated Time to Next Level:** {hours_remaining:.2f} hours")
    st.caption(f"Training: {training_type} — Hits/hour: {hit_rate_per_hour:,}")

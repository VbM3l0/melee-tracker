import math
import streamlit as st

# --- App Title and Description ---
st.set_page_config(page_title="Tibia Melee Skill Tracker")
st.title("🗡️ Tibia Melee Skill Tracker")
st.markdown("Track your melee skill progress, points remaining, and estimated training time based on your selected training method. Loyalty bonus is displayed for reference only.")

# --- User Input Form ---
with st.form("skill_form"):
    skill = st.number_input("What is your current melee skill level?", min_value=10, max_value=200, value=102)
    percent_left = st.number_input("What is the % left to next level?", min_value=0.0, max_value=100.0, value=19.0)
    desired_level = st.number_input("Optional: What is your desired target level? (leave blank for next level)", min_value=skill+1, max_value=200, value=0, step=1)
    loyalty_bonus = st.number_input("What is your loyalty bonus %? (for display only)", min_value=0.0, max_value=50.0, value=5.0)

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
    "Online Training (monster combat)": 1800,      # ~1 hit every 2 seconds
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

    # Determine target level
    target_level = desired_level if desired_level > 0 else skill + 1
    Tp_target = A * (b ** (target_level - c) - 1) / (b - 1)
    points_remaining = Tp_target - Tp_total_now
    hours_remaining = points_remaining / hit_rate_per_hour if hit_rate_per_hour > 0 else 0

    # --- Display Results ---
    st.markdown("### 📊 Results")
    st.write(f"**Current Skill Level:** {skill}")
    st.write(f"**Target Skill Level:** {target_level}")
    st.write(f"**Progress Done Toward Next Level:** {progress_done * 100:.2f}%")
    st.write(f"**Total Skill Points So Far:** {Tp_total_now:,.0f}")
    st.write(f"**Total Points Required for Target Level:** {Tp_target:,.0f}")
    st.write(f"**Points Remaining to Target Level:** {points_remaining:,.0f}")
    st.write(f"**Estimated Time to Reach Target Level:** {hours_remaining:.2f} hours")
    st.caption(f"Training: {training_type} — Hits/hour: {hit_rate_per_hour:,} — Loyalty Bonus: {loyalty_bonus:.1f}% (for display only)")

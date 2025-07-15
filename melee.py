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
    desired_level_input = st.text_input("Optional: What is your desired target level? (leave blank for next level)")
    loyalty_bonus = st.number_input("What is your loyalty bonus %? (for display only)", min_value=0.0, max_value=50.0, value=5.0)

    training_type = st.selectbox(
        "Training Method",
        [
            "Online Training (monster combat)",
            "Offline Training (stamina bed)",
            "Dummy Training (training weapon at dummy)"
        ]
    )

    st.markdown("#### Optional: Weekly Training Plan")
    online_hours = st.number_input("How many hours per week do you train online (monster combat)?", min_value=0.0, value=7.0)
    offline_hours = st.number_input("How many hours per week do you train offline (stamina bed)?", min_value=0.0, value=42.0)

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

    # Handle optional target level
    try:
        desired_level = int(desired_level_input)
        if desired_level <= skill:
            target_level = skill + 1
        else:
            target_level = desired_level
    except:
        target_level = skill + 1

    Tp_target = A * (b ** (target_level - c) - 1) / (b - 1)
    points_remaining = Tp_target - Tp_total_now
    hours_remaining = points_remaining / hit_rate_per_hour if hit_rate_per_hour > 0 else 0

    # Estimate time based on total training plan (combined online + offline)
    total_weekly_hits = (online_hours * HIT_RATES["Online Training (monster combat)"] +
                         offline_hours * HIT_RATES["Offline Training (stamina bed)"])
    weekly_training_hours = online_hours + offline_hours
    weeks_to_reach = points_remaining / total_weekly_hits if total_weekly_hits > 0 else 0
    total_days_to_reach = weeks_to_reach * 7

    # --- Display Results ---
    st.markdown("### 📊 Results")
    st.write(f"**Current Skill Level:** {skill}")
    st.write(f"**Target Skill Level:** {target_level}")
    st.write(f"**Progress Done Toward Next Level:** {progress_done * 100:.2f}%")
    st.write(f"**Total Skill Points So Far:** {Tp_total_now:,.0f}")
    st.write(f"**Total Points Required for Target Level:** {Tp_target:,.0f}")
    st.write(f"**Points Remaining to Target Level:** {points_remaining:,.0f}")
    st.write(f"**Estimated Time to Reach Target Level (based on selected method only):** {hours_remaining:.2f} hours")
    st.write(f"**Estimated Total Days with Weekly Training Plan:** {total_days_to_reach:.1f} days ({weeks_to_reach:.2f} weeks)")
    st.caption(f"Training: {training_type} — Hits/hour: {hit_rate_per_hour:,} — Loyalty Bonus: {loyalty_bonus:.1f}% (for display only)")

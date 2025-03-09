import streamlit as st
import time

# Constants
WORK_TIME = 25 * 60  # 25 minutes in seconds
BREAK_TIME = 5 * 60  # 5 minutes in seconds

# Initialize session state
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "points" not in st.session_state:
    st.session_state.points = 0
if "badges" not in st.session_state:
    st.session_state.badges = []

# Timer logic
def start_timer():
    st.session_state.start_time = time.time()
    st.session_state.is_running = True

def pause_timer():
    st.session_state.is_running = False

def reset_timer():
    st.session_state.start_time = None
    st.session_state.elapsed_time = 0
    st.session_state.is_running = False

# App layout
st.title("FocusFlow Timer 🍅")

# Timer display
if st.session_state.is_running:
    elapsed_time = int(time.time() - st.session_state.start_time)
    remaining_time = max(WORK_TIME - elapsed_time, 0)
    minutes, seconds = divmod(remaining_time, 60)
    st.write(f"Time remaining: {minutes:02}:{seconds:02}")
else:
    st.write("Press Start to begin your focus session!")

# Buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Start"):
        start_timer()
with col2:
    if st.button("Pause"):
        pause_timer()
with col3:
    if st.button("Reset"):
        reset_timer()

# Points and badges
if st.session_state.elapsed_time >= WORK_TIME and not st.session_state.is_running:
    st.session_state.points += 10
    st.session_state.elapsed_time = 0
    st.balloons()  # Celebrate!
    st.write(f"🎉 You earned 10 points! Total points: {st.session_state.points}")

    # Award badges
    if st.session_state.points >= 50 and "50 Points Badge" not in st.session_state.badges:
        st.session_state.badges.append("50 Points Badge")
        st.write("🏅 You earned the 50 Points Badge!")

# Display points and badges
st.write(f"Total Points: {st.session_state.points}")
st.write("Badges: " + ", ".join(st.session_state.badges))
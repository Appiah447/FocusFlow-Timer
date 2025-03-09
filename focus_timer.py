import streamlit as st
import time

# Constants
WORK_TIME = 50 * 60  # 50 minutes in seconds
BREAK_TIME = 10 * 60  # 10 minutes in seconds

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
    if st.session_state.points >= 100 and "100 Points Badge" not in st.session_state.badges:
    st.session_state.badges.append("100 Points Badge")
    st.write("🏆 You earned the 100 Points Badge!")

# Define levels
levels = {
    0: "Beginner",
    100: "Intermediate",
    200: "Advanced",
    500: "Expert"
}

# Display current level
current_level = "Beginner"
for points_required, level_name in levels.items():
    if st.session_state.points >= points_required:
        current_level = level_name

st.write(f"Level: {current_level}")

# Initialize leaderboard
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = {}

# Add user to leaderboard
user_name = st.text_input("Enter your name to join the leaderboard:")
if user_name and st.button("Join Leaderboard"):
    st.session_state.leaderboard[user_name] = st.session_state.points

# Display leaderboard
st.write("Leaderboard:")
for name, points in sorted(st.session_state.leaderboard.items(), key=lambda x: x[1], reverse=True):
    st.write(f"{name}: {points} points")

# Display points and badges
st.write(f"Total Points: {st.session_state.points}")
st.write("Badges: " + ", ".join(st.session_state.badges))

# Create two columns
col1, col2 = st.columns(2)

# Add content to the first column
with col1:
    st.write("### Timer")
    if st.session_state.is_running:
        elapsed_time = int(time.time() - st.session_state.start_time)
        remaining_time = max(WORK_TIME - elapsed_time, 0)
        minutes, seconds = divmod(remaining_time, 60)
        st.write(f"Time remaining: {minutes:02}:{seconds:02}")
    else:
        st.write("Press Start to begin your focus session!")

# Add content to the second column
with col2:
    st.write("### Points & Badges")
    st.write(f"Total Points: {st.session_state.points}")
    st.write("Badges: " + ", ".join(st.session_state.badges))
    
    # Add a sidebar
with st.sidebar:
    st.write("### Settings")
    work_time = st.slider("Work Time (minutes)", 1, 60, 25)
    break_time = st.slider("Break Time (minutes)", 1, 30, 5)
    WORK_TIME = work_time * 60
    BREAK_TIME = break_time * 60

    st.write("### Leaderboard")
    for name, points in sorted(st.session_state.leaderboard.items(), key=lambda x: x[1], reverse=True):
        st.write(f"{name}: {points} points")
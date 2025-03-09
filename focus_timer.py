import streamlit as st
import time
import base64

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
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = {}
if "daily_challenge" not in st.session_state:
    st.session_state.daily_challenge = {"completed": 0, "goal": 3}

# Function to play sound
def play_sound(sound_file):
    with open(sound_file, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)

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

# Sidebar for settings and leaderboard
with st.sidebar:
    st.write("### Settings")
    work_time = st.slider("Work Time (minutes)", 1, 60, 25)
    break_time = st.slider("Break Time (minutes)", 1, 30, 5)
    WORK_TIME = work_time * 60
    BREAK_TIME = break_time * 5

    st.write("### Leaderboard")
    for name, points in sorted(st.session_state.leaderboard.items(), key=lambda x: x[1], reverse=True):
        st.write(f"{name}: {points} points")

# Timer display
if st.session_state.is_running:
    elapsed_time = int(time.time() - st.session_state.start_time)
    remaining_time = max(WORK_TIME - elapsed_time, 0)
    minutes, seconds = divmod(remaining_time, 60)
    st.write(f"Time remaining: {minutes:02}:{seconds:02}")

    # Progress bar
    progress = (WORK_TIME - remaining_time) / WORK_TIME
    st.progress(progress)

    # Check if the timer has ended
    if remaining_time <= 0:
        st.session_state.is_running = False
        st.session_state.points += 10
        st.session_state.elapsed_time = 0
        play_sound("sounds/focusflow_sound.mp3")  # Play sound
        st.balloons()  # Celebrate!
        st.write("🎉 Focus session completed! You earned 10 points.")

        # Update daily challenge
        st.session_state.daily_challenge["completed"] += 1
        if st.session_state.daily_challenge["completed"] >= st.session_state.daily_challenge["goal"]:
            if "Bonus Badge" not in st.session_state.badges:
                st.session_state.badges.append("Bonus Badge")
                st.write("🎉 You completed the daily challenge and earned a Bonus Badge!")
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
st.write(f"Total Points: {st.session_state.points}")
st.write("Badges: " + ", ".join(st.session_state.badges))

# Award badges
if st.session_state.points >= 50 and "50 Points Badge" not in st.session_state.badges:
    st.session_state.badges.append("50 Points Badge")
    play_sound("sounds/focusflow_sound.mp3")  # Play sound
    st.write("🏅 You earned the 50 Points Badge!")
if st.session_state.points >= 100 and "100 Points Badge" not in st.session_state.badges:
    st.session_state.badges.append("100 Points Badge")
    play_sound("sounds/focusflow_sound.mp3")  # Play sound
    st.write("🏆 You earned the 100 Points Badge!")

# Leaderboard input
user_name = st.text_input("Enter your name to join the leaderboard:")
if user_name and st.button("Join Leaderboard"):
    st.session_state.leaderboard[user_name] = st.session_state.points
    st.write(f"Welcome, {user_name}! You've been added to the leaderboard.")

# Daily challenge
st.write("### Daily Challenge")
st.write(f"Complete {st.session_state.daily_challenge['goal']} focus sessions today to earn a bonus badge!")
st.write(f"Progress: {st.session_state.daily_challenge['completed']}/{st.session_state.daily_challenge['goal']}")

# Customizable themes
theme = st.selectbox("Choose a theme", ["Light", "Dark", "Forest", "Ocean", "Space"])
if theme == "Forest":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #228B22;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
elif theme == "Ocean":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #1E90FF;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
elif theme == "Space":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #000033;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Social sharing
st.write("### Share Your Achievements")
st.write("Let others know about your progress! Copy the link below and share it:")
st.code(f"https://focusflow-timer-fptuaezjebef9bhztlsafa.streamlit.app/")

# Credits
st.sidebar.write("### Credits")
st.sidebar.write("Sound by luisangelmaciel from Freesound.org")
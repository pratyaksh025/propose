import mysql.connector
from connection import mycon
import streamlit as st
import bcrypt as b
import time
import random

def get_bonds():
    """Fetch all bond terms from the database."""
    conn = mycon()
    cur = conn.cursor()
    cur.execute("SELECT terms FROM bonds")
    bonds = [row[0] for row in cur.fetchall()]
    conn.close()
    return bonds

def login_page():
    st.markdown(
        """
        <style>
        .bg-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('heart.png') no-repeat center center fixed;
            background-size: cover;
            z-index: -1;
        }
        .title-container {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            color: #ff69b4;
            margin-top: 50px;
            text-shadow: 0 0 10px #ff69b4, 0 0 20px #ff69b4, 0 0 30px #ff69b4;
        }
        .title-container::before {
            content: '❤️ ';
        }
        .title-container::after {
            content: ' ❤️';
        }
        .input-container {
            text-align: center;
            margin-top: 30px;
        }
        .stTextInput > div > div > input {
            border: 2px solid #ff69b4;
            border-radius: 10px;
            padding: 10px;
            font-size: 20px;
            text-align: center;
        }
        .stButton > button {
            background-color: #ff69b4;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 20px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .stButton > button:hover {
            background-color: #ff1493;
        }
        </style>
        <div class="bg-container"></div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="title-container">Bond Agreement Login</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    user = st.text_input("Enter your name")
    pasw = st.text_input("Enter your password", type="password")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Login"):
        conn = mycon()
        cur = conn.cursor(buffered=True)
        cur.execute("SELECT pass FROM userper WHERE username = %s", (user,))
        result = cur.fetchone()

        if result is None:
            st.error("User not found! Redirecting to registration...")
            time.sleep(2)
            st.session_state["menu_selection"] = "Create User"
            st.rerun()
        else:
            stored_pass = result[0]  # Removed .encode()

            if b.checkpw(pasw.encode(), stored_pass):
                st.success("Login Successful!")
                st.session_state.update({
                    "logged_in": True,
                    "username": user,
                    "bonds": get_bonds(),
                    "current_bond": 0,
                    "no_clicked": False,
                    "signature_uploaded": False
                })
                time.sleep(1)
                st.rerun()
            else:
                st.error("Incorrect password! Try again.")
                time.sleep(1)
                st.rerun()

def falling_hearts():
    """Generate falling hearts animation using JavaScript."""
    st.markdown(
        """
        <script>
        function createHearts() {
            let heartContainer = document.createElement('div');
            heartContainer.style.position = 'fixed';
            heartContainer.style.top = '0';
            heartContainer.style.left = '0';
            heartContainer.style.width = '100%';
            heartContainer.style.height = '100%';
            heartContainer.style.pointerEvents = 'none';
            heartContainer.style.zIndex = '9999';
            document.body.appendChild(heartContainer);

            for (let i = 0; i < 30; i++) {
                let heart = document.createElement('div');
                heart.innerHTML = '💖';
                heart.style.position = 'absolute';
                heart.style.left = Math.random() * 100 + 'vw';
                heart.style.top = '-50px';
                heart.style.fontSize = '24px';
                heart.style.animation = 'fall 3s linear infinite';
                heart.style.opacity = Math.random();
                heart.style.transform = 'rotate(' + (Math.random() * 360) + 'deg)';
                heartContainer.appendChild(heart);

                let duration = Math.random() * 2 + 1;
                heart.style.animationDuration = duration + 's';
            }

            setTimeout(() => { heartContainer.remove(); }, 3000);
        }

        createHearts();  // Create hearts immediately
        </script>
        <style>
        @keyframes fall {
            0% { transform: translateY(-100px) rotate(0deg); opacity: 1; }
            100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def big_heart():
    """Display a big heart with 'I love you' text on the whole screen."""
    st.markdown(
        """
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            background: rgba(255, 255, 255, 0.8);
            z-index: 9999;
            flex-direction: column;
        ">
            <div style="
                font-size: 100px;
                animation: pulse 1s infinite;
            ">
                ❤️
            </div>
            <div style="
                font-size: 32px;
                color: #d10068;
                margin-top: 20px;
            ">
                I love you
            </div>
        </div>
        <style>
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def show_bond():
    """Display bonds one by one with falling hearts animation."""
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] { display: none; } /* Hide Sidebar */

        .bond-container {
            text-align: center;
            margin-top: 50px;
        }
        .bond-text {
            font-size: 32px;
            font-weight: bold;
            font-family: 'Comic Sans MS', cursive;
            color: #ff1493;
            background: rgba(255, 240, 245, 0.8);
            padding: 20px;
            border-radius: 15px;
            display: inline-block;
            animation: glow 1s infinite alternate;
        }
        @keyframes glow {
            from {
                text-shadow: 0 0 10px #ff1493, 0 0 20px #ff1493, 0 0 30px #ff1493, 0 0 40px #ff1493, 0 0 50px #ff1493, 0 0 60px #ff1493, 0 0 70px #ff1493;
            }
            to {
                text-shadow: 0 0 20px #ff69b4, 0 0 30px #ff69b4, 0 0 40px #ff69b4, 0 0 50px #ff69b4, 0 0 60px #ff69b4, 0 0 70px #ff69b4, 0 0 80px #ff69b4;
            }
        }
        .button-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }
        .yes-button, .no-button {
            font-size: 20px;
            padding: 12px 24px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            text-align: center;
            width: 150px;
        }
        .yes-button {
            background-color: #ff69b4;
            color: white;
        }
        .yes-button:hover {
            background-color: #ff1493;
        }
        .no-button {
            background-color: #d10068;
            color: white;
        }
        .no-button:hover {
            background-color: #a00050;
        }
        .final-text {
            font-size: 40px;
            font-weight: bold;
            color: #ff1493;
            text-align: center;
            margin-top: 50px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    bonds = st.session_state["bonds"]
    bond_index = st.session_state["current_bond"]
    no_clicked = st.session_state.get("no_clicked", False)
    signature_uploaded = st.session_state.get("signature_uploaded", False)

    if bond_index < len(bonds):
        falling_hearts()  # Hearts fall before each bond
        st.markdown(f"<div class='bond-container'><p class='bond-text'>{bonds[bond_index]}</p></div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([2, 1, 2])

        with col1:
            st.write("")  # Empty space for alignment

        with col2:
            yes_clicked = st.button("Yes! ❤️", key=f"yes_{bond_index}")

        with col3:
            if not no_clicked:
                no_clicked = st.button("No 💔", key=f"no_{bond_index}")

        if yes_clicked:
            big_heart()  # Show big heart
            time.sleep(3)
            st.session_state["current_bond"] += 1
            st.session_state["no_clicked"] = False  # Reset "No" state
            st.rerun()

        if no_clicked:
            st.warning("Oh no! You must say Yes! 💕")
            time.sleep(1)
            st.session_state["no_clicked"] = False
            st.rerun()

    else:
        falling_hearts()  # Final heart fall
        st.markdown("<div class='final-text'>All bonds accepted! You're officially bound by love! ❤️</div>", unsafe_allow_html=True)
        
        signature = st.file_uploader("Upload your signed signature to finalize the bond 💕", type=["png", "jpg", "jpeg"])

        if signature:
            st.session_state["signature_uploaded"] = True
            st.session_state["signature"] = signature

        if st.session_state["signature_uploaded"]:
            if st.button("Submit"):
                # Save the signature to the database
                conn = mycon()
                cur = conn.cursor()
                cur.execute("INSERT INTO user_signature (username, signature) VALUES (%s, %s)", (st.session_state["username"], st.session_state["signature"].read()))
                conn.commit()
                conn.close()
                st.success("Signature received! 💍")
                time.sleep(2)
                st.markdown(
                    """
                    <div style="
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        background: rgba(255, 255, 255, 0.8);
                        z-index: 9999;
                        flex-direction: column;
                    ">
                        <div style="
                            font-size: 100px;
                            animation: pulse 1s infinite;
                        ">
                            ❤️
                        </div>
                        <div style="
                            font-size: 32px;
                            color: #d10068;
                            margin-top: 20px;
                        ">
                            I love you forever Sakshi! ❤️
                        </div>
                    </div>
                    <style>
                    @keyframes pulse {
                        0% { transform: scale(1); }
                        50% { transform: scale(1.2); }
                        100% { transform: scale(1); }
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.warning("Please upload your signature to complete the bond! 💕")

# Run the app logic
if "logged_in" not in st.session_state:
    login_page()
else:
    show_bond()

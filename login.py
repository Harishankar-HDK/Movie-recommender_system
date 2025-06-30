import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import os
from dotenv import load_dotenv
from app import app  # Movie recommender app function

# Firebase init
load_dotenv()
cred_path = os.getenv("FIREBASE_CREDENTIAL_PATH")
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

def login():

    if 'signed_in' not in st.session_state:
        st.session_state.signed_in = False
    if 'user' not in st.session_state:
        st.session_state.user = None

    if not st.session_state.signed_in:
        st.markdown(
        "<h1 style='white-space: nowrap;'>Welcome to <span style='color:red;'>Movie-Recommendation</span> System</h1>",
        unsafe_allow_html=True
        )
        option = st.selectbox('Login/Sign Up', ['Login', 'Sign Up'], index=0)

        email = st.text_input("Email")
        password = st.text_input("Password", type='password')

        if option == 'Sign Up':
            username = st.text_input("Enter your Unique User Name")

        if st.button(option):
            try:
                if option == 'Login':
                    user = auth.get_user_by_email(email) #This line does not verify the password, since Firebase Admin SDK doesn't support password-based login. This is fine for prototyping but not secure in production
                    st.success("Login Successful")
                else:
                    user = auth.create_user(email=email, password=password, uid=username)
                    st.success("Account created successfully. Please log in.")
                    st.stop()

                st.session_state.signed_in = True
                st.session_state.user = {'uid': user.uid, 'email': user.email}
                st.rerun()

            except Exception as e:
                st.warning(f"{option} failed: {e}")

    else:
        app()  # Call the main app if signed in

login()

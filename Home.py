import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="UNICEF-CBE",
    page_icon=("Boom")
)
st.subheader('UNICEF CBE Project - ACT & PPC', divider='rainbow')

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    st.write("Here goes your normal Streamlit app...")
    st.button("Click me")


    st.markdown('<h1 class="animate__animated animate__fadeInDown">Hello!</h1>', unsafe_allow_html=True)


    st.markdown(
    """
    <style>
    .unicef-text {
        color: #0099D8;
    }
    </style>
    """,
    unsafe_allow_html=True
)


    st.markdown(
    """
    <style>
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }

    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #0099D8; }
    }

    .typewriter-text {
        overflow: hidden;
        border-right: .15em solid #0099D8;
        white-space: nowrap;
        margin: 0 auto;
        letter-spacing: .15em;
        color: #0099D8;
        animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
        font-size: 19px; /* Adjust the font size as desired */
    }
    </style>
    """,
    unsafe_allow_html=True
)

    st.markdown("""
    <h1 class="typewriter-text">The purpose of this webApp is to maintain high-quality data.</h1>
    """,
    unsafe_allow_html=True
)


    multi = '''
 If you run into any technical problems or difficulties, feel free to contact Abdul Waris Amini, the Senior Data Officer at Premium Performance Consulting.
'''
    st.markdown(multi)

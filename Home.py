import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Multipage APP",
    page_icon=("Boom")
)
st.subheader('UNICEF CBE Project - ACT & PPC', divider='rainbow')

#text writer an
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


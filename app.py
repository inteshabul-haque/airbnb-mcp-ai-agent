import streamlit as st
import asyncio

from main import hotel_search


# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="SEARCH HEIST AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

/* Hide Streamlit default UI */
header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

/* Main App */
.stApp {
    background-color: #0b0b0b;
    color: white;
}

/* Remove default spacing */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1000px;
}

/* Title */
.title {
    text-align: center;
    color: #ff1a1a;

    font-size: 72px;
    font-weight: 900;

    letter-spacing: 4px;

    margin-top: 20px;
    margin-bottom: 10px;

    text-shadow: 0px 0px 10px rgba(255,0,0,0.45);
}
            
/* Subtitle */
.subtitle {
    text-align: center;
    color: #dddddd;
    font-size: 22px;
    margin-bottom: 50px;
}

/* Input */
.stTextInput input {
    background-color: #111111 !important;
    color: white !important;

    border: 2px solid red !important;
    border-radius: 12px !important;

    padding: 18px !important;
    font-size: 18px !important;
}

/* Button */
.stButton {
    display: flex;
    justify-content: center;
    margin-top: 25px;
}

.stButton button {
    background: linear-gradient(90deg, #ff0000, #990000);

    color: white;
    border: none;

    border-radius: 12px;

    width: 250px;
    height: 55px;

    font-size: 18px;
    font-weight: bold;
}

.stButton button:hover {
    transform: scale(1.03);
    transition: 0.3s;
}

/* Response Box */
.response-box {
    background-color: #111111;

    padding: 25px;

    border-radius: 15px;
    border-left: 5px solid red;

    margin-top: 35px;

    font-size: 17px;
    line-height: 1.8;

    color: white;
}

/* Footer */
.footer {
    text-align: center;
    color: #888888;

    margin-top: 60px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# =========================================
# HEADER
# =========================================

st.markdown(
    '<div class="title">SEARCH HEIST AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI Powered Airbnb Intelligence Agent</div>',
    unsafe_allow_html=True
)


# =========================================
# INPUT
# =========================================

query = st.text_input(
    "",
    placeholder="Ask about Airbnb stays, hotels, pricing, weather..."
)


# =========================================
# BUTTON
# =========================================

if st.button("START HEIST"):

    if query:

        with st.spinner("🔍 Searching Airbnb Intelligence..."):

            response = asyncio.run(
                hotel_search(query)
            )

            st.markdown(
                f"""
                <div class="response-box">
                    {response}
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================
# FOOTER
# =========================================

st.markdown(
    """
    <div class="footer">
    Built with Gemini AI • LangChain • MCP • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
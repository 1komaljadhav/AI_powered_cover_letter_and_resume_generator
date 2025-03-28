import streamlit as st
import homepage as homepage
import cover_letter as cover_letter
import resume as resume

# Set page configuration
st.set_page_config(page_title="AI Cover Letter & Resume Generator", page_icon="📄", layout="wide")

# Add custom CSS styles
st.markdown(
    """
    <style>
    /* General Page Styling */
    body {
        background-color: #E9F1FA; /* Background: Light Blue */
        font-family: 'Arial', sans-serif;
    }
    .stApp {
        background-color: #E9F1FA; /* Background: Light Blue */
        color: #111827; /* Text: Dark Charcoal */
    }

    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background-color: #FFFFFF; /* White */
        border-right: 1px solid #00ABE4; /* Bright Blue */
    }
    .sidebar .sidebar-title {
        color: #00ABE4; /* Bright Blue */
        font-size: 1.2rem;
        font-weight: bold;
    }
    .sidebar .sidebar-radio {
        color: #111827; /* Dark Charcoal */
    }

    /* Title Styling */
    h1, h2, h3, h4 {
        color: #00ABE4; /* Bright Blue */
    }

    /* Button Styling */
    .stButton>button {
        background-color: #00ABE4; /* Bright Blue */
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 1rem;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #007BB5; /* Darker Blue for hover */
    }

    /* Alert Styling */
    .stAlert {
        background-color: #00ABE4; /* Bright Blue */
        color: white;
        border: 1px solid #00ABE4;
        border-radius: 5px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Cover Letter Generator", "Resume Generator"])

# Page Routing
if page == "Home":
    homepage.show()
elif page == "Cover Letter Generator":
    cover_letter.show()
elif page == "Resume Generator":
    resume.show()

import streamlit as st
# st.set_page_config(page_title="AI Cover Letter & Resume Generator", page_icon="📄", layout="wide")

from PIL import Image

# Set page configuration - must be the first Streamlit command

def show():
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

        /* Title Styling */
        h1, h2, h3, h4 {
            color: #00ABE4; /* Bright Blue */
        }

        /* Input Box Styling */
        .stTextInput > div > div > input {
            background-color: #FFFFFF; /* White */
            border: 1px solid #00ABE4; /* Bright Blue */
            border-radius: 5px;
            padding: 10px;
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

        /* Info Box Styling */
        .stInfo {
            background-color: #FFFFFF; /* White */
            border: 1px solid #00ABE4; /* Bright Blue */
            border-radius: 5px;
            padding: 10px;
            color: #111827; /* Dark Charcoal */
        }

        /* Image Styling */
        img {
            border-radius: 10px;
        }

        /* Text Area Styling */
        textarea {
            background-color: #FFFFFF; /* White */
            border: 1px solid #00ABE4; /* Bright Blue */
            border-radius: 5px; /* Rounded corners */
            padding: 10px; /* Padding inside the textarea */
            color: #111827; /* Dark Charcoal for text */
            font-size: 1rem; /* Font size */
            width: 100%; /* Full width */
            box-sizing: border-box; /* Include padding and border in width */
        }

        /* Footer Styling */
        footer {
            text-align: center;
            color: #111827; /* Dark Charcoal */
            font-size: 0.9rem;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Main Title
    st.title("🚀 AI-Powered Cover Letter & Resume Generator")
    st.subheader("Create professional cover letters & resumes in seconds with AI!")

    st.write(
        "Welcome to the **AI-Powered Cover Letter & Resume Generator**—your ultimate tool for crafting professional and personalized job application documents effortlessly! "
        "Whether you're applying for your dream job or updating your resume, our AI-driven solution ensures you stand out with well-structured, compelling content tailored to your needs."
    )

    # Why Use This Tool?
    st.markdown("## 🔍 Why Use This Tool?")
    st.write(
        "Traditional resume-building can be **time-consuming** and **challenging**. Writing an engaging cover letter that highlights your skills while aligning with a job description is even harder. "
        "That’s where AI comes in! Our system simplifies the entire process, helping you:"
    )
    st.markdown("✅ Create **ATS-friendly** resumes in a few clicks.  \n"
                "✅ Generate **tailored cover letters** by analyzing job descriptions.  \n"
                "✅ Format your documents professionally with **ready-to-use templates**.  \n"
                "✅ **Save time** while improving the quality of your job applications.")

    # How It Works
    st.markdown("## 📌 How It Works?")
    st.write("Creating your cover letter and resume is as easy as 1-2-3!")
    st.markdown("""
    1️⃣ **Enter Your Details:** Fill in your basic details (Name, Contact, Skills, Experience, etc.).  
    - Upload or paste the **job description** to personalize your cover letter.  

    2️⃣ **Choose a Template:** Select from multiple **professional resume and cover letter formats**.  
    - Customize the layout and font style to match your preferences.  

    3️⃣ **Generate & Download:** Let AI **write your cover letter** based on the job description.  
    - Preview the document before **downloading it as a PDF**.
    """)

    st.success("✨ That’s it! Your job application materials are ready in minutes!")

    # Key Features
    st.markdown("## 🚀 Key Features")
    st.markdown("""
    🔹 **AI-Powered Writing:** Instantly generate cover letters and resumes based on job descriptions.  

    🔹 **Professional Templates:** Choose from a variety of **ATS-friendly** formats.  

    🔹 **Personalization & Editing:** Customize the content before finalizing your documents.  

    🔹 **Instant Download:** Get your files in **PDF format** for easy job applications.  

    🔹 **Time-Saving & Efficient:** No need to struggle with formatting or writing from scratch.  
    """)

    # Who Can Use This?
    st.markdown("## 🎯 Who Can Use This?")
    st.markdown("""
    🔹 **Job Seekers** – Looking for an edge in their applications.  

    🔹 **Students & Freshers** – Wanting to craft a great first impression.  

    🔹 **Professionals** – Updating their resumes for new opportunities.  

    🔹 **Recruiters & HR Teams** – Creating job-specific resumes quickly.  
    """)

    # Explore Features
   

    # Sample Templates Section
    st.markdown("## 📝 Sample Resume & Cover Letter Templates")

    st.subheader('Cover Letter')
    a1, a2 = st.columns(2)

    # Ensure the image file paths are correct
    try:
        image1 = Image.open('cv1.png')
        a1.image(image1, caption="Template 1", use_container_width=True)  # Updated parameter

        image2 = Image.open('cv2.png')
        a2.image(image2, caption="Template 2", use_container_width=True)  # Updated parameter

    except FileNotFoundError as e:
        st.error(f"Error: {e}. Please ensure the image files exist in the specified path.")

    st.subheader('Resume Templates')
    a1, a2 = st.columns(2)

    # Ensure the image file paths are correct
    try:
        image1 = Image.open('resume1.png')
        a1.image(image1, caption="Template 1", use_container_width=True)

        image2 = Image.open('resume2.png')
        a2.image(image2, caption="Template 2", use_container_width=True)

    except FileNotFoundError as e:
        st.error(f"Error: {e}. Please ensure the image files exist in the specified path.")

    # Why Choose AI?
    st.markdown("## 💡 Why Choose AI for Resume & Cover Letter Writing?")
    st.markdown("""
    📌 **Tailored to Job Descriptions:** AI analyzes job postings to align your content accordingly.  

    🎯 **Eliminates Guesswork:** No need to stress about wording—AI crafts professional text for you.  

    ⏳ **Saves Time:** What takes hours to write manually is done in seconds!  

    ✅ **Error-Free & Optimized:** Ensures clarity, grammar accuracy, and professional tone.  
    """)

    # Footer
    st.markdown("---")
    st.write("Developed with ❤️ using **Streamlit & AI**")


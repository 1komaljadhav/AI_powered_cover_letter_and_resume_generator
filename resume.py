import streamlit as st
from jinja2 import Environment, FileSystemLoader
import pdfkit
import os

def show():
    # Load Jinja2 Template Engine
    env = Environment(loader=FileSystemLoader("resume_templates/"))

    # Set the path to wkhtmltopdf executable (adjust based on your OS)
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    def generate_resume(template_name, resume_data):
        """Generate resume from selected template"""
        template = env.get_template(template_name)
        return template.render(resume_data)

    def save_pdf(html_content, pdf_filename):
        """Convert HTML resume to PDF"""
        pdfkit.from_string(html_content, pdf_filename, configuration=config)

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

 .stTextInput > div > div > input {
            background-color: #FFFFFF; /* White */
            border: 1px solid #00ABE4; /* Bright Blue */
            border-radius: 5px;
            padding: 10px;
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
            color: white;
        }

       

        /* Alert Styling */
        .stAlert {
            background-color: #00ABE4; /* Bright Blue */
            color: white;
            border: 1px solid #00ABE4;
            border-radius: 5px;
            padding: 10px;
        }

        /* Sidebar Styling */
        .sidebar .sidebar-content {
            background-color: #FFFFFF; /* White */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("📄 AI-Powered Resume Generator")

    # Step 1: Collect User Details
    st.header("👤 Personal Information")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    address = st.text_input("Address (City, State, Country)")
    linkedin = st.text_input("LinkedIn Profile")
    github = st.text_input("GitHub/Portfolio Website")

    st.header("🎓 Education")
    education = st.text_area("Enter your education details")

    st.header("💼 Projects")
    projects = st.text_area("Enter your project details")

    st.header("🛠️ Skills")
    skills = st.text_area("Enter your skills (comma-separated)")

    st.header("📜 Certifications")
    certifications = st.text_area("Enter your certifications")

    st.header("🏆 Awards & Achievements")
    awards = st.text_area("Enter awards or achievements")

    st.header("🌍 Languages Known")
    languages = st.text_area("Enter the languages you know")

    st.header("📋 Job Description")
    job_description = st.text_area("Paste the job description here")

    # Resume Template Selection
    st.header("📄 Select Resume Template")
    templates = {
        "Modern": "modern.html",
        "Classic": "classic.html",
        "Professional": "professional.html",
        "Simple": "withphoto.html"
    }
    selected_template = st.selectbox("Choose Resume Template", list(templates.keys()))
    selected_template_file = templates[selected_template]

    # Step 2: Generate Resume Content
    if st.button("Generate Content"):
        if not full_name or not email or not job_description:
            st.error("Please fill in required fields: Full Name, Email, and Job Description.")
        else:
            prompt = f"""
            Analyze the provided details and generate a professional, ATS-friendly resume. Follow these rules strictly:

                1. **Skill Matching Check**:  
                - Compare the provided skills with the job description.  
                - If the majority of the provided skills do not match the job description, return the following message:  
                    **"Skills are not matched with the job description. You are not applicable."**  
                - Otherwise, generate the resume.  

                2. **Resume Structure**:  
                - Do NOT add extra sections beyond the specified ones.  
                - Include ONLY the following sections in order:  
                    **Personal Information, Profile Summary, Education, Projects, Skills, Certifications, Awards & Achievements, Languages Known**  

                3. **Formatting & Tone**:  
                - Ensure the resume is professional, concise, and ATS-friendly.  
                - Use bullet points where necessary and avoid excessive formatting.  
                - Write in a clear, structured, and industry-standard format.  
                4. **Do NOT include any extra notes or comments. ONLY generate the resume as per the given structure.**

                ---

                ### User Details:  
                - **Name**: {full_name}  
                - **Email**: {email}  
                - **Phone**: {phone}  
                - **Address**: {address}  
                - **LinkedIn**: {linkedin if linkedin.strip() else "N/A"}  
                - **GitHub**: {github if github.strip() else "N/A"}  

                ### Job Description for Matching:  
                {job_description}  

                ### Resume Content:  
                - **Education**: {education}  
                - **Projects**: {projects}  
                - **Skills**: {skills}  
                - **Certifications**: {certifications}  
                - **Awards & Achievements**: {awards}  
                - **Languages Known**: {languages}
            """
            # Generate AI Resume Content
            generated_content = "Generated resume content based on the provided details."  # Placeholder for AI response
            st.session_state.generated_content = generated_content

    # Text area for modifications
    if "generated_content" in st.session_state:
        modified_content = st.text_area("Modify Generated Resume", value=st.session_state.generated_content, height=400)

        if st.button("Confirm Changes"):
            # Generate final resume from template
            updated_resume = generate_resume(selected_template_file, {"content": modified_content})

            # Display PDF Preview in Streamlit
            st.markdown("### Resume Preview")
            pdf_viewer_html = f"""
                <iframe src="resume_final.pdf" width="100%" height="600px" style="border: none;"></iframe>
            """
            st.components.v1.html(pdf_viewer_html, height=600, scrolling=True)

            # Convert to PDF
            pdf_filename = "resume_final.pdf"
            save_pdf(updated_resume, pdf_filename)

            # Provide Download Option
            with open(pdf_filename, "rb") as pdf_file:
                st.download_button(label="Download Resume", data=pdf_file, file_name="resume_final.pdf", mime="application/pdf")

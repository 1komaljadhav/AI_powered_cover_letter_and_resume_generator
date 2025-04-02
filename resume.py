import streamlit as st
from jinja2 import Environment, FileSystemLoader
import pdfkit
import os
import cohere
import re  # Import regex for parsing

# Initialize Cohere client
co = cohere.Client("uyRCRe0AwstpNh7hzjZR9Qz0MKqq94EbtBzFhlUj")

def show():
    # Load Jinja2 Template Engine
    env = Environment(loader=FileSystemLoader("resume_templates/"))

    # Set the path to wkhtmltopdf executable (adjust based on your OS)
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    def generate_resume(template_name, resume_data):
        """Generate resume from selected template"""
        try:
            template = env.get_template(template_name)
            return template.render(resume_data)
        except Exception as e:
            st.error(f"An error occurred while rendering the template: {e}")
            return ""

    def save_pdf(html_content, pdf_filename):
        """Convert HTML resume to PDF"""
        pdfkit.from_string(html_content, pdf_filename, configuration=config)

    import re

    def extract_resume_details(generated_content):
        """Extract structured resume data from the generated content."""
        
        def extract_single(pattern, content):
            """Extracts single-line fields like Name, Email, Phone, etc."""
            match = re.search(pattern, content)
            return match.group(1).strip() if match else "N/A"

        def extract_multiple(pattern, content):
            """Extracts multi-line sections like Education, Projects, Skills, etc."""
            match = re.search(pattern, content, re.DOTALL)
            return re.findall(r"-\s*(.*)", match.group(1)) if match else []
        
        # Extracting single-line fields
        resume_details = {
            "name": extract_single(r"Name:\s*(.*?)\s*\n", generated_content),
            "email": extract_single(r"Email:\s*(.*?)\s*\n", generated_content),
            "phone": extract_single(r"Phone:\s*(.*?)\s*\n", generated_content),
            "address": extract_single(r"Address:\s*(.*?)\s*\n", generated_content),
            "profile_summary": extract_single(r"Profile Summary:\s*(.*?)\s*---", generated_content),
        }

        # Extracting multi-line sections
        resume_details.update({
            "education": extract_multiple(r"Education:\s*(.*?)\s*---", generated_content),
            "projects": extract_multiple(r"Projects:\s*(.*?)\s*---", generated_content),
            "skills": extract_multiple(r"Skills:\s*(.*?)\s*---", generated_content),
            "certifications": extract_multiple(r"Certifications:\s*(.*?)\s*---", generated_content),
            "awards": extract_multiple(r"Awards & Achievements:\s*(.*?)\s*---", generated_content),
            "languages": extract_multiple(r"Languages Known:\s*(.*?)\s*---", generated_content),
        })
        print(resume_details)
        return resume_details

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
            color: #111827; /* Dark Charcoal */
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

    # Step 2: Generate Resume Content using Cohere API
    if st.button("Generate Content"):
        if not full_name or not email or not job_description:
            st.error("Please fill in required fields: Full Name, Email, and Job Description.")
        else:
            prompt = f"""
            Analyze the provided details and generate a professional, ATS-friendly resume with detailed description. Follow these rules strictly:

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
                - write somemore detailed 
                - if any section is empty then dont give that section in the resume.
                - if any section is not given then dont give that section in the resume.
                
                4. **Do NOT include any extra notes or comments. ONLY generate the resume as per the given structure. separate the section using --- this pls note it. and after section name : there is colon** 

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
            try:
                # Use Cohere API to generate resume content
                response = co.chat(
                    message=prompt,
                    chat_history=[],
                    max_tokens=700,
                    temperature=0.7
                )

                # Deb
                # Extract the generated content
                if hasattr(response, "text") and response.text:
                    # Clean the generated content by removing `*` and `***`
                    generated_content = response.text.replace("*", "").strip()
                    st.session_state.generated_content = generated_content
                    st.success("Resume content generated successfully!")
                else:
                    st.error("Failed to generate resume content. Please try again.")

            except Exception as e:
                st.error(f"An error occurred while generating content: {e}")

    # Text area for modifications
    if "generated_content" in st.session_state:
        modified_content = st.text_area("Modify Generated Resume", value=st.session_state.generated_content, height=400)

        if st.button("Confirm Changes"):
            # Extract structured data from the modified content
            resume_data = extract_resume_details(modified_content)

            # Generate final resume from template
            updated_resume = generate_resume(selected_template_file, resume_data)

            if updated_resume:
                # Display the rendered HTML in the preview
                st.markdown("### Resume Preview")
                st.components.v1.html(updated_resume, height=600, scrolling=True)

                # Convert the rendered HTML to a PDF
                pdf_filename = "resume_final.pdf"
                save_pdf(updated_resume, pdf_filename)

                # Provide a download button for the PDF
                with open(pdf_filename, "rb") as pdf_file:
                    st.download_button(label="Download Resume", data=pdf_file, file_name="resume_final.pdf", mime="application/pdf")
            else:
                st.error("Failed to render the resume. Please check the template.")


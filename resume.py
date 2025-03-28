import streamlit as st
from jinja2 import Environment, FileSystemLoader
import pdfkit
import os
import cohere
import re
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

    # Cohere API for AI-generated content
    class CoverLetter:
        @staticmethod
        def generate_resume_content(prompt):
            co = cohere.Client('uyRCRe0AwstpNh7hzjZR9Qz0MKqq94EbtBzFhlUj')  # Replace with your actual API key
            response = co.generate(
                model='command-r-plus-08-2024',
                prompt=prompt,
                max_tokens=450,
                temperature=0.49,
                k=2,
                p=0.75,
                frequency_penalty=0.134,
                presence_penalty=0,
                stop_sequences=['Sincerely', '[Your Name]'],
                return_likelihoods='NONE'
            )
            return response.generations[0].text

    # Streamlit App UI
    st.title("AI-Powered Resume Generator")

    # Step 1: Collect User Details
    st.header("Personal Information")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    address = st.text_input("Address (City, State, Country)")
    linkedin = st.text_input("LinkedIn Profile")
    github = st.text_input("GitHub/Portfolio Website")

    st.header("Education")
    education = st.text_area("Enter your education details")

    st.header("Projects")
    projects = st.text_area("Enter your project details")

    st.header("Skills")
    skills = st.text_area("Enter your skills (comma-separated)")

    st.header("Certifications")
    certifications = st.text_area("Enter your certifications")

    st.header("Awards & Achievements")
    awards = st.text_area("Enter awards or achievements")

    st.header("Languages Known")
    languages = st.text_area("Enter the languages you know")

    st.header("Job Description")
    job_description = st.text_area("Paste the job description here")

    # Resume Template Selection
    st.header("Select Resume Template")
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
                    **Personal Information,profile summary, Education, Projects, Skills, Certifications, Awards & Achievements, Languages Known**  

                3. **Formatting & Tone**:  
                - Ensure the resume is professional, concise, and ATS-friendly.  
                - Use bullet points where necessary and avoid excessive formatting.  
                - Write in a clear, structured, and industry-standard format.  
                4. **plzz DO NOT include any extra notes or comments. ONLY generate the resume as per the given structure.**

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
            plsss don't give any extra notes or comments, just generate the resume.
                """
            
            # prompt = f"""
            # Generate a professional, ATS-friendly resume:
            # Name: {full_name}
            # Email: {email}
            # Phone: {phone}
            # Address: {address}
            # LinkedIn: {linkedin if linkedin.strip() else "N/A"}
            # GitHub: {github if github.strip() else "N/A"}
            # Profile Summary: [Brief summary about the individual]
            # """

            # # Include additional sections if provided
            # if education.strip():
            #     prompt += f"\nEducation:\n{education}"
            # if projects.strip():
            #     prompt += f"\nProjects:\n{projects}"
            # if skills.strip():
            #     prompt += f"\nSkills:\n{skills}"
            # if certifications.strip():
            #     prompt += f"\nCertifications:\n{certifications}"
            # if awards.strip():
            #     prompt += f"\nAwards:\n{awards}"
            # if languages.strip():
            #     prompt += f"\nLanguages:\n{languages}"

            # prompt += f"\nJob Description:\n{job_description}"

            # Generate AI Resume Content
            generated_content = CoverLetter.generate_resume_content(prompt)
            generated_content = generated_content.replace("**", "").strip()

            # Store generated content in session state for modification
            st.session_state.generated_content = generated_content

    # Text area for modifications
    if "generated_content" in st.session_state:
        modified_content = st.text_area("Modify Generated Resume", value=st.session_state.generated_content, height=400)

        if st.button("Confirm Changes"):
            def extract_details(text):
                """Extract structured information from modified resume content using regex."""
                # Extract Name
                name_match = re.search(r"Name:\s*(.+)", text)
                name = name_match.group(1).strip() if name_match else "N/A"

                # Extract Email
                email_match = re.search(r"Email:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", text)
                email = email_match.group(1).strip() if email_match else "N/A"

                # Extract Phone
                phone_match = re.search(r"Phone:\s*(\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9})", text)
                phone = phone_match.group(1).strip() if phone_match else "N/A"

                # Extract Address
                address_match = re.search(r"Address:\s*(.+)", text)
                address = address_match.group(1).strip() if address_match else "N/A"

                # Extract LinkedIn
                linkedin_match = re.search(r"LinkedIn:\s*(https?://[^\s]+)", text)
                linkedin = linkedin_match.group(1).strip() if linkedin_match else "N/A"

                # Extract GitHub
                github_match = re.search(r"GitHub:\s*(https?://[^\s]+)", text)
                github = github_match.group(1).strip() if github_match else "N/A"

                # Extract Profile Summary
                summary_match = re.search(r"Profile Summary:\s*(.+?)Education:", text, re.DOTALL)
                summary = summary_match.group(1).strip() if summary_match else "N/A"

                # Extract Education
                education_section = re.search(r"Education:(.+?)Projects:", text, re.DOTALL)
                education = re.findall(r"-\s*(.+)", education_section.group(1)) if education_section else []

                # Extract Projects
                projects_section = re.search(r"Projects:(.+?)Skills:", text, re.DOTALL)
                projects = re.findall(r"-\s*(.+)", projects_section.group(1)) if projects_section else []

                # Extract Skills
                skills_section = re.search(r"Skills:(.+?)Certifications:", text, re.DOTALL)
                skills = re.findall(r"-\s*(.+)", skills_section.group(1)) if skills_section else []

                # Extract Certifications
                
                # Extract Certifications
                certifications_section = re.search(r"Certifications:\s*(.+)", text)
                certifications = re.findall(r"-\s*(.+)", certifications_section.group(1)) if certifications_section else []

                # Extract Awards
                awards_section = re.search(r"Awards & Achievements:\s*(.+)", text, re.DOTALL)
                awards = re.findall(r"-\s*(.+)", awards_section.group(1)) if awards_section else []

                # Extract Languages
                languages_section = re.search(r"Languages Known:\s*(.+)", text, re.DOTALL)
                languages = re.findall(r"-\s*(.+)", languages_section.group(1)) if languages_section else []

                return {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "address": address,
                    "linkedin": linkedin,
                    "github": github,
                    "profile_summary": summary,
                    "education": education,
                    "projects": projects,
                    "skills": skills,
                    "certifications": certifications,
                    "awards": awards,
                    "languages": languages
                }
            # Fix spacing issue in skills list
            skills = [" ".join(skill.split()) for skill in skills]

            # Extract details and update resume
            resume_data = extract_details(modified_content)
            resume_data = {k: v.replace("##", "").strip() if isinstance(v, str) else v for k, v in resume_data.items()}

            # Generate final resume from template
            updated_resume = generate_resume(selected_template_file, resume_data)
            print(resume_data)
        # Display PDF Preview in Streamlit
            st.markdown("### Resume Preview")
            pdf_viewer_html = f"""
                <iframe src="resume_final.pdf" width="100%" height="600px" style="border: none;"></iframe>
                """
            # Display Resume Preview
            st.components.v1.html(updated_resume,  height=500, scrolling=True)

            # Save HTML Preview
            with open("resume_preview.html", "w", encoding="utf-8") as file:
                file.write(updated_resume)

            # Convert to PDF
            pdf_filename = "resume_final.pdf"
            save_pdf(updated_resume, pdf_filename)

            # Provide Download Option
            with open(pdf_filename, "rb") as pdf_file:
                st.download_button(label="Download Resume", data=pdf_file, file_name="resume_final.pdf", mime="application/pdf")

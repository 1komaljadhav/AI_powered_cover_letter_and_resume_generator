import streamlit as st
import cohere
import os
import pdfkit

# Initialize Cohere API
COHERE_API_KEY = "uyRCRe0AwstpNh7hzjZR9Qz0MKqq94EbtBzFhlUj"  # Replace with your Cohere API key
co = cohere.Client(COHERE_API_KEY)

# Function to load HTML templates
def load_html_template(template_name):
    templates_folder = "cover_letter_templates"  # Folder where templates are stored
    template_path = os.path.join(templates_folder, template_name)
    with open(template_path, "r", encoding="utf-8") as file:
        return file.read()

# Function to render HTML with dynamic content
def render_html_template(template, cover_letter_content, full_name, email, phone):
    formatted_lines = "<br>".join(cover_letter_content.splitlines())  # Preserve line breaks in HTML
    return template.replace("{{ lines }}", formatted_lines)\
                   .replace("{{ full_name }}", full_name)\
                   .replace("{{ email }}", email)\
                   .replace("{{ phone }}", phone)

# Function to save HTML as PDF
def save_html_as_pdf(html_content, output_path):
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")  # Path to wkhtmltopdf
    pdfkit.from_string(html_content, output_path, configuration=config)

# Streamlit UI
def show():
    # Initialize session state variables
    if "cover_letter" not in st.session_state:
        st.session_state.cover_letter = ""
    if "edited_cover_letter" not in st.session_state:
        st.session_state.edited_cover_letter = ""
    if "show_preview" not in st.session_state:
        st.session_state.show_preview = False

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

        /* Highlight Styling */
        .highlight {
            background-color: #FFFFFF; /* White */
            color: #00ABE4; /* Bright Blue */
            padding: 2px 4px;
            border-radius: 3px;
        }

        /* Sidebar Styling */
        .sidebar .sidebar-content {
            background-color: #FFFFFF; /* White */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("📄 AI-Powered Cover Letter Generator")
    st.write("Fill in your details to generate a professional, tailored cover letter.")

    # Personal Information
    st.subheader("📌 Personal Information")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")

    # Hiring Manager & Company Details
    st.subheader("🏢 Company Details")
    company_name = st.text_input("Company Name")

    # Job Details
    st.subheader("💼 Job Details")
    job_description = st.text_area("Job Description")

    # Skills & Qualifications
    st.subheader("🎯 Skills & Qualifications")
    key_skills = st.text_area("Key Skills")
    education = st.text_input("Education")

    # Template Selection
    st.subheader("📄 Select a Template")
    template_options = ["Formal", "Creative", "Enthusiastic"]
    selected_template = st.selectbox("Select a Template", template_options)

    # Generate Cover Letter Button
    if st.button("Generate Content"):
        user_message = f"""
        Write a cover letter for the position of {job_description} at {company_name}.
        Include the following details:
        - Full Name: {full_name}
        - Email: {email}
        - Phone: {phone}
        - Key Skills: {key_skills}
        - Education: {education}

        The cover letter should be professional, concise, and tailored to the job description. Only 3 short paragraphs.
        """

        try:
            response = co.chat(
                message=user_message,
                chat_history=[],
                max_tokens=700,
                temperature=0.7
            )

            if hasattr(response, "text"):
                cover_letter = response.text.strip().replace("**", "")  # Clean Markdown formatting

                if not cover_letter or cover_letter.lower().startswith("dear hiring manager,"):
                    st.error("The generated cover letter seems incomplete. Please try again.")
                else:
                    st.session_state.cover_letter = cover_letter
                    st.session_state.edited_cover_letter = cover_letter  # Store initial version
                    st.success("Cover letter generated successfully! Edit if needed.")
            else:
                st.error("Failed to generate cover letter. Please try again.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Editing Section (if content exists)
    if "cover_letter" in st.session_state and st.session_state.cover_letter:
        st.subheader("✏️ Edit Your Cover Letter")
        st.session_state.edited_cover_letter = st.text_area("Edit your cover letter", value=st.session_state.edited_cover_letter, height=300)

        # Apply Changes Button
        if st.button("Confirm Changes"):
            st.session_state.cover_letter = st.session_state.edited_cover_letter  # Save edited version
            st.session_state.show_preview = True  # Enable preview
            st.success("Changes applied successfully!")

    # Preview and Download Section
    if st.session_state.show_preview:
        # Load the selected template
        if selected_template == "Formal":
            html_template = load_html_template("formal.html")
        elif selected_template == "Creative":
            html_template = load_html_template("creative.html")
        else:
            html_template = load_html_template("enthusiastic.html")

        # Render HTML with updated content
        final_html = render_html_template(
            html_template,
            st.session_state.cover_letter,
            full_name,
            email,
            phone
        )

        st.subheader("📄 Preview Your Cover Letter")
        st.components.v1.html(final_html, height=500, scrolling=True)

        # Save as PDF
        pdf_path = "cover_letter.pdf"
        save_html_as_pdf(final_html, pdf_path)

        # Provide a download button for the PDF
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                "📥 Download Cover Letter as PDF",
                pdf_file,
                file_name="cover_letter.pdf",
                mime="application/pdf"
            )

# Run Streamlit App
if __name__ == "__main__":
    show()

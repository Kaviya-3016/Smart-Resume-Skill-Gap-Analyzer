import streamlit as st
from PyPDF2 import PdfReader
import re
from fpdf import FPDF
from io import BytesIO



# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Resume Skill Gap Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("Smart Resume Skill Gap Analyzer")
st.subheader("AI-powered resume insights for career growth")
st.markdown("---")

# ---------------- JOB SKILLS DATA ----------------
job_skills = {
    "Data Analyst": [
        "python", "sql", "excel", "statistics", "power bi", "tableau",
        "data analysis", "data cleaning", "visualization"
    ],

    "Data Scientist": [
        "python", "pandas", "numpy", "statistics", "machine learning",
        "data analysis", "data visualization", "sql"
    ],

    "Machine Learning Engineer": [
        "python", "numpy", "pandas", "scikit-learn",
        "machine learning", "model training", "feature engineering"
    ],

    "AI Engineer": [
        "python", "machine learning", "deep learning",
        "tensorflow", "pytorch", "neural networks"
    ],

    "Web Developer": [
        "html", "css", "javascript", "react",
        "frontend", "backend", "api"
    ],

    "Backend Developer": [
        "python", "java", "node", "api",
        "database", "sql", "backend"
    ],

    "Frontend Developer": [
        "html", "css", "javascript", "react",
        "ui", "frontend", "responsive"
    ],

    "Software Engineer": [
        "python", "java", "oops",
        "data structures", "algorithms",
        "problem solving"
    ],

    "DevOps Engineer": [
        "linux", "docker", "kubernetes",
        "ci/cd", "cloud", "aws"
    ],

    "Cloud Engineer": [
        "aws", "azure", "gcp",
        "cloud", "deployment", "linux"
    ],

    "Business Analyst": [
        "excel", "sql", "power bi",
        "data analysis", "business requirements",
        "stakeholder"
    ],

    "Product Manager": [
        "roadmap", "analytics", "user research",
        "product strategy", "stakeholder",
        "communication"
    ],

    "UI/UX Designer": [
        "figma", "wireframe", "prototyping",
        "ui", "ux", "user research"
    ],

    "Cybersecurity Analyst": [
        "network security", "linux",
        "risk assessment", "security",
        "incident response"
    ],
    "Embedded Systems Engineer": [
        "c", "c++", "embedded systems", "microcontroller",
        "arm", "avr", "rtos", "uart", "spi", "i2c"
    ],

    "IoT Engineer": [
        "iot", "embedded systems", "arduino", "raspberry pi",
        "mqtt", "sensors", "cloud", "wifi", "bluetooth"
    ],

    "Electronics Design Engineer": [
        "analog electronics", "digital electronics",
        "circuit design", "pcb design",
        "proteus", "multisim", "altium"
    ],

    "VLSI Engineer": [
        "vlsi", "verilog", "system verilog",
        "digital design", "asic", "fpga"
    ],

    "FPGA Engineer": [
        "fpga", "verilog", "vhdl",
        "xilinx", "quartus", "timing analysis"
    ],

    "Robotics Engineer": [
        "robotics", "embedded systems",
        "sensors", "actuators",
        "ros", "control systems"
    ],

    "Control Systems Engineer": [
        "control systems", "pid",
        "state space", "matlab",
        "simulink"
    ],

    "Signal Processing Engineer": [
        "signal processing", "dsp",
        "fft", "filters",
        "matlab", "python"
    ],

    "Hardware Engineer": [
        "hardware design", "schematics",
        "pcb", "debugging",
        "oscilloscope", "multimeter"
    ],

    "Automotive Electronics Engineer": [
        "automotive electronics", "can",
        "lin", "embedded systems",
        "autosar", "microcontroller"
    ]
}

# ---------------- FUNCTIONS ----------------
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.lower()

def extract_skills_advanced(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return set(words)

def compare_skills(resume_skills, required_skills):
    matched = resume_skills.intersection(required_skills)
    missing = required_skills - resume_skills
    percentage = round((len(matched) / len(required_skills)) * 100, 2)
    return matched, missing, percentage

def generate_report(job_role, percentage, matched, missing):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Resume Analysis Report", ln=True)
    pdf.cell(200, 10, txt=f"Role: {job_role}", ln=True)
    pdf.cell(200, 10, txt=f"Match: {percentage}%", ln=True)

    pdf.cell(200, 10, txt="Matched Skills:", ln=True)
    pdf.multi_cell(0, 10, ", ".join(matched))

    pdf.cell(200, 10, txt="Missing Skills:", ln=True)
    pdf.multi_cell(0, 10, ", ".join(missing))

    # 👉 Convert to bytes instead of saving file
    pdf_output = pdf.output(dest='S').encode('latin-1')
    return BytesIO(pdf_output)

# ---------------- INPUT ----------------
input_mode = st.radio(
    "Choose input method:",
    ["📄 Upload PDF", "✍️ Enter Text Manually"]
)

resume_text = ""

if input_mode == "📄 Upload PDF":
    resume_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
    if resume_file:
        resume_text = extract_text_from_pdf(resume_file)
        st.success("Resume uploaded successfully!")

else:
    resume_text = st.text_area("Paste your resume text here", height=250)

# ---------------- JOB ROLE ----------------
job_role = st.selectbox("🎯 Select Target Job Role", list(job_skills.keys()))

# ---------------- INFO ----------------
st.markdown("### 🔍 What This App Does")

c1, c2, c3 = st.columns(3)

with c1:
    st.info("📄 Reads resumes like a recruiter")

with c2:
    st.warning("🧠 Finds missing skills")

with c3:
    st.success("🚀 Guides your career growth")

# ---------------- ANALYSIS ----------------
if st.button("🚀 Analyze Resume"):

    if not resume_text.strip():
        st.error("Please upload or paste resume.")
    else:
        required_skills = set(job_skills[job_role])
        resume_skills = extract_skills_advanced(resume_text)

        matched, missing, percentage = compare_skills(
            resume_skills, required_skills
        )

        st.markdown("---")
        st.subheader("📊 Analysis Dashboard")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Match Percentage", f"{percentage}%")

        with col2:
            st.metric("Missing Skills", len(missing))

        st.progress(percentage / 100)

        # -------- RESULTS --------
        st.markdown("### ✅ Matched Skills")
        st.success(", ".join(sorted(matched)) if matched else "None")

    st.markdown("### ❌ Missing Skills")
    st.error(", ".join(sorted(missing)) if missing else "None")

    # -------- REPORT DOWNLOAD --------
    report_file = generate_report(job_role, percentage, matched, missing)

    st.download_button(
        label="📄 Download Report",
        data=report_file,
        file_name="resume_analysis_report.pdf",
        mime="application/pdf"
    )

        # -------- FINAL MESSAGE --------
    if percentage >= 70:
        st.success("🎉 Excellent match!")
    elif percentage >= 40:
        st.warning("⚠️ Improve your skills")
    else:
        st.error("❗ Needs significant improvement")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("© 2026 Smart Resume Analyzer")


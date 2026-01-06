import streamlit as st

from PyPDF2 import PdfReader
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Resume Skill Gap Analyzer",
    page_icon="📄",
    layout="centered"
)


st.markdown(
    """
    <style>
    

    /* Page background gradient */
    .stApp {
        min-height: 100vh;
        background: linear-gradient(135deg, #ff9a9e 0%, #fbc2eb 25%, #a18cd1 50%, #8ec5fc 75%, #74ebd5 100%);
        background-attachment: fixed;
        background-size: cover;
    }

    /* Slight translucent layer to improve text contrast */
    .app-content {
        background: rgba(255,255,255,0.65);
        border-radius: 12px;
        padding: 0.6rem;
    }

    .main-title {
        font-size: 42px;
        font-weight: bold;
        color: #2b0a3d;
        text-align: center;
        margin-top: 10px;
    }
    .sub-title {
        font-size: 16px;
        color: #2b0a3d;
        text-align: center;
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        padding: 20px;
        color: #4B5563;
        font-size: 14px;
    }

    /* Ensure Streamlit built-in blocks don't add opaque backgrounds */
    .stBlock, .stContainer, .css-1l02zno, .css-18e3th9 {
        background: transparent !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">Smart Resume Skill Gap Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-powered resume insights for career growth</div>', unsafe_allow_html=True)
#st.markdown("---")
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

def extract_skills(resume_text):
    resume_text = resume_text.lower()
    extracted = set()

    for skills in job_skills.values():
        for skill in skills:
            if skill in resume_text:
                extracted.add(skill)

    return extracted

def compare_skills(resume_skills, required_skills):
    matched = resume_skills.intersection(required_skills)
    missing = required_skills - resume_skills
    percentage = round((len(matched) / len(required_skills)) * 100, 2)
    return matched, missing, percentage


# ---------------- INPUT SECTION ----------------
st.subheader("📥 Upload Resume")

resume_file = st.file_uploader(
    "Upload your resume (PDF only)",
    type=["pdf"]
)

resume_text = ""

if resume_file:
    resume_text = extract_text_from_pdf(resume_file)
    st.success("Resume uploaded and processed successfully!")

st.markdown("**OR**")

resume_text_manual = st.text_area(
    "✍️ Paste resume text manually",
    height=200
)

if resume_text_manual.strip():
    resume_text = resume_text_manual.lower()

#st.markdown("---")

job_role = st.selectbox(
    "🎯 Select Target Job Role",
    list(job_skills.keys())
)
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
        st.error("Please upload a PDF resume or paste resume text.")
    else:
        required_skills = set(job_skills[job_role])
        resume_skills = extract_skills(resume_text)

        matched, missing, percentage = compare_skills(
            resume_skills, required_skills
        )

        st.markdown("---")
        st.subheader("📊 Skill Match Result")

        st.metric(
            label="Skill Match Percentage",
            value=f"{percentage}%"
        )

        st.progress(percentage / 100)
        # -------- PIE CHART --------
        st.subheader("🥧 Skill Distribution")

        fig1, ax1 = plt.subplots()
        ax1.pie(
            [len(matched), len(missing)],
            labels=["Matched Skills", "Missing Skills"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax1.axis("equal")
        st.pyplot(fig1)
        # -------- BAR CHART --------
        st.subheader("📈 Skill-wise Breakdown")

        skill_labels = list(required_skills)
        skill_status = [
            1 if skill in matched else 0 for skill in skill_labels
        ]

        fig2, ax2 = plt.subplots()
        ax2.bar(skill_labels, skill_status)
        ax2.set_ylabel("Skill Presence (1 = Yes, 0 = No)")
        ax2.set_xticklabels(skill_labels, rotation=45, ha="right")
        st.pyplot(fig2)

         # -------- TEXT RESULTS --------

        st.markdown("### ✅ Matched Skills")
        if matched:
            st.success(", ".join(sorted(matched)))
        else:
            st.warning("No matching skills found.")

        st.markdown("### ❌ Missing Skills")
        if missing:
            st.error(", ".join(sorted(missing)))
        else:
            st.success("No missing skills. Excellent match!")

        st.markdown("### 📚 Suggested Skills to Learn")
        if missing:
            st.info(", ".join(sorted(list(missing)[:5])))

        if percentage >= 70:
            st.success("🎉 Great! Your resume matches well with this role.")
        elif percentage >= 40:
            st.warning("⚠️ Decent match, but improvement is recommended.")
        else:
            st.error("❗ Low match. Focus on building missing skills.")

# ---------------- FOOTER ----------------
st.markdown('---')
st.markdown(
    """
    <div class="footer">
        © 2026 Smart Resume Skill Gap Analyzer <br>
        Built with Python, Streamlit & Data Science Fundamentals
    </div>
    """,
    unsafe_allow_html=True
)

from flask import Flask, render_template, request
import os
import docx2txt
import PyPDF2

app = Flask(__name__)

SKILL_KEYWORDS = [
    "Python", "Java", "C++", "C", "C#", "HTML", "CSS", "JavaScript", "TypeScript",
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "NoSQL", "Oracle", "SQLite",
    "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask", "Spring Boot",
    "Git", "GitHub", "Docker", "Kubernetes", "Jenkins", "Linux", "Bash",
    "REST API", "GraphQL", "Firebase", "AWS", "Azure", "GCP",

    # AI, ML & Data Science
    "Machine Learning", "Deep Learning", "Data Science", "Data Analysis", "Big Data",
    "NLP", "Computer Vision", "TensorFlow", "Keras", "PyTorch", "Pandas", "NumPy",
    "Scikit-learn", "Matplotlib", "Seaborn", "Power BI", "Tableau", "Excel",

    # Mechanical Engineering
    "AutoCAD", "SolidWorks", "CATIA", "Fusion 360", "ANSYS", "MATLAB", "CREO",
    "3D Printing", "Mechanical Design", "Thermodynamics", "Fluid Mechanics",
    "HVAC", "Mechatronics", "Production Planning", "CAM", "CNC", "FEM", "CFD",

    # Electrical & Electronics
    "PLC", "SCADA", "Embedded Systems", "IoT", "Arduino", "Raspberry Pi",
    "Proteus", "MATLAB Simulink", "LabVIEW", "Multisim", "VLSI", "Verilog",
    "Power Systems", "Signal Processing", "Control Systems", "Circuit Design",

    # Civil Engineering
    "AutoCAD Civil 3D", "Revit", "STAAD Pro", "ETABS", "Primavera", "SAP2000",
    "Construction Planning", "Structural Design", "Quantity Surveying",
    "Geotechnical Engineering", "Surveying", "BIM", "Estimation and Costing",

    # Design & Creative Tools
    "Adobe Photoshop", "Adobe Illustrator", "Figma", "Canva", "Adobe XD",
    "UI/UX Design", "3D Modelling", "Sketch", "Wireframing", "Prototyping",

    # Common Soft Skills (optional)
    "Teamwork", "Leadership", "Communication", "Time Management", "Problem Solving",

    # Advanced CS/IT and Emerging Tech
    "Blockchain", "Cybersecurity", "Ethical Hacking", "DevOps", "Agile", "Scrum",
    "CI/CD", "Microservices", "System Design", "Responsive Design",
    "Cross-platform Development", "WebSockets", "API Integration", "WebAssembly",

    # Advanced Data Science & Analytics
    "Hadoop", "Spark", "Kafka", "Snowflake", "Databricks", "Looker", "Domo",
    "Jupyter", "Data Engineering", "Data Warehousing", "A/B Testing",
    "ETL", "Data Visualization", "Data Cleaning",

    # Mechanical Engineering - Expanded
    "DFMEA", "DVP&R", "Geometric Dimensioning & Tolerancing (GD&T)", "Moldflow",
    "Reliability Engineering", "Six Sigma", "Lean Manufacturing", "Kaizen",
    "Value Stream Mapping", "Material Science", "Robotics", "Pneumatics", "Hydraulics",
    "Energy Systems", "Kinematics", "Maintenance Planning",

    # Electrical & Electronics - Expanded
    "Embedded C", "Microcontrollers", "Signal Integrity", "PCB Design", "LTspice",
    "Electrical Wiring", "Power Electronics", "Smart Grid", "Renewable Energy",
    "IoT Protocols", "Wireless Communication", "Bluetooth", "ZigBee", "LoRaWAN",
    "Instrumentation", "Sensor Networks", "Power Distribution",

    # Civil Engineering - Expanded
    "Construction Management", "Green Building", "Smart City Planning", "Transportation Engineering",
    "Water Resources Engineering", "Hydrology", "Bridge Design", "Seismic Design",
    "Road Estimation", "Drainage System Design", "Wastewater Treatment",
    "Environmental Engineering", "Project Tendering", "Soil Mechanics",

    # Design & Creative - Expanded
    "After Effects", "InDesign", "Motion Graphics", "Typography", "Branding", "UI Animation",
    "Interaction Design", "Storyboarding", "Infographic Design",

    # Industrial / Production / Automobile Engineering
    "Industrial Engineering", "Logistics", "Supply Chain", "TQM", "Inventory Management",
    "Manufacturing Systems", "Assembly Line Design", "Kaizen", "Poka-Yoke", "Just-in-Time (JIT)",
    "Auto Electronics", "IC Engines", "Vehicle Dynamics", "CAD CAM CAE",

    # Biotechnology / Life Sciences
    "Bioinformatics", "Genetic Engineering", "Molecular Biology", "CRISPR", "DNA Sequencing",
    "PCR", "Gel Electrophoresis", "Microbiology", "Cell Culture", "Bioreactors",
    "Clinical Trials", "Pharmaceutical Analysis", "Spectrophotometry",

    # Management & Business Tools
    "SAP", "ERP", "Tally", "Zoho", "MS Project", "JIRA", "Confluence", "PowerPoint",
    "Business Intelligence", "Market Analysis", "Customer Journey Mapping",

    # Soft Skills / Workplace Tools
    "Technical Documentation", "Presentation Skills", "Public Speaking", "Remote Collaboration",
    "Critical Thinking", "Adaptability", "Interpersonal Skills", "Project Coordination",
    "Research & Development", "Innovation", "Mentorship"
]

def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(docx_file):
    return docx2txt.process(docx_file)

def extract_skills(text):
    text = text.lower()
    found_skills = [skill for skill in SKILL_KEYWORDS if skill.lower() in text]
    return found_skills

@app.route('/')
def home():
    return render_template('upload.html')  # Your custom upload.html file

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('resume')
    if not file:
        return "No file uploaded", 400

    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()

    if ext == '.pdf':
        text = extract_text_from_pdf(file)
    elif ext == '.docx':
        text = extract_text_from_docx(file)
    else:
        return "Unsupported file format. Please upload PDF or DOCX.", 400

    skills = extract_skills(text)
    return render_template('skills.html', skills=skills)

if __name__ == '__main__':
    app.run(debug=True)


import os
import re
import spacy
import pandas as pd
import pdfplumber

# Define the keywords and criteria for Software Testers
REQUIRED_SKILLS = {
    "testing_types": ["manual testing", "automation testing", "api testing", "performance testing", "regression testing",
                      "functional testing"],
    "tools": ["selenium", "postman", "jmeter", "testng"],
    "bug_tracking_tools": ["jira"],
    "programming_languages": ["java"],
    "methodologies": ["agile"]
}

# Load spaCy's English model for NER
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    """Extract text content from a PDF file."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return "".join([page.extract_text() for page in pdf.pages])
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None

def evaluate_resume(text, required_skills):
    """Evaluate the resume based on required skills."""
    matched_skills = {category: [] for category in required_skills}
    for category, keywords in required_skills.items():
        for keyword in keywords:
            if keyword.lower() in text.lower():
                matched_skills[category].append(keyword)
    return matched_skills

def score_resume(matched_skills):
    """Calculate a simple score based on matched skills."""
    total_keywords = sum(len(keywords) for keywords in REQUIRED_SKILLS.values())
    matched_keywords = sum(len(skills) for skills in matched_skills.values())
    return (matched_keywords / total_keywords) * 100

def extract_name_from_filename(filename):
    """
    Extract the name from the resume filename by removing 'resume' or 'cv' keywords.
    """
    name_without_extension = os.path.splitext(filename)[0]
    cleaned_name = re.sub(r"[\s_/-]*(resume|cv|pdf)[\s_/-]*", "", name_without_extension, flags=re.IGNORECASE)
    return ' '.join(cleaned_name.split()).title()

def extract_entities(text, filename=None):
    """
    Extract names, places, phone numbers, and email addresses from text.
    Optionally, extract name from filename if provided.
    """
    names = []
    if filename:
        name_from_filename = extract_name_from_filename(filename)
        if name_from_filename:
            names.append(name_from_filename)

    doc = nlp(text)
    locations = [ent.text for ent in doc.ents if ent.label_ == "GPE" and len(ent.text.split()) < 3]
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    phone_numbers = re.findall(r"(?:\+91[-.\s]?)?\d{10}", text)

    return {
        "names": list(set(names)),
        "locations": list(set(locations)),
        "emails": list(set(emails)),
        "phone_numbers": list(set(phone_numbers)),
    }

def save_to_spreadsheet(data, output_file):
    """Save extracted data to a spreadsheet."""
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)
    print(f"Data saved to {output_file}")

def get_pdf_files(directory):
    """Fetch all PDF files from the specified directory."""
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.lower().endswith(".pdf")]

def main():
    pdf_folder = "pdf"  # Adjust this path if necessary
    resumes = get_pdf_files(pdf_folder)
    if not resumes:
        print(f"No PDF files found in the folder: {pdf_folder}")
        return

    passed_resumes = []
    threshold_score = 50

    spreadsheet_data = {
        "File Name": [],
        "Names": [],
        "Locations": [],
        "Emails": [],
        "Phone Numbers": [],
        "Matched Skills": [],
        "Relevance Score (%)": []
    }

    for resume in resumes:
        print(f"\nEvaluating {resume}...")
        text = extract_text_from_pdf(resume)
        if text:
            matched_skills = evaluate_resume(text, REQUIRED_SKILLS)
            score = score_resume(matched_skills)
            extracted_entities = extract_entities(text, os.path.basename(resume))

            spreadsheet_data["File Name"].append(os.path.basename(resume))
            spreadsheet_data["Names"].append(", ".join(extracted_entities["names"]))
            spreadsheet_data["Locations"].append(", ".join(extracted_entities["locations"]))
            spreadsheet_data["Emails"].append(", ".join(extracted_entities["emails"]))
            spreadsheet_data["Phone Numbers"].append(", ".join(extracted_entities["phone_numbers"]))
            spreadsheet_data["Matched Skills"].append(str(matched_skills))
            spreadsheet_data["Relevance Score (%)"].append(score)

            print(f"Matched Skills: {matched_skills}")
            print(f"Relevance Score: {score:.2f}%")
            print(f"Extracted Entities: {extracted_entities}")

            if score >= threshold_score:
                print(f"{resume} is a good match!")
                passed_resumes.append(resume)
            else:
                print(f"{resume} does not meet the criteria.")
        else:
            print(f"Failed to evaluate {resume}.")

    save_to_spreadsheet(spreadsheet_data, "resume_evaluation_results1.xlsx")

    if passed_resumes:
        print("\nList of Passed Resumes:")
        for passed_resume in passed_resumes:
            print(f"- {passed_resume}")
    else:
        print("\nNo resumes passed the criteria.")

if __name__ == "__main__":
    main()

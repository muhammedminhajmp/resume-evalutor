Here's a `README.md` file you can use for your project:

```markdown
# Resume Evaluator

This project is a **Resume Evaluator** that helps individuals evaluate resumes. The application allows users to upload a PDF resume, and it processes the document to extract relevant information such as names, locations, emails, phone numbers, and evaluates the skills mentioned in the resume. It returns a relevance score based on the matched skills.

### Key Features:
- Upload one resume at a time.
- Extract relevant information: Names, Locations, Emails, and Phone Numbers.
- Evaluate skills against a predefined set of required skills.
- Provide a relevance score (percentage) based on the skills match.

### Limitations:
- **Name Extraction**: The method used for extracting names is not highly accurate.
- **Location Extraction**: If the resume contains multiple places, the system might extract more than one location. This can lead to false positives in certain cases.

### Prerequisites

To run this project locally, ensure you have the following installed:

- **Python 3.x**
- **pip** (Python package manager)
- **spaCy** (for Natural Language Processing)
- **flask** (for the backend API)

### Getting Started

Follow these steps to set up the project locally:

#### 1. Clone the Project
Clone the repository to your local machine:

```bash
git clone https://github.com/muhammedminhajmp/resume-evalutor.git
cd resume-evalutor
```

#### 2. Create a Virtual Environment
Create a Python virtual environment to isolate dependencies:

```bash
python -m venv venv
```

#### 3. Activate the Virtual Environment
- On **Windows**:
  ```bash
  venv\Scripts\activate
  ```

- On **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

#### 4. Install Dependencies
Install the required dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```

#### 5. Install SpaCy Model
The project uses **spaCy** for Natural Language Processing (NLP). You need to install the **`en_core_web_sm`** model for language processing.

```bash
python -m spacy download en_core_web_sm
```

### Running the Application Locally

1. Start the Flask server by running the following command in your terminal:

    ```bash
    python backend.py
    ```

2. Open your browser and navigate to `http://127.0.0.1:5000`. The application will load a page where you can upload a PDF resume for evaluation.

3. Once the resume is uploaded, the application will process the file, extract relevant information, evaluate the skills, and display the results, including a relevance score based on the matched skills.

### How the Application Works

1. **Upload Resume**: The user uploads a PDF resume through the frontend.
2. **Extract Text**: The backend extracts the text content from the PDF using `pdfplumber`.
3. **Evaluate Skills**: The backend evaluates the resume by checking the presence of predefined skills (testing types, tools, etc.) and calculates the relevance score.
4. **Extract Entities**: The backend uses spaCy to extract entities such as names, locations, emails, and phone numbers from the resume.
5. **Display Results**: The results are displayed on the frontend with information such as the file name, extracted entities, matched skills, and relevance score.

### File Structure

```
/resume-evaluator
├── backend.py            # Flask backend logic
├── requirements.txt      # Project dependencies
├── templates
│   ├── index.html        # Frontend for uploading resumes
├── uploads               # Temporary folder for uploaded files
├── README.md             # This file
```

### Dependencies

The following libraries are required:

- Flask
- spaCy
- pdfplumber
- werkzeug

You can install them using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Contributing

Feel free to fork the project and submit pull requests. If you have suggestions or improvements, please create an issue and we will review it!

### License

This project is open-source and available under the [MIT License](LICENSE).
```

### Explanation:
- **Prerequisites**: Describes what needs to be installed on the local machine to run the project.
- **Getting Started**: Details the steps to clone the project, set up the environment, and install dependencies.
- **Running the Application**: Explains how to run the application locally after the setup.
- **How the Application Works**: Describes the flow from uploading the resume to displaying the results.
- **File Structure**: Provides an overview of the file structure for clarity.
- **Dependencies**: Lists the necessary dependencies and how to install them.
- **Contributing**: Encourages contributions and suggests how others can get involved.

You can customize or expand this README as needed for your project.

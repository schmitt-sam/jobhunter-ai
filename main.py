import os
from agents.resume_generator import generate_tailored_resume, save_as_docx, sanitize_filename
from utils.pdf_parser import parse_all_resumes
from agents.job_description_extractor import extract_job_description_from_url

DEFAULT_RESUME_DIR = "C:/Users/samsc/OneDrive/Documents/Resume"
RESUME_OUTPUT_DIR = "output"

if __name__ == "__main__":
    print("=== AI Resume Generator: Phase 1 ===")
    url = input("Enter a job posting URL: ").strip()


    print("\n📥 Extracting job description...")
    job_description = extract_job_description_from_url(url)

    # Allow custom resume path
    custom_path = input(f"\nEnter full path to your resume folder, or press Enter to use default ({DEFAULT_RESUME_DIR}): ").strip()
    resume_path = custom_path if custom_path else DEFAULT_RESUME_DIR

    print(f"\n📂 Loading resume bullet points from: {resume_path}")
    bullet_points = parse_all_resumes(resume_path)

    print("\n🧠 Generating tailored resume using GPT-5 mini...")
    tailored_resume = generate_tailored_resume(job_description, bullet_points)

    company = input("Company name for output filename: ").strip()
    title = input("Job title for output filename: ").strip()

    filename = f"resume_{sanitize_filename(company)}_{sanitize_filename(title)}.docx"
    output_path = os.path.join(RESUME_OUTPUT_DIR, filename)
    os.makedirs(RESUME_OUTPUT_DIR, exist_ok=True)
    save_as_docx(tailored_resume, output_path)

    print(f"\n✅ Resume saved to: {output_path}")

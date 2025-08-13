import os
import fitz  # PyMuPDF

def parse_all_resumes(folder_path):
    """
    Parses all PDFs in the given folder and extracts bullet points from each.
    
    Args:
        folder_path (str): Path to the folder containing resume PDFs.
    
    Returns:
        list of str: A flat list of all bullet points extracted from all resumes.
    """
    bullet_points = []

    for fname in os.listdir(folder_path):
        if fname.endswith(".pdf"):
            file_path = os.path.join(folder_path, fname)
            try:
                with fitz.open(file_path) as doc:
                    text = ""
                    for page in doc:
                        text += page.get_text()
                    points = split_into_bullets(text)
                    bullet_points.extend(points)
            except Exception as e:
                print(f"❌ Failed to parse {fname}: {e}")
    
    return bullet_points

def split_into_bullets(text):
    """
    Splits text into bullet-point-like segments.
    
    Args:
        text (str): Full resume text.
    
    Returns:
        list of str: List of bullet-like statements.
    """
    lines = text.split("\n")
    bullets = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("•") or line.startswith("-") or line.startswith("*"):
            bullets.append(line[1:].strip())
        elif len(line.split()) > 5:  # filter out headers/footers
            bullets.append(line)

    return bullets

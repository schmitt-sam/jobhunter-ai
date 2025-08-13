from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_job_description_from_url(url: str) -> str:
    print("🌐 Launching headless browser...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Update this path to where chromedriver.exe is located
    service = Service(executable_path="C:/tools/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    print("🕸️ Fetching webpage...")
    driver.get(url)
    time.sleep(5)  # wait for page to load

    page_html = driver.page_source
    driver.quit()

    print("🤖 Using GPT-5 to extract job description...")
    return extract_description_with_ai(page_html)


def extract_description_with_ai(page_text: str) -> str:
    system_msg = (
        "You are an AI that reads job posting HTML and extracts the job description "
        "that lists the responsibilities and qualifications, ignoring all navigation or footer text. "
        "Return the result as clean plaintext, no formatting tags."
    )

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": page_text}
        ],
        max_completion_tokens=1000,
        temperature=1,
    )

    return response.choices[0].message.content.strip()


import os
import webbrowser
from urllib.parse import urlparse
from tkinter import filedialog


def open_website(url):
    url = url.strip()

    if not url:
        return False, "Please enter a website URL."

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed_url = urlparse(url)

    if not parsed_url.netloc or "." not in parsed_url.netloc:
        return False, "Please enter a valid website URL."

    if parsed_url.scheme not in ("http", "https"):
        return False, "Only HTTP and HTTPS websites are supported."

    try:
        opened = webbrowser.open_new_tab(url)

        if opened:
            return True, f"Website opened: {url}"

        return False, "Could not open the website."

    except Exception as error:
        return False, f"Website error: {error}"


def select_pdf():
    file_path = filedialog.askopenfilename(
        title="Select a PDF document",
        filetypes=[
            ("PDF Documents", "*.pdf"),
            ("All Files", "*.*")
        ]
    )

    if not file_path:
        return False, "No document selected."

    if not file_path.lower().endswith(".pdf"):
        return False, "Please select a PDF document."

    try:
        os.startfile(file_path)
        return True, f"PDF opened: {os.path.basename(file_path)}"

    except Exception as error:
        return False, f"Could not open PDF: {error}"

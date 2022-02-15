import pdfplumber

with pdfplumber.open("../data/test.py") as pdf:
    first_page = pdf.pages[0]
    x = [page.extract_text() for page in pdf.pages]
    full_str = (" ".join(x))
    print(full_str)

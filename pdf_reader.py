import pdfplumber

def get_text_from_pdf(path):

    with pdfplumber.open(path) as pdf:
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text = page.extract_text()
            return f"\n{text}\n"

# print(get_text_from_pdf("uploads/try.pdf"))

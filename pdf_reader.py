import pdfplumber

def get_text_from_pdf(path):
    content = ""
    with pdfplumber.open(path) as pdf:
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text = page.extract_text()
            content+=f"\n{text}\n"
    return content

# print(get_text_from_pdf("uploads/try.pdf"))

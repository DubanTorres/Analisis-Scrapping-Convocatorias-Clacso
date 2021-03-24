#!/usr/bin/env python
import pdfplumber

# extract text pdfs firts page
# cases argentina, colombia and mexico.

with pdfplumber.open(r'argentina.pdf') as pdf:
    firts_page = pdf.pages[0]
    print(firts_page.extract_text())

print('##################'+'\n')

with pdfplumber.open(r'colombia.pdf') as pdf:
    firts_page = pdf.pages[0]
    print(firts_page.extract_text())


print('##################'+'\n')

with pdfplumber.open(r'mexico.pdf') as pdf:
    firts_page = pdf.pages[0]
    print(firts_page.extract_text())

print('END OF EXTRACTION')

# it does work well.

# extract all text from one pdf. 
pdf = pdfplumber.open(r'colombia.pdf')
num_pages=len(pdf.pages)
pdf_str = ""
for i in range(num_pages):
    pdf_str+='\n'+str(pdf.pages[i].extract_text())

# it does work: catch punctuation, paragraphs, tables.

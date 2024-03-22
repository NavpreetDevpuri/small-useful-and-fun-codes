import os
from PyPDF2 import PdfReader, PdfWriter

def combine_pdfs(folder_path, output_filename):
    pdf_writer = PdfWriter()
    
    for item in sorted(os.listdir(folder_path)):
        if item.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, item)
            pdf_reader = PdfReader(pdf_path)
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)
    
    with open(output_filename, 'wb') as out:
        pdf_writer.write(out)

folder_path = '/Users/navpreetdevpuri/Downloads/Slides'  # Replace with the path to the folder containing your PDFs
output_filename = '/Users/navpreetdevpuri/Downloads/Slides/combined_pdf.pdf'  # The name of the output file

combine_pdfs(folder_path, output_filename)

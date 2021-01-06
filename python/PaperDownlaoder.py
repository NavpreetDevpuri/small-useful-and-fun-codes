from simplegmail import Gmail
from datetime import datetime
import time
from PyPDF2 import PdfFileReader, PdfFileWriter
import glob
import os
import magic

# from_date_and_time = "16/12/2020 13:00:00"
# to_date_and_time = "16/12/2020 16:00:00"
# save_folder_name = "bsc sem 5"

if not os.path.exists("client_secret.json"):
    client_secret = input("Enter client_secret json: ")
    with open("client_secret.json", "w") as f:
        f.write(client_secret)

print("Enter date and time (16/12/2020 13:00:00)")
from_date_and_time = input("Enter from: ")
to_date_and_time = input("Enter to: ")
save_folder_name = input("Folder name: ")


def _get_timestamp(date_and_time="16/12/2020 13:00:00"):
    return int(datetime.strptime(date_and_time, "%d/%m/%Y %H:%M:%S").timestamp())


class PaperDownloader:
    def __init__(self, after_date_and_time, before_date_and_time, save_dir="output"):
        self.gmail = Gmail()
        self.save_dir = save_dir
        self.messages = self.gmail.get_messages(
            query=f'after:{_get_timestamp(after_date_and_time)} '
                  f'before:{_get_timestamp(before_date_and_time)} '
                  f'has:attachment')
        os.makedirs(save_dir, exist_ok=True)
        i = 0
        for message in self.messages:
            i += 1
            print(f"{i}/{len(self.messages)} From: " + message.sender)
            if message.attachments:
                for attm in message.attachments:
                    if attm.filename.find(".pdf") != -1 or attm.filename.find(".PDF") != -1:
                        file_path = os.path.join(save_dir, attm.filename)
                        if os.path.exists(file_path):
                            attm.filename = f'{attm.filename.replace(".pdf", "").replace(".PDF", "")}'
                            attm.filename = f'{attm.filename}_{int(time.time())}.pdf'
                        else:
                            attm.filename = f'{attm.filename.replace(".pdf", "").replace(".PDF", "")}'
                            attm.filename = f'{attm.filename}.pdf'
                    file_path = os.path.join(save_dir, attm.filename)
                    attm.save(file_path)
                    print(f"   Downloaded: {file_path}")


PaperDownloader(from_date_and_time, to_date_and_time, save_folder_name)


def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)


pdfList = glob.glob(os.path.join(save_folder_name, "*.pdf"))
os.makedirs(save_folder_name + "_merged", exist_ok=True)
merge_pdfs(pdfList, output=f'{os.path.join(save_folder_name + "_merged", save_folder_name + "_merged.pdf")}')

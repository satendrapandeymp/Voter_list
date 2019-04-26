from pdf2image import convert_from_path
from glob import glob
import os

def decrypt(files):
    cmd = "qpdf --password='' --decrypt {0} {1}"
    for file in files:
        new_file = file.split(".")[0] + "_decrypted.pdf"
        os.system(cmd.format(file, new_file))

def base_name(name):
    return name.split("/")[-1].split(".")[0]

def check(name):
    if not os.path.exists(name):
        os.mkdir(name)

pdfs = glob("PDFs/*")
decrypt(pdfs)

pdfs = glob("PDFs/*_decrypted.pdf")

for pdf in pdfs:
    pages = convert_from_path(pdf)
    folder = base_name(pdf)
    check("Imgs/" + folder)
    name = "Imgs/" + folder + "/out{0}.jpg"
    for count, page in enumerate(pages):
        temp = name.format(count)
        page.save(temp, 'JPEG')



from PyPDF2 import PdfFileReader

"data/clusts.dot.pdf"
"clustnum_4.clustname_5.clusts.dot.pdf"
"clustnum_5.clustname_6.clusts.dot.pdf"

def get_pdf_file_size(pdf_fname):
  """Return pdf (width,height) in pixels."""
  pdf = PdfFileReader(open(pdf_fname,"rb"))
  mbox = pdf.getPage(0).mediaBox
  return mbox[2], mbox[3]

print get_pdf_file_size("data/clusts.dot.pdf")
print get_pdf_file_size("data/clustnum_6.clustname_7.clusts.dot.pdf")
print get_pdf_file_size("data/2.3.clusts.dot.pdf")

# HOW CAN I PLACE A PDF IN ANOTHER PDF?

pdf1 = PdfFileReader(open("data/clusts.dot.pdf","rb"))
pdf2 = PdfFileReader(open("data/clustnum_6.clustname_7.clusts.dot.pdf","rb"))

p = pdf1.getPage(0)

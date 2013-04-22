from PyPDF2 import PdfFileReader

"data/clusts.dot.pdf"
"data/clustnum_6.clustname_7.clusts.dot.pdf"
"data/2.3.clusts.dot.pdf"


def get_pdf_file_size(pdf_fname):
  """Return pdf (width,height) in pixels."""
  pdf = PdfFileReader(open(pdf_fname,"rb"))
  mbox = pdf.getPage(0).mediaBox
  return mbox[2], mbox[3]

print get_pdf_file_size("data/clusts.dot.pdf")
print get_pdf_file_size("data/clustnum_6.clustname_7.clusts.dot.pdf")
print get_pdf_file_size("data/2.3.clusts.dot.pdf")

"""Export figures/pipeline-v10.pptx to PDF via PowerPoint COM, then render
the PDF to PNG at high DPI for inspection."""
import os
import sys

import fitz
import win32com.client

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PPTX = os.path.abspath("figures/pipeline-v10.pptx")
PDF = os.path.abspath("figures/pipeline-v10.pdf")
PNG = os.path.abspath("figures/pipeline-v10.png")

app = win32com.client.Dispatch("PowerPoint.Application")
pres = app.Presentations.Open(PPTX, WithWindow=False)
pres.SaveAs(PDF, 32)          # ppSaveAsPDF
pres.Close()
app.Quit()
print("pdf written:", PDF)

doc = fitz.open(PDF)
print("pdf pages:", doc.page_count)
page = doc[0]
pix = page.get_pixmap(dpi=300)
pix.save(PNG)
print("png:", PNG, pix.width, "x", pix.height)

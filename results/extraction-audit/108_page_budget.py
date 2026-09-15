"""FSE 2027 page budget: counted text+figures pages vs the 18-page cap.

CFP: at most 18 pages of text and figures, plus up to 4 pages of references.
The Data Availability section is exempt; there is no appendix exemption.

Method. The page that holds the end of the body is located: the last text line
above the "Data Availability" heading (that section is exempt) or above the
"References" heading when no Data Availability section is present. Everything
before that page counts in full; that page counts for the fraction of its text
frame the body occupies. References are everything after.

Usage:  py results/extraction-audit/108_page_budget.py [pdf]
Default pdf: TestVDB-v10.pdf
"""
import sys

import fitz  # pymupdf

PDF = sys.argv[1] if len(sys.argv) > 1 else "TestVDB-v10.pdf"
CAP_TEXT = 18.0
CAP_REFS = 4.0
EXEMPT_HEADING = "Data Availability"
REFS_HEADING = "References"


def text_frame(doc):
    """Estimate the text frame from the page with the highest content."""
    top = min(b[1] for b in doc[0].get_text("blocks") if b[4].strip())
    bottom = 0.0
    for i in range(doc.page_count):
        blocks = [b for b in doc[i].get_text("blocks") if b[4].strip()]
        if blocks:
            bottom = max(bottom, max(b[3] for b in blocks))
    return top, bottom


def heading_y(doc, wanted):
    """First (page, y) at which `wanted` is the first line of a block."""
    for i in range(doc.page_count):
        for blk in doc[i].get_text("blocks"):
            if blk[4].strip().split("\n")[0].strip() == wanted:
                return i + 1, blk[1]
    return None, None


def main():
    doc = fitz.open(PDF)
    n = doc.page_count
    frame_top, frame_bottom = text_frame(doc)
    height = frame_bottom - frame_top

    ex_page, ex_y = heading_y(doc, EXEMPT_HEADING)
    refs_page, _ = heading_y(doc, REFS_HEADING)
    if refs_page is None:
        print("References heading not found; cannot measure.")
        return 1

    # the first page on which the counted body stops
    stop_page = ex_page if ex_page else refs_page
    stop_limit = ex_y if ex_page else heading_y(doc, REFS_HEADING)[1]

    # last counted line above the limit, on that page or an earlier one
    last_y, last_page = None, None
    for i in range(stop_page - 1, -1, -1):
        ys = [b[3] for b in doc[i].get_text("blocks")
              if b[4].strip() and (i + 1 < stop_page or b[3] < stop_limit - 1)]
        if ys:
            last_y, last_page = max(ys), i + 1
            break
    if last_y is None:
        print("No body text found above the headings; cannot measure.")
        return 1

    counted = (last_page - 1) + (last_y - frame_top) / height
    refs_pages = n - counted

    print("pdf            :", PDF)
    print("total pages    :", n)
    print("text frame     : y %.1f .. %.1f (height %.1f pt)" % (frame_top, frame_bottom, height))
    print("exempt section : %s on page %s at y=%s" % (EXEMPT_HEADING, ex_page, ex_y))
    print("references on  : page", refs_page)
    print("body ends      : page %d at y=%.1f" % (last_page, last_y))
    print()
    print("COUNTED text+figures: %.2f  (cap %.0f)  -> %s"
          % (counted, CAP_TEXT, "OK" if counted <= CAP_TEXT else "OVER"))
    print("REFERENCES pages    : %.2f  (cap %.0f)  -> %s"
          % (refs_pages, CAP_REFS, "OK" if refs_pages <= CAP_REFS else "OVER"))
    print("HEADROOM            : %.2f pages of text" % (CAP_TEXT - counted))
    return 0


if __name__ == "__main__":
    sys.exit(main())

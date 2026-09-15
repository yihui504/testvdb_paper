"""FSE 2027 page budget: counted text+figures pages vs the 18-page cap.

CFP: at most 18 pages of text and figures, plus up to 4 pages of references.
The Data Availability section is exempt; there is no appendix exemption.

Method. The text frame is measured on a page that is full of body text (the page
whose content runs from the highest top to the lowest bottom), not on the title
page, whose first block sits lower. The page holding the end of the body is then
located -- the last text line above the "Data Availability" heading (exempt) or
above the "References" heading -- and everything before that page counts in
full while that page counts for the fraction of the frame the body occupies.
References are everything after.
"""
import sys

import fitz  # pymupdf

PDF = sys.argv[1] if len(sys.argv) > 1 else "TestVDB-v10.pdf"
CAP_TEXT = 18.0
CAP_REFS = 4.0
EXEMPT_HEADING = "Data Availability"
REFS_HEADING = "References"


# The running head (the paper title, or the copyright line) sits in the top
# margin, ABOVE the first body line. Counting it as body overstates the budget
# by a fraction of a page and, worse, mis-reads a page whose only non-heading
# block is the head. Body text begins at the line-number gutter's first entry,
# which is never inside the head band.
HEAD_BAND = 80.0  # pt; the head spans roughly y 57-76, body starts at ~87


FOOT_BAND = 672.0  # pt; the footer rule and imprint run below this


def body_blocks(page):
    return [b for b in page.get_text("blocks")
            if b[4].strip() and HEAD_BAND <= b[1] < FOOT_BAND]


def text_frame(doc):
    """The text frame: the topmost and the bottom-most body line, over all pages.

    NOT the extents of the page carrying the most body text. That page is the
    one whose own span is largest, which is not the same as the page whose first
    line sits highest and the page whose last line sits lowest -- the frame's
    two edges fall on different pages, since a page opening on a section heading
    starts lower and a page ending a paragraph stops higher. Reading the frame
    off one page understates its height, and the understatement lands directly
    in the counted fraction, which is why the frame is the min and the max.
    """
    tops, bottoms = [], []
    for i in range(doc.page_count):
        blocks = body_blocks(doc[i])
        if not blocks:
            continue
        tops.append(min(b[1] for b in blocks))
        bottoms.append(max(b[3] for b in blocks))
    return min(tops), max(bottoms)


def heading_y(doc, wanted):
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

    stop_page = ex_page if ex_page else refs_page
    stop_limit = ex_y if ex_page else heading_y(doc, REFS_HEADING)[1]

    last_y = last_page = None
    for i in range(stop_page - 1, -1, -1):
        ys = [b[3] for b in body_blocks(doc[i])
              if i + 1 < stop_page or b[3] < stop_limit - 1]
        if ys:
            last_y, last_page = max(ys), i + 1
            break
    if last_y is None:
        print("No body text found above the headings; cannot measure.")
        return 1

    counted = (last_page - 1) + (last_y - frame_top) / height
    refs_pages = n - counted

    print("pdf            :", PDF)
    # The reading depends on the interpreter: two Pythons on this machine differ
    # in PyMuPDF version and segment text blocks differently, which moves the
    # frame and the counted fraction. Print both so a reading is attributable to
    # the tool that produced it.
    print("interpreter    : %s %s  (PyMuPDF %s)"
          % (sys.executable, sys.version.split()[0], fitz.version[0]))
    print("total pages    :", n)
    print("text frame     : y %.1f .. %.1f (height %.1f pt)" % (frame_top, frame_bottom, height))
    print("exempt section : %s on page %s" % (EXEMPT_HEADING, ex_page))
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

"""
copy_and_verify_pitch_deck.py
Copies the 6-slide presentation PDF to submission_pdfs/Pitch_Deck.pdf and exports PNG previews.
"""

import os
import shutil
import pymupdf

source_pdf = r"c:\Seva Sankalp Hackathon\AMR Sentinel\PPT\AMR_Sentinel_Winning_Pitch_Deck.pdf"
target_pdf = r"c:\Seva Sankalp Hackathon\AMR Sentinel\submission_pdfs\Pitch_Deck.pdf"

if not os.path.exists(source_pdf):
    source_pdf = r"c:\Seva Sankalp Hackathon\AMR Sentinel\AMR_Sentinel_Hackathon_Presentation_6Pages.pdf"

shutil.copyfile(source_pdf, target_pdf)
print(f"Copied {source_pdf} -> {target_pdf} ({os.path.getsize(target_pdf)} bytes)")

doc = pymupdf.open(target_pdf)
print(f"Pitch_Deck.pdf has {len(doc)} pages.")

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    img_path = rf"c:\Seva Sankalp Hackathon\AMR Sentinel\submission_pdfs\pitch_deck_p{i+1}.png"
    pix.save(img_path)
    print(f"Saved {img_path} ({pix.width}x{pix.height})")

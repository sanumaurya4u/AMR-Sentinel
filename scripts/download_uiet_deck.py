"""
download_uiet_deck.py
Downloads the 10-slide UIET MDU pitch deck from Canva, saves PDF & PPTX, and renders preview PNGs.
"""

import os
import urllib.request
import pymupdf

pdf_url = "https://export-download.canva.com/ZcQTY/DAHbBEZcQTY/-1/0-86090680996569527.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH4R7NKVBA%2F20261115%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20261115T131819Z&X-Amz-Expires=34873&X-Amz-Signature=d6544ae175c0cf71deed80136e986870ea9620b419e7b6121e6a51b8950031e4&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Sun%2C%2015%20Nov%202026%2022%3A59%3A32%20GMT"
pptx_url = "https://export-download.canva.com/ZcQTY/DAHbBEZcQTY/-1/3449153706762592289.pptx?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH4R7NKVBA%2F20261115%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20261115T093429Z&X-Amz-Expires=47645&X-Amz-Signature=b8963e2c5776e19871318e29468a6c77df6134af72bb4569e038146cba027b6e&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Sun%2C%2015%20Nov%202026%2022%3A48%3A34%20GMT"

target_dir = r"c:\Seva Sankalp Hackathon\AMR Sentinel\submission_pdfs"
os.makedirs(target_dir, exist_ok=True)

pdf_dest = os.path.join(target_dir, "AMR_Sentinel_UIET_Pitch_Deck.pdf")
pptx_dest = os.path.join(target_dir, "AMR_Sentinel_UIET_Pitch_Deck.pptx")
pitch_deck_main = os.path.join(target_dir, "Pitch_Deck.pdf")

print("Downloading 10-slide PDF from Canva...")
urllib.request.urlretrieve(pdf_url, pdf_dest)
print(f"Downloaded PDF: {pdf_dest} ({os.path.getsize(pdf_dest)} bytes)")

print("Downloading 10-slide PPTX from Canva...")
urllib.request.urlretrieve(pptx_url, pptx_dest)
print(f"Downloaded PPTX: {pptx_dest} ({os.path.getsize(pptx_dest)} bytes)")

# Update main Pitch_Deck.pdf as well
import shutil
shutil.copyfile(pdf_dest, pitch_deck_main)
print(f"Updated main {pitch_deck_main}")

# Convert each slide to PNG
doc = pymupdf.open(pdf_dest)
print(f"Canva PDF has {len(doc)} pages.")

preview_dir = os.path.join(target_dir, "uiet_slides_preview")
os.makedirs(preview_dir, exist_ok=True)

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    img_path = os.path.join(preview_dir, f"slide_{i+1}.png")
    pix.save(img_path)
    print(f"Saved slide {i+1}: {img_path} ({pix.width}x{pix.height})")

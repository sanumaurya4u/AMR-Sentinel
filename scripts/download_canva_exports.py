"""
download_canva_exports.py
Downloads the exported PDF and PPTX from Canva and renders each page as a PNG for inspection.
"""

import os
import urllib.request
import pymupdf

pdf_url = "https://export-download.canva.com/ZDE7c/DAHbBIZDE7c/-1/0-6543126646788273994.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH4R7NKVBA%2F20261114%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20261114T220132Z&X-Amz-Expires=88010&X-Amz-Signature=ec0d968737ca214dbf185057680605606862e69c5ce4cb6946e3dbc2bd187d6f&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Sun%2C%2015%20Nov%202026%2022%3A28%3A22%20GMT"
pptx_url = "https://export-download.canva.com/ZDE7c/DAHbBIZDE7c/-1/3165426923532176239.pptx?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH4R7NKVBA%2F20261115%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20261115T115408Z&X-Amz-Expires=37798&X-Amz-Signature=797d56c5a09caff6c47785b7bc243bcd8ef9d222c937098983817e4f27a71e1f&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Sun%2C%2015%20Nov%202026%2022%3A24%3A06%20GMT"

target_dir = r"c:\Seva Sankalp Hackathon\AMR Sentinel\submission_pdfs"
os.makedirs(target_dir, exist_ok=True)

pdf_dest = os.path.join(target_dir, "AMR_Sentinel_Canva_Pitch_Deck.pdf")
pptx_dest = os.path.join(target_dir, "AMR_Sentinel_Canva_Pitch_Deck.pptx")

print("Downloading PDF from Canva...")
urllib.request.urlretrieve(pdf_url, pdf_dest)
print(f"Downloaded PDF: {pdf_dest} ({os.path.getsize(pdf_dest)} bytes)")

print("Downloading PPTX from Canva...")
urllib.request.urlretrieve(pptx_url, pptx_dest)
print(f"Downloaded PPTX: {pptx_dest} ({os.path.getsize(pptx_dest)} bytes)")

# Convert each page to PNG for visual inspection
doc = pymupdf.open(pdf_dest)
print(f"Canva PDF has {len(doc)} pages.")

canva_preview_dir = os.path.join(target_dir, "canva_slides_preview")
os.makedirs(canva_preview_dir, exist_ok=True)

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    img_path = os.path.join(canva_preview_dir, f"slide_{i+1}.png")
    pix.save(img_path)
    print(f"Saved slide {i+1} preview: {img_path} ({pix.width}x{pix.height})")

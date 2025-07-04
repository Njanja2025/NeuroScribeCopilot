def detect_text_blocks(pdf_path):
    import fitz  # PyMuPDF
    doc = fitz.open(pdf_path)
    text_blocks = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        bbox = span["bbox"]
                        font = span["font"]
                        size = span["size"]
                        text_blocks.append({
                            "page": page_num,
                            "text": text,
                            "bbox": bbox,
                            "font": font,
                            "size": size
                        })
    return text_blocks
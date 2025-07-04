def edit_text_block(text_data, edited_text, bbox):
    # Logic to edit the text block
    text_data["edited_text"] = edited_text
    return text_data

def erase_text_block(text_data, bbox):
    # Logic to erase the text block by filling it with white
    text_data["edited_text"] = " "  # Replace with a space or empty string
    return text_data

def apply_edits_to_pdf(doc, edited_data):
    for item in edited_data:
        page = doc.load_page(item["page"])
        x0, y0, x1, y1 = item["bbox"]
        page.insert_text((x0, y0),
                         item["edited_text"],
                         fontsize=item["size"],
                         fontname=item["font"])
    return doc
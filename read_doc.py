import zipfile
import xml.etree.ElementTree as ET

ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def is_heading_section(p, style):
    """Returns True if the given paragraph section has been styled with the specified style"""
    heading_style_elem = p.find(f".//w:pStyle[@w:val='{style}']", ns)
    return heading_style_elem is not None

def get_section(p):
    """Returns the joined text of the text elements under the given paragraph tag"""
    return_val = ''
    text_elems = p.findall('.//w:t', ns)
    if text_elems is not None:
        return_val = ''.join([t.text for t in text_elems])
    return return_val

def get_section_text(p_sections):
    section_text = []
    title = ""
    text = []
    paragraph_num = 1

    for p in p_sections:
        if is_heading_section(p, 'Heading1') or is_heading_section(p, 'Heading2'):
            if title and text:
                section_text.append({'title': title, 'text': text})
                text = []
                paragraph_num += 1
            
            #title = f"{get_section(p)} (Paragraph {paragraph_num})"
            title = get_section(p)
        else:
            text.append(get_section(p))

    if title and text:
        section_text.append({'title': title, 'text': text})

    return section_text

def get_section_paragraph(section_text):
    section_paragraph = {}

    for section in section_text:
        title = section["title"]
        text = section["text"]
        paragraph = "\n\n".join(text)
        section_paragraph[title] = paragraph

    return section_paragraph

def read_doc(uploaded_file):
    with zipfile.ZipFile(uploaded_file) as zip_file:
        doc = zip_file.read('word/document.xml')
        root = ET.fromstring(doc)

        body = root.find('w:body', ns)
        p_sections = body.findall('w:p', ns)

        section_text = get_section_text(p_sections)
        section_paragraph = get_section_paragraph(section_text)

    return section_paragraph

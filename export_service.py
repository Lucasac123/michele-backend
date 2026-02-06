import svgwrite
import os

def create_svg(assets_data: dict, text_content: str, output_path: str):
    # Standard Corel page size or just a generic canvas?
    # Let's go with 500x500px for now, or use asset dimensions if known
    # Corel handles units well.
    
    dwg = svgwrite.Drawing(output_path, profile='tiny', size=('500px', '500px'))
    
    # 1. Background
    bg = assets_data.get('background')
    if bg and bg.get('file_path'):
        # For simplicity, we reference the file. 
        # CAUTION: Local file links in SVG might break if moved. 
        # Embedding is safer but larger. 
        # For this "Local App", absolute paths might work if opened on same PC, 
        # but relative paths are better if we bundle.
        # Corel usually embeds on import or asks.
        # Let's try embedding (base64) or absolute path for local usage.
        # Using absolute path for "Michele's PC" scenario.
        dwg.add(dwg.image(href=f"file:///{bg['file_path'].replace(os.sep, '/')}", insert=(0, 0), size=('500px', '500px')))

    # 2. Frame
    frame = assets_data.get('frame')
    if frame and frame.get('file_path'):
         dwg.add(dwg.image(href=f"file:///{frame['file_path'].replace(os.sep, '/')}", insert=(0, 0), size=('500px', '500px')))

    # 3. Text
    if text_content:
        # Centered text
        dwg.add(dwg.text(text_content, insert=('250px', '250px'), text_anchor="middle", font_family="Arial", font_size="24px", fill="black"))

    dwg.save()
    return output_path

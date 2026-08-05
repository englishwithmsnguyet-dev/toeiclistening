import json
import re

with open("data/part01_data.js", "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find("[")
end_idx = content.rfind("]") + 1
data = json.loads(content[start_idx:end_idx])

for section in data:
    if section["id"] == "dang_01":
        for slide in section.get("theory", []):
            if not slide.get("text"): continue
            html = slide["text"][0]
            
            # Slide with slide_116_img_5.jpg and slide_116_img_6.png (Customers vs Employees)
            if "slide_116_img_5.jpg" in html:
                # Left image: Employees working. Right image: Customers at market.
                # Currently: Left has "some customers" + "một vài nhân viên". Right has "some employees" + "một vài khách hàng".
                # We need to change Left to "some employees" + "một vài nhân viên".
                # We need to change Right to "some customers" + "một vài khách hàng".
                
                # Replace exact strings to fix the mismatch.
                # Left column fixing (it has 'data-text="some customers"' and 'some customers' but should be 'some employees')
                html = html.replace('<strong>some customers</strong>', '<strong>some employees_TEMP</strong>')
                html = html.replace('data-text="some customers"', 'data-text="some employees_TEMP"')
                
                # Right column fixing
                html = html.replace('<strong>some employees</strong>', '<strong>some customers</strong>')
                html = html.replace('data-text="some employees"', 'data-text="some customers"')
                
                # Finalize left column
                html = html.replace('some employees_TEMP', 'some employees')
                
                slide["text"][0] = html

            # Slide with slide_117_img_5.jpg and slide_117_img_6.jpg (Vendors vs Passengers)
            elif "slide_117_img_5.jpg" in html:
                # Left image: Airport passengers (currently has text "some vendors / một vài người bán dạo")
                # Right image: Street food vendors (currently has text "some passengers / một vài hành khách")
                # We just swap the text blocks entirely.
                
                # The text blocks look like:
                # <div style="margin-bottom: 12px; font-size: 1.3rem;"><span style="color: #0070C0;"><strong>some vendors</strong></span> ...</div><div style="margin-bottom: 12px; font-size: 1.3rem;"><strong>một</strong><strong> </strong><strong>vài</strong><strong> </strong><strong>người</strong><strong> </strong><strong>bán</strong><strong> </strong><strong>dạo</strong></div>
                
                # Let's just swap the images! It's much safer and easier.
                # Wait, swapping images means Left = Vendors, Right = Passengers.
                # Is that okay? Yes!
                html = html.replace('slide_117_img_5.jpg', 'slide_117_img_TEMP.jpg')
                html = html.replace('slide_117_img_6.jpg', 'slide_117_img_5.jpg')
                html = html.replace('slide_117_img_TEMP.jpg', 'slide_117_img_6.jpg')
                
                slide["text"][0] = html

new_content = "window.part01Data = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"
with open("data/part01_data.js", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Done fixing swapped text/images.")

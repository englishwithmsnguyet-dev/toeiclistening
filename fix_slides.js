const fs = require('fs');
let content = fs.readFileSync('data/part01_data.js', 'utf8');

// The file starts with window.part01Data = [ ... ]
// We need to parse it, modify it, and write it back.
// Since it's a JS file, we can eval it (or just slice the JSON part).
let jsonStr = content.substring(content.indexOf('['), content.lastIndexOf(']') + 1);
let data = JSON.parse(jsonStr);

// A mapping for the problematic slides
// mapping[slide_index] = { left: [text lines], right: [text lines], images: [left_img, right_img] }
const fixes = {
    14: { left: ["adjusting a microphone", "điều chỉnh mi-crô"], right: ["adjusting a chair", "điều chỉnh cái ghế"], images: ["slide_14_img_5.jpg", "slide_14_img_6.png"] },
    17: { left: ["approaching the front desk", "tiến lại gần quầy lễ tân"], right: ["approaching the cash register", "tiến lại gần quầy tính tiền"], images: ["slide_17_img_6.jpg", "slide_17_img_7.jpg"] }, // Note: Front desk is left image (6), cash register is right image (7)
    20: { left: ["carrying a briefcase", "mang cặp tài liệu"], right: ["carrying a jacket", "mang chiếc áo khoác"], images: ["slide_20_img_6.jpg", "slide_20_img_7.jpg"] },
    23: { left: ["checking a schedule", "kiểm tra lịch làm việc"], right: ["checking documents", "kiểm tra tài liệu"], images: ["slide_23_img_6.jpg", "slide_23_img_7.jpg"] },
    26: { left: ["entering an amusement park", "tiến vào công viên giải trí"], right: ["entering a building", "tiến vào toà nhà"], images: ["slide_26_img_6.jpg", "slide_26_img_7.jpg"] },
    29: { left: ["hanging a picture", "treo một bức tranh"], right: ["hanging a clock", "treo một chiếc đồng hồ"], images: ["slide_29_img_6.jpg", "slide_29_img_7.jpg"] },
    32: { left: ["holding a book", "cầm một cuốn sách"], right: ["holding a pen", "cầm một chiếc bút"], images: ["slide_32_img_6.jpg", "slide_32_img_7.jpg"] },
    35: { left: ["leaning against the wall", "tựa vào bức tường"], right: ["leaning against the railing", "tựa vào lan can"], images: ["slide_35_img_6.jpg", "slide_35_img_7.png"] },
    38: { left: ["looking at a monitor", "nhìn vào màn hình"], right: ["looking at a map", "nhìn vào bản đồ"], images: ["slide_38_img_6.jpg", "slide_38_img_7.jpg"] },
    41: { left: ["reaching for a book", "với lấy một cuốn sách"], right: ["reaching for an item", "với lấy một món đồ"], images: ["slide_41_img_6.jpg", "slide_41_img_7.jpg"] }
};

// Process all sections and theories
for (let section of data) {
    if (section.theory) {
        for (let slide of section.theory) {
            if (fixes[slide.slide_index]) {
                let fix = fixes[slide.slide_index];
                
                // Build a custom HTML block in slide.text
                let html = `<div style="display: flex; flex-direction: row; gap: 32px; justify-content: center; width: 100%; align-items: flex-start; margin-top: 10px;">
                    <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
                        <img src="data/graphics/part01/${fix.images[0]}" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
                        <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
                            ${fix.left.map(t => `<div style="margin-bottom: 8px;">${t}</div>`).join('')}
                        </div>
                    </div>
                    <div style="flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start;">
                        <img src="data/graphics/part01/${fix.images[1]}" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); margin-bottom: 24px;">
                        <div style="font-size: 1.3rem; line-height: 1.8; color: var(--text-main);">
                            ${fix.right.map(t => `<div style="margin-bottom: 8px;">${t}</div>`).join('')}
                        </div>
                    </div>
                </div>`;
                
                slide.text = [html];
                slide.images = []; // Clear images so app.js doesn't double-render
            }
        }
    }
}

// Write back
fs.writeFileSync('data/part01_data.js', 'window.part01Data = ' + JSON.stringify(data, null, 2) + ';');
console.log('Successfully updated part01_data.js');

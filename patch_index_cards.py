import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make sure all dashboard cards look correct initially (Part 1 is unlocked, but we'll let it show normal, not "locked" class by default, so they can click it. Wait, actually Part 2, 3, 4 are locked initially, so they SHOULD have the "locked" class!)

# Part 1: Change to unlocked
old_part1 = """<div class="dashboard-card locked" id="card-part1">
                            <div class="card-icon">
                                <svg viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
                            </div>
                            <h3>PART 01 - PHOTOGRAPHS</h3>
                            <p>Mô tả tranh ảnh. Luyện kỹ năng quan sát tranh và chọn câu mô tả chính xác nhất.</p>
                            <span class="status-tag coming-soon">ĐANG CẬP NHẬT</span>
                        </div>"""
# Wait, I don't know the exact HTML of Part 1 card because it didn't have an ID in the original file I dumped?

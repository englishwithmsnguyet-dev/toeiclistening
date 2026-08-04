import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Password Modal right before <script src="data/part01_data.js?v=1.0.0"></script>
modal_html = """
    <!-- PASSWORD MODAL -->
    <div id="password-modal" class="modal-overlay hidden" style="z-index: 10001; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(9, 8, 18, 0.85); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px); display: flex; align-items: center; justify-content: center; opacity: 0; pointer-events: none; transition: opacity 0.3s ease;">
        <div class="glass-panel" style="max-width: 400px; width: 90%; padding: 40px; text-align: center; border: 1px solid var(--border); box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);">
            <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #ef4444, #f97316); display: flex; align-items: center; justify-content: center; margin: 0 auto 24px auto; color: white; border-radius: 50%; box-shadow: 0 0 20px rgba(239, 68, 68, 0.4);">
                <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
            </div>
            <h2 style="font-size: 1.6rem; margin-bottom: 12px; font-weight: 800; color: var(--text-main);">NỘI DUNG ĐÃ KHÓA</h2>
            <p style="color: var(--text-muted); font-size: 1rem; line-height: 1.6; margin-bottom: 24px;">Vui lòng nhập mật khẩu (2026) để truy cập.</p>
            
            <div style="position: relative; margin-bottom: 20px;">
                <input type="password" id="passwordInput" placeholder="Nhập mật khẩu..." style="width: 100%; padding: 14px 16px; background: rgba(0, 0, 0, 0.2); border: 1px solid var(--border); color: var(--text-main); font-size: 1.05rem; outline: none; transition: border-color 0.2s; text-align: center; border-radius: 8px;" />
                <div id="passwordError" style="color: var(--danger); font-size: 0.85rem; margin-top: 8px; display: none;">Mật khẩu không chính xác!</div>
            </div>
            
            <div style="display: flex; gap: 12px; justify-content: center;">
                <button class="btn" id="cancelPasswordBtn" style="padding: 12px 24px; font-size: 1rem; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: var(--text-main);">Hủy</button>
                <button class="btn btn-primary" id="submitPasswordBtn" style="padding: 12px 24px; font-size: 1rem; border-radius: 8px;">Mở Khóa</button>
            </div>
        </div>
    </div>
"""

if 'id="password-modal"' not in html:
    html = html.replace('<!-- Scripts -->', modal_html + '\n    <!-- Scripts -->')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Added modal to index.html")


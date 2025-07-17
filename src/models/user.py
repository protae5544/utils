from flask_frozen import Freezer
from app import app
import os
import shutil

# สร้าง freezer instance
freezer = Freezer(app)

# กำหนดค่า configuration
app.config['FREEZER_DESTINATION'] = 'build'
app.config['FREEZER_RELATIVE_URLS'] = True

@freezer.register_generator
def static_file_generator():
    """Generate static files"""
    static_files = []
    
    # สร้าง path สำหรับ static files
    static_dir = os.path.join(app.root_path, 'static')
    if os.path.exists(static_dir):
        for root, dirs, files in os.walk(static_dir):
            for file in files:
                file_path = os.path.relpath(os.path.join(root, file), static_dir)
                static_files.append(file_path)
    
    return static_files

if __name__ == '__main__':
    # ลบโฟลเดอร์ build เก่า
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # สร้าง static site
    print("🔨 กำลังสร้าง static site...")
    freezer.freeze()
    
    # คัดลอก combined-data.json ไปยัง build directory
    if os.path.exists('combined-data.json'):
        shutil.copy('combined-data.json', 'build/')
        print("📄 คัดลอกไฟล์ combined-data.json แล้ว")
    
    # สร้าง _redirects file สำหรับ Netlify
    with open('build/_redirects', 'w') as f:
        f.write('/*    /index.html   200\n')
    
    print("✅ สร้าง static site สำเร็จ!")
    print("📁 ไฟล์ static อยู่ในโฟลเดอร์ 'build'")

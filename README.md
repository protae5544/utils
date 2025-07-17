# ระบบใบเสร็จรับเงิน - กรมการจัดหางาน

โปรเจคนี้เป็นระบบจัดการใบเสร็จรับเงินสำหรับค่าธรรมเนียมใบอนุญาตทำงานคนต่างด้าว ที่ถูก refactor จากเว็บไซต์เดิมให้เป็น Flask Python application พร้อมใช้ฟอนต์ Sarabun ตามที่กำหนด

## คุณสมบัติหลัก

- 🏢 **ระบบจัดการเอกสาร** - Control panel สำหรับจัดการเอกสารต่างๆ
- 🧾 **ใบเสร็จรับเงิน** - สร้างและจัดการใบเสร็จรับเงินค่าธรรมเนียม
- 📄 **แบบฟอร์ม BT.50** - จัดการแบบฟอร์มใบอนุญาตทำงาน
- 👥 **ข้อมูลคนงาน** - จัดการข้อมูลประวัติคนงานต่างด้าว
- 🔐 **ระบบเข้าสู่ระบบ** - ป้องกันการเข้าถึงโดยไม่ได้รับอนุญาต

## เทคโนโลยีที่ใช้

### Backend
- **Flask** - Python web framework
- **Flask-CORS** - สำหรับการเชื่อมต่อ cross-origin
- **SQLAlchemy** - ORM สำหรับฐานข้อมูล
- **SQLite** - ฐานข้อมูลในตัว

### Frontend
- **HTML5/CSS3/JavaScript** - เทคโนโลยีพื้นฐาน
- **Sarabun Font** - ฟอนต์ไทยจาก Google Fonts
- **jsPDF** - สำหรับสร้าง PDF
- **html2canvas** - สำหรับแปลง HTML เป็นรูปภาพ
- **QRious** - สำหรับสร้าง QR Code
- **JSZip** - สำหรับสร้างไฟล์ ZIP

## การติดตั้งและใช้งาน

### ข้อกำหนดระบบ
- Python 3.11+
- pip (Python package manager)

### การติดตั้ง

1. **Clone หรือดาวน์โหลดโปรเจค**
   ```bash
   cd worker-receipt-app
   ```

2. **เปิดใช้งาน virtual environment**
   ```bash
   source venv/bin/activate
   ```

3. **ติดตั้ง dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **รันแอปพลิเคชัน**
   ```bash
   python src/main.py
   ```

5. **เปิดเบราว์เซอร์และไปที่**
   ```
   http://localhost:5000
   ```

### การใช้งาน

1. **เข้าสู่ระบบ**
   - รหัสผ่าน: `admin123`

2. **เลือกฟังก์ชันที่ต้องการ**
   - แบบฟอร์ม BT.50
   - ใบเสร็จรับเงิน
   - ข้อมูลคนงาน

3. **สำหรับใบเสร็จรับเงิน**
   - เลือกรายการจาก dropdown
   - ดาวน์โหลด PDF รายการเดียวหรือทั้งหมด
   - สแกน QR Code เพื่อดาวน์โหลดโดยตรง

## API Endpoints

### ข้อมูลคนงาน
- `GET /api/worker-data` - ดึงข้อมูลคนงานทั้งหมด
- `GET /api/worker-data/<request_number>` - ดึงข้อมูลคนงานตามเลขคำขอ
- `POST /api/add-worker` - เพิ่มข้อมูลคนงานใหม่
- `PUT /api/update-worker/<request_number>` - อัปเดตข้อมูลคนงาน
- `DELETE /api/delete-worker/<request_number>` - ลบข้อมูลคนงาน

### วันที่และเวลา
- `GET /api/current-date` - ดึงวันที่ปัจจุบันในรูปแบบไทย

## โครงสร้างโปรเจค

```
worker-receipt-app/
├── src/
│   ├── models/          # Database models
│   │   └── user.py
│   ├── routes/          # API routes
│   │   ├── user.py
│   │   └── receipt.py
│   ├── static/          # Frontend files
│   │   ├── index.html   # Control panel
│   │   ├── receipt.html # ใบเสร็จรับเงิน
│   │   ├── bt50.html    # แบบฟอร์ม BT.50
│   │   ├── worker.html  # ข้อมูลคนงาน
│   │   └── ...          # ไฟล์ CSS และ assets อื่นๆ
│   ├── database/        # SQLite database
│   └── main.py          # Entry point
├── venv/                # Virtual environment
├── requirements.txt     # Python dependencies
└── README.md           # เอกสารนี้
```

## ฟีเจอร์เด่น

### ฟอนต์ Sarabun
- ใช้ฟอนต์ Sarabun จาก Google Fonts
- รองรับน้ำหนักฟอนต์ 300 (Light) และ 600 (Semibold)
- แสดงผลภาษาไทยได้สวยงาม

### ระบบ PDF
- สร้าง PDF จาก HTML โดยใช้ html2canvas และ jsPDF
- รองรับการดาวน์โหลดรายการเดียวหรือทั้งหมดเป็น ZIP
- QR Code สำหรับการเข้าถึงโดยตรง

### Responsive Design
- รองรับการแสดงผลบนอุปกรณ์มือถือ
- UI/UX ที่ใช้งานง่าย
- เอฟเฟกต์และ animation ที่สวยงาม

## การ Deploy

### สำหรับ Production
1. อัปเดต `requirements.txt`
   ```bash
   pip freeze > requirements.txt
   ```

2. ใช้ production WSGI server เช่น Gunicorn
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
   ```

### สำหรับ Netlify (Frontend Only)
- หากต้องการ deploy เฉพาะ frontend ไปยัง Netlify
- ใช้ไฟล์ในโฟลเดอร์ `src/static/`
- ปรับ API endpoints ให้ชี้ไปยัง backend server

## การพัฒนาต่อ

### เพิ่มฟีเจอร์ใหม่
1. สร้าง route ใหม่ในโฟลเดอร์ `src/routes/`
2. เพิ่ม model ในโฟลเดอร์ `src/models/` (ถ้าจำเป็น)
3. อัปเดต `main.py` เพื่อ register blueprint ใหม่

### การปรับแต่ง UI
- แก้ไขไฟล์ HTML ในโฟลเดอร์ `src/static/`
- ใช้ฟอนต์ Sarabun classes: `.thsarabun`, `.thsarabun-light`, `.thsarabun-semibold`

## ข้อมูลติดต่อ

สำหรับคำถามหรือข้อเสนอแนะ กรุณาติดต่อทีมพัฒนา

---

**หมายเหตุ**: โปรเจคนี้ใช้สำหรับการสาธิตและพัฒนาเท่านั้น ไม่เหมาะสำหรับการใช้งานจริงในสภาพแวดล้อม production โดยไม่มีการปรับปรุงด้านความปลอดภัย


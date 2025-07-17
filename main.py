from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from datetime import datetime
import tempfile
import io
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# โหลดข้อมูลจากไฟล์ JSON
def load_worker_data():
    try:
        with open('combined-data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except FileNotFoundError:
        print("ไม่พบไฟล์ combined-data.json กำลังใช้ข้อมูลตัวอย่าง")
        return get_sample_data()
    except json.JSONDecodeError:
        print("เกิดข้อผิดพลาดในการอ่านไฟล์ JSON กำลังใช้ข้อมูลตัวอย่าง")
        return get_sample_data()

def get_sample_data():
    """ข้อมูลตัวอย่างสำหรับกรณีที่ไม่มีไฟล์ JSON"""
    return [
        {
            "englishName": "MISS EI YE PYAN",
            "requestNumber": "WP-67-009630",
            "alienReferenceNumber": "2492100646840",
            "เลขที่บนขวาใบเสร็จ": "2100680001130",
            "personalID": "6682190049543",
            "nationality": "เมียนมา",
            "หมายเลขชำระเงิน": "IV680106/001176",
            "employerName": "บริษัทบานกง เอ็นจิเนียริ่ง จำกัด",
            "employerId": "0255565000295"
        },
        {
            "englishName": "MR. JOHN SMITH",
            "requestNumber": "WP-67-009631",
            "alienReferenceNumber": "2492100646841",
            "เลขที่บนขวาใบเสร็จ": "2100680001131",
            "personalID": "6682190049544",
            "nationality": "อเมริกัน",
            "หมายเลขชำระเงิน": "IV680106/001177",
            "employerName": "บริษัท ABC จำกัด",
            "employerId": "0255565000296"
        },
        {
            "englishName": "MS. MARIA GONZALEZ",
            "requestNumber": "WP-67-009632",
            "alienReferenceNumber": "2492100646842",
            "เลขที่บนขวาใบเสร็จ": "2100680001132",
            "personalID": "6682190049545",
            "nationality": "เม็กซิโก",
            "หมายเลขชำระเงิน": "IV680106/001178",
            "employerName": "บริษัท XYZ จำกัด",
            "employerId": "0255565000297"
        }
    ]

@app.route('/')
def index():
    """หน้าแรก - ระบบใบเสร็จรับเงิน"""
    return render_template('index.html')

@app.route('/api/worker-data')
def get_worker_data():
    """API สำหรับดึงข้อมูลแรงงาน"""
    try:
        data = load_worker_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/current-date')
def get_current_date():
    """API สำหรับดึงวันที่ปัจจุบัน"""
    try:
        now = datetime.now()
        
        # วันที่แบบไทย
        thai_months = [
            'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน',
            'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม',
            'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
        ]
        
        thai_date = f"{now.day:02d} {thai_months[now.month-1]} {now.year + 543}"
        
        # วันที่สำหรับพิมพ์
        print_date = f"{now.day:02d}/{now.month:02d}/{str(now.year + 543)[2:]} {now.hour:02d}:{now.minute:02d} น."
        
        return jsonify({
            'formatted_date': thai_date,
            'print_date': print_date,
            'timestamp': now.isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-data', methods=['POST'])
def upload_data():
    """API สำหรับอัพโหลดข้อมูล JSON ใหม่"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'ไม่พบไฟล์ที่อัพโหลด'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'ไม่ได้เลือกไฟล์'}), 400
        
        if file and file.filename.endswith('.json'):
            # อ่านและตรวจสอบข้อมูล JSON
            content = file.read().decode('utf-8')
            data = json.loads(content)
            
            # บันทึกไฟล์ใหม่
            with open('combined-data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return jsonify({
                'success': True,
                'message': 'อัพโหลดข้อมูลสำเร็จ',
                'count': len(data) if isinstance(data, list) else 1
            })
        else:
            return jsonify({'error': 'กรุณาอัพโหลดไฟล์ .json เท่านั้น'}), 400
            
    except json.JSONDecodeError:
        return jsonify({'error': 'ไฟล์ JSON มีรูปแบบไม่ถูกต้อง'}), 400
    except Exception as e:
        return jsonify({'error': f'เกิดข้อผิดพลาด: {str(e)}'}), 500

@app.route('/api/worker-data/<request_number>')
def get_worker_by_request_number(request_number):
    """API สำหรับดึงข้อมูลแรงงานตามเลขคำขอ"""
    try:
        data = load_worker_data()
        worker = next((item for item in data if item.get('requestNumber') == request_number), None)
        
        if worker:
            return jsonify(worker)
        else:
            return jsonify({'error': 'ไม่พบข้อมูลสำหรับเลขคำขอที่ระบุ'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search-worker')
def search_worker():
    """API สำหรับค้นหาข้อมูลแรงงาน"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'error': 'กรุณาระบุคำค้นหา'}), 400
        
        data = load_worker_data()
        results = []
        
        for item in data:
            # ค้นหาในฟิลด์ต่างๆ
            if (query.lower() in (item.get('englishName', '') or '').lower() or
                query in (item.get('requestNumber', '') or '') or
                query in (item.get('personalID', '') or '') or
                query in (item.get('alienReferenceNumber', '') or '')):
                results.append(item)
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics')
def get_statistics():
    """API สำหรับดึงสถิติข้อมูล"""
    try:
        data = load_worker_data()
        
        # นับจำนวนตามสัญชาติ
        nationality_count = {}
        for item in data:
            nationality = item.get('nationality', 'ไม่ระบุ')
            nationality_count[nationality] = nationality_count.get(nationality, 0) + 1
        
        # นับจำนวนตามบริษัท
        employer_count = {}
        for item in data:
            employer = item.get('employerName', 'ไม่ระบุ')
            employer_count[employer] = employer_count.get(employer, 0) + 1
        
        stats = {
            'total_workers': len(data),
            'nationality_distribution': nationality_count,
            'employer_distribution': employer_count,
            'last_updated': datetime.now().isoformat()
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-data')
def export_data():
    """API สำหรับ export ข้อมูลเป็น JSON"""
    try:
        data = load_worker_data()
        
        # สร้างไฟล์ JSON ใน memory
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        
        # สร้าง response
        output = io.BytesIO()
        output.write(json_data.encode('utf-8'))
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/json',
            as_attachment=True,
            download_name=f'worker_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin')
def admin_panel():
    """หน้าแอดมินสำหรับจัดการข้อมูล"""
    return render_template('admin.html')

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'ไม่พบหน้าที่ระบุ'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'เกิดข้อผิดพลาดภายในเซิร์ฟเวอร์'}), 500

if __name__ == '__main__':
    # สร้างโฟลเดอร์ที่จำเป็น
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # ตรวจสอบว่ามีไฟล์ JSON หรือไม่
    if not os.path.exists('combined-data.json'):
        print("สร้างไฟล์ combined-data.json ตัวอย่าง")
        with open('combined-data.json', 'w', encoding='utf-8') as f:
            json.dump(get_sample_data(), f, ensure_ascii=False, indent=2)
    
    # รัน Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
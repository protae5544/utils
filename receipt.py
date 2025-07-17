from flask import Blueprint, jsonify, request, render_template_string
from datetime import datetime
import json

receipt_bp = Blueprint('receipt', __name__)

# ข้อมูลตัวอย่างสำหรับใบเสร็จ
sample_data = [
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
    }
]

@receipt_bp.route('/worker-data', methods=['GET'])
def get_worker_data():
    """API สำหรับดึงข้อมูลคนงาน"""
    return jsonify(sample_data)

@receipt_bp.route('/worker-data/<request_number>', methods=['GET'])
def get_worker_by_request_number(request_number):
    """API สำหรับดึงข้อมูลคนงานตามเลขคำขอ"""
    worker = next((item for item in sample_data if item["requestNumber"] == request_number), None)
    if worker:
        return jsonify(worker)
    else:
        return jsonify({"error": "ไม่พบข้อมูลสำหรับเลขคำขอที่ระบุ"}), 404

@receipt_bp.route('/add-worker', methods=['POST'])
def add_worker():
    """API สำหรับเพิ่มข้อมูลคนงานใหม่"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "ไม่พบข้อมูลที่ส่งมา"}), 400
        
        # ตรวจสอบข้อมูลที่จำเป็น
        required_fields = ["englishName", "requestNumber", "alienReferenceNumber"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"ข้อมูล {field} เป็นข้อมูลที่จำเป็น"}), 400
        
        # ตรวจสอบว่าเลขคำขอซ้ำหรือไม่
        if any(item["requestNumber"] == data["requestNumber"] for item in sample_data):
            return jsonify({"error": "เลขคำขอนี้มีอยู่แล้ว"}), 400
        
        sample_data.append(data)
        return jsonify({"message": "เพิ่มข้อมูลสำเร็จ", "data": data}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@receipt_bp.route('/update-worker/<request_number>', methods=['PUT'])
def update_worker(request_number):
    """API สำหรับอัปเดตข้อมูลคนงาน"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "ไม่พบข้อมูลที่ส่งมา"}), 400
        
        # หาข้อมูลที่ต้องการอัปเดต
        worker_index = next((i for i, item in enumerate(sample_data) if item["requestNumber"] == request_number), None)
        if worker_index is None:
            return jsonify({"error": "ไม่พบข้อมูลสำหรับเลขคำขอที่ระบุ"}), 404
        
        # อัปเดตข้อมูล
        sample_data[worker_index].update(data)
        return jsonify({"message": "อัปเดตข้อมูลสำเร็จ", "data": sample_data[worker_index]})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@receipt_bp.route('/delete-worker/<request_number>', methods=['DELETE'])
def delete_worker(request_number):
    """API สำหรับลบข้อมูลคนงาน"""
    try:
        # หาข้อมูลที่ต้องการลบ
        worker_index = next((i for i, item in enumerate(sample_data) if item["requestNumber"] == request_number), None)
        if worker_index is None:
            return jsonify({"error": "ไม่พบข้อมูลสำหรับเลขคำขอที่ระบุ"}), 404
        
        # ลบข้อมูล
        deleted_worker = sample_data.pop(worker_index)
        return jsonify({"message": "ลบข้อมูลสำเร็จ", "data": deleted_worker})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@receipt_bp.route('/current-date', methods=['GET'])
def get_current_date():
    """API สำหรับดึงวันที่ปัจจุบันในรูปแบบไทย"""
    try:
        today = datetime.now()
        day = str(today.day).zfill(2)
        month = today.month
        year = today.year + 543  # แปลงเป็น พ.ศ.
        hours = str(today.hour).zfill(2)
        minutes = str(today.minute).zfill(2)
        
        thai_months = [
            'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
            'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
        ]
        
        formatted_date = f"{day} {thai_months[month-1]} {year}"
        print_date = f"{day}/{str(month).zfill(2)}/{str(year)[2:]} {hours}:{minutes} น."
        
        return jsonify({
            "formatted_date": formatted_date,
            "print_date": print_date,
            "timestamp": today.isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


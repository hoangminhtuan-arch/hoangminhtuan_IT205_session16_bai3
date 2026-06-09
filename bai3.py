er_patients = [
    "ER01|Nguyen Van Quan|HR:115|TEMP:39.5",
    "ER02|Tran Thi Binh|HR:80|TEMP:37.0",
    "ER03|Le Van Xua|HR:130|TEMP:38.2"
]

def parse_patient(data):
    parts = data.split("|")
    return {
        "id": parts[0],
        "name": parts[1],
        "hr": parts[2].split(":")[1],
        "temp": parts[3].split(":")[1]
    }

def display_dashboard(patients_list):
    if not patients_list:
        print("Khoa cấp cứu hiện đang trống.")
        return

    print("--- BẢNG THEO DÕI CA CẤP CỨU ------------------------------------")
    for i, data in enumerate(patients_list):
        patient = parse_patient(data)
        print(f"{i+1}. [{patient['id']}] {patient['name']} | Nhịp tim: {int(float(patient['hr']))} bpm | Nhiệt độ: {patient['temp']} °C")
    print("-----------------------------------------------------------------")

def find_patient_index(patients_list, er_id):
    er_id = er_id.strip().upper()
    for i, data in enumerate(patients_list):
        if data.split("|")[0].strip().upper() == er_id:
            return i
    return -1

def admit_patient(patients_list):
    er_id = input("Nhập mã ER: ").strip().upper()
    if not er_id:
        print("Mã ER không được để trống!")
        return

    if find_patient_index(patients_list, er_id) != -1:
        print("Mã ca cấp cứu đã tồn tại!")
        return

    name = input("Nhập tên bệnh nhân: ").strip().title()
    if not name:
        print("Tên bệnh nhân không được để trống!")
        return

    try:
        hr = float(input("Nhập nhịp tim HR: "))
        if hr <= 0:
            print("Sinh hiệu không hợp lệ, vui lòng nhập số lớn hơn 0!")
            return
    except:
        print("Sinh hiệu không hợp lệ, vui lòng nhập số lớn hơn 0!")
        return

    try:
        temp = float(input("Nhập nhiệt độ TEMP: "))
        if temp < 36.5:
            print("Sinh hiệu không hợp lệ, vui lòng nhập số lớn hơn hoặc bằng 36.5!")
            return
    except:
        print("Sinh hiệu không hợp lệ, vui lòng nhập số lớn hơn hoặc bằng 36.5!")
        return

    new_data = f"{er_id}|{name}|HR:{hr}|TEMP:{temp}"
    patients_list.append(new_data)
    print("Tiếp nhận ca cấp cứu mới thành công!")

def extract_vital_value(vital):
    return float(vital.split(":")[1])

def update_vitals(patients_list):
    er_id = input("Nhập mã ER cần cập nhật: ").strip().upper()
    idx = find_patient_index(patients_list, er_id)

    if idx == -1:
        print("Không tìm thấy bệnh nhân. Vui lòng kiểm tra lại mã ER!")
        return

    patient = parse_patient(patients_list[idx])
    print(f"Tìm thấy bệnh nhân: {patient['name']}")
    print(f"Sinh hiệu hiện tại: HR:{patient['hr']} | TEMP:{patient['temp']}")

    choice = input("Chọn loại sinh hiệu (1-HR, 2-TEMP): ").strip()

    if choice == "1":
        try:
            new_hr = float(input("Nhập nhịp tim mới: "))
            if new_hr <= 0:
                print("Sinh hiệu không hợp lệ, vui lòng nhập số lớn hơn 0!")
                return
            parts = patients_list[idx].split("|")
            parts[2] = f"HR:{new_hr}"
            patients_list[idx] = "|".join(parts)
            print("Cập nhật nhịp tim thành công!")
        except:
            print("Sinh hiệu không hợp lệ, vui lòng nhập số lớn hơn 0!")

    elif choice == "2":
        try:
            new_temp = float(input("Nhập nhiệt độ mới: "))
            if new_temp < 36.5:
                print("Sinh hiệu không hợp lệ, vui lòng nhập số lớn hơn hoặc bằng 36.5!")
                return
            parts = patients_list[idx].split("|")
            parts[3] = f"TEMP:{new_temp}"
            patients_list[idx] = "|".join(parts)
            print("Cập nhật nhiệt độ thành công!")
        except:
            print("Sinh hiệu không hợp lệ, vui lòng nhập số lớn hơn hoặc bằng 36.5!")
    else:
        print("Lựa chọn không hợp lệ. Vui lòng chọn 1 hoặc 2!")

def trigger_red_alert(patients_list):
    if not patients_list:
        print("Khoa cấp cứu hiện đang trống.")
        return

    danger = []
    for data in patients_list:
        patient = parse_patient(data)
        hr = float(patient["hr"])
        temp = float(patient["temp"])
        if hr > 100 or temp >= 39.0:
            danger.append(patient)

    if not danger:
        print("--- KIỂM TRA BÁO ĐỘNG ĐỎ ---")
        print("Không có bệnh nhân nguy kịch tại thời điểm hiện tại.")
        return

    print("!!! BÁO ĐỘNG ĐỎ - DANH SÁCH BỆNH NHÂN NGUY KỊCH !!!")
    for i, p in enumerate(danger):
        print(f"{i+1}. [{p['id']}] {p['name']} | HR:{p['hr']} bpm | TEMP:{p['temp']} °C | CẦN XỬ LÝ KHẨN CẤP")
    print(f"Tổng số ca nguy kịch: {len(danger)}")

def discharge_patient(patients_list):
    er_id = input("Nhập mã ER cần xóa khỏi hệ thống: ").strip().upper()
    idx = find_patient_index(patients_list, er_id)

    if idx == -1:
        print("Không tìm thấy bệnh nhân. Vui lòng kiểm tra lại mã ER!")
        return

    patient = parse_patient(patients_list[idx])
    patients_list.pop(idx)
    print(f"Đã chuyển khoa thành công cho bệnh nhân {patient['name']}!")

while True:
    choice = input("""
===== HỆ THỐNG QUẢN LÝ CẤP CỨU RIKKEI ER =====
1. Bảng theo dõi bệnh nhân
2. Tiếp nhận ca cấp cứu mới
3. Cập nhật lại sinh hiệu
4. BÁO ĐỘNG ĐỎ
5. Xuất viện / Chuyển khoa
6. Thoát chương trình
=================================================
Chọn chức năng (1-6): """)

    if choice == "1":
        display_dashboard(er_patients)
    elif choice == "2":
        admit_patient(er_patients)
    elif choice == "3":
        update_vitals(er_patients)
    elif choice == "4":
        trigger_red_alert(er_patients)
    elif choice == "5":
        discharge_patient(er_patients)
    elif choice == "6":
        print("Kết thúc ca trực.")
        break
    else:
        print("Lựa chọn không hợp lệ, vui lòng nhập số từ 1-6!")

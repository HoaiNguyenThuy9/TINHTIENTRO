import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tính Tiền Trọ", layout="wide")

st.title("Bảng Tính Tiền Phòng Trọ")

# Cấu trúc bảng theo yêu cầu:
# Giữ đúng thứ tự các cột mà bạn mong muốn
data = {
    "Phòng": [f"P{i}" for i in range(1, 11)],
    "Số điện cũ": [0.0] * 10,
    "Số điện mới": [0.0] * 10,
    "Tiền điện": [0.0] * 10,
    "Số nước cũ": [0.0] * 10,
    "Số nước mới": [0.0] * 10,
    "Tiền nước": [0.0] * 10,
    "Tiền phòng": [0.0] * 10,
    "Phí khác": [0.0] * 10,
    "Tổng tiền": [0.0] * 10
}

df = pd.DataFrame(data)

# Sidebar để nhập đơn giá chung cho cả dãy trọ
st.sidebar.header("Thông số cài đặt")
don_gia_dien = st.sidebar.number_input("Đơn giá điện (VNĐ/số)", value=3000)
don_gia_nuoc = st.sidebar.number_input("Đơn giá nước (VNĐ/số)", value=15000)

st.subheader("Nhập liệu thông số tháng")
# Cho phép chỉnh sửa bảng
edited_df = st.data_editor(df, use_container_width=True)

# Hàm tính toán đảm bảo không có số âm
def calculate_row(row):
    # Tính số tiêu thụ: Nếu mới < cũ thì mặc định là 0 để tránh số âm
    so_dien_dung = max(0, row["Số điện mới"] - row["Số điện cũ"])
    so_nuoc_dung = max(0, row["Số nước mới"] - row["Số nước cũ"])
    
    # Tính tiền
    row["Tiền điện"] = so_dien_dung * don_gia_dien
    row["Tiền nước"] = so_nuoc_dung * don_gia_nuoc
    
    # Tính tổng tiền (Tiền phòng và Phí khác cũng lấy giá trị dương)
    tien_phong = max(0, row["Tiền phòng"])
    phi_khac = max(0, row["Phí khác"])
    
    row["Tổng tiền"] = row["Tiền điện"] + row["Tiền nước"] + tien_phong + phi_khac
    
    return row

# Áp dụng tính toán cho từng dòng
final_df = edited_df.apply(calculate_row, axis=1)

st.subheader("Bảng kết quả")
st.dataframe(final_df, use_container_width=True)

# Nút xuất file
csv = final_df.to_csv(index=False).encode('utf-8')
st.download_button("Tải kết quả về máy", csv, "Bang_Tinh_Tien_Tro.csv", "text/csv")

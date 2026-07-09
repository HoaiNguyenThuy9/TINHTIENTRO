import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tính tiền phòng trọ", layout="wide")

st.title("Ứng dụng Tính tiền Phòng trọ")

# Định nghĩa các cột theo yêu cầu từ ảnh
# Các cột đầu vào và cột kết quả
data = {
    "Phòng": [i for i in range(1, 11)],
    "Số điện mới": [0.0] * 10,
    "Số điện cũ": [0.0] * 10,
    "Tiền điện": [0.0] * 10, # Cột này sẽ được tính
    "Số nước mới": [0.0] * 10,
    "Số nước cũ": [0.0] * 10,
    "Tiền nước": [0.0] * 10, # Cột này sẽ được tính
    "Tiền phòng": [0.0] * 10, # Cột mới thêm vào
    "Phí khác": [0.0] * 10,
    "Tổng tiền": [0.0] * 10  # Cột này sẽ được tính
}

df = pd.DataFrame(data)

# Thiết lập đơn giá ở thanh bên (sidebar)
st.sidebar.header("Cấu hình đơn giá")
gia_dien = st.sidebar.number_input("Đơn giá điện (VNĐ/số)", value=3000)
gia_nuoc = st.sidebar.number_input("Đơn giá nước (VNĐ/số)", value=15000)

st.subheader("Nhập liệu thông số tháng")
# Cho phép chỉnh sửa trực tiếp trên bảng
edited_df = st.data_editor(df, use_container_width=True)

# Tính toán các cột kết quả
def calculate_bill(row):
    tien_dien = (row["Số điện mới"] - row["Số điện cũ"]) * gia_dien
    tien_nuoc = (row["Số nước mới"] - row["Số nước cũ"]) * gia_nuoc
    # Tổng tiền = Tiền điện + Tiền nước + Tiền phòng + Phí khác
    tong_tien = tien_dien + tien_nuoc + row["Tiền phòng"] + row["Phí khác"]
    
    row["Tiền điện"] = tien_dien
    row["Tiền nước"] = tien_nuoc
    row["Tổng tiền"] = tong_tien
    return row

# Áp dụng tính toán
final_df = edited_df.apply(calculate_bill, axis=1)

st.subheader("Bảng tính tiền chi tiết")
st.dataframe(final_df, use_container_width=True)

# Tải file kết quả
csv = final_df.to_csv(index=False).encode('utf-8')
st.download_button("Tải file kết quả (CSV)", csv, "chi_tiet_tien_phong.csv", "text/csv")

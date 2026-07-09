import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tính tiền điện nước", layout="wide")

st.title("Ứng dụng Tính tiền Điện - Nước")

# Định nghĩa các cột cho bảng nhập liệu
columns = [
    "Phòng", "Số điện mới", "Số điện cũ", "Số nước mới", "Số nước cũ", 
    "Đơn giá điện", "Đơn giá nước", "Phí khác"
]

# Tạo dataframe mặc định cho 10 phòng
data = {
    "Phòng": [f"Phòng {i}" for i in range(1, 11)],
    "Số điện mới": [0.0] * 10,
    "Số điện cũ": [0.0] * 10,
    "Số nước mới": [0.0] * 10,
    "Số nước cũ": [0.0] * 10,
    "Đơn giá điện": [3000.0] * 10, # Giá mặc định, có thể sửa
    "Đơn giá nước": [15000.0] * 10, # Giá mặc định, có thể sửa
    "Phí khác": [0.0] * 10
}

df = pd.DataFrame(data)

st.subheader("Nhập liệu thông số tháng")
# Cho phép chỉnh sửa trực tiếp trên bảng
edited_df = st.data_editor(df, use_container_width=True)

# Tính toán các cột kết quả
def calculate_bill(row):
    tien_dien = (row["Số điện mới"] - row["Số điện cũ"]) * row["Đơn giá điện"]
    tien_nuoc = (row["Số nước mới"] - row["Số nước cũ"]) * row["Đơn giá nước"]
    tong_tien = tien_dien + tien_nuoc + row["Phí khác"]
    return pd.Series([tien_dien, tien_nuoc, tong_tien], index=["Tiền điện", "Tiền nước", "Tổng tiền"])

# Áp dụng tính toán
results = edited_df.apply(calculate_bill, axis=1)
final_df = pd.concat([edited_df[["Phòng"]], results], axis=1)

st.subheader("Kết quả tính toán")
st.dataframe(final_df, use_container_width=True)

# Tải file kết quả
csv = final_df.to_csv(index=False).encode('utf-8')
st.download_button("Tải file kết quả (CSV)", csv, "ket_qua_tien_phong.csv", "text/csv")

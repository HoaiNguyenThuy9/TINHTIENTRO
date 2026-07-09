import streamlit as st
import pandas as pd

st.set_page_config(page_title="Quản lý tiền phòng", layout="wide")

st.title("Ứng dụng Quản lý Tiền phòng trọ")

# Khởi tạo dữ liệu mẫu cho 10 phòng
data = {
    "Phòng": [i for i in range(1, 11)],
    "Số điện mới": [0.0] * 10,
    "Số điện cũ": [0.0] * 10,
    "Đơn giá điện": [3000.0] * 10,
    "Số nước mới": [0.0] * 10,
    "Số nước cũ": [0.0] * 10,
    "Đơn giá nước": [15000.0] * 10,
    "Tiền phòng": [1500000.0] * 10,
    "Phí khác": [0.0] * 10
}

df = pd.DataFrame(data)

st.subheader("Nhập liệu số điện, nước và giá")
# Người dùng nhập liệu trực tiếp trên bảng
edited_df = st.data_editor(df, use_container_width=True)

# Hàm tính toán chi tiết
def calculate_all(row):
    # Sử dụng max(0, ...) để đảm bảo kết quả không bao giờ âm
    dien_tieu_thu = max(0, row["Số điện mới"] - row["Số điện cũ"])
    nuoc_tieu_thu = max(0, row["Số nước mới"] - row["Số nước cũ"])
    
    tien_dien = dien_tieu_thu * row["Đơn giá điện"]
    tien_nuoc = nuoc_tieu_thu * row["Đơn giá nước"]
    
    # Tính tổng tiền
    tong_tien = tien_dien + tien_nuoc + row["Tiền phòng"] + row["Phí khác"]
    
    return pd.Series([tien_dien, tien_nuoc, tong_tien], index=["Tiền điện", "Tiền nước", "Tổng tiền"])

# Thực hiện tính toán
results = edited_df.apply(calculate_all, axis=1)
# Kết hợp lại bảng: Phòng + Kết quả tính toán + Dữ liệu gốc
final_df = pd.concat([edited_df[["Phòng"]], results, edited_df.drop(columns=["Phòng"])], axis=1)

st.subheader("Kết quả chi tiết")
st.dataframe(final_df, use_container_width=True)

# Tải file kết quả
csv = final_df.to_csv(index=False).encode('utf-8')
st.download_button("Tải bảng tính về máy (CSV)", csv, "quan_ly_tien_phong.csv", "text/csv")

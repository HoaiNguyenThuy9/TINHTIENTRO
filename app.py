import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tính Tiền Trọ", layout="wide")

st.title("Bảng Tính Tiền Phòng Trọ")

# Cấu trúc nhập liệu: chỉ bao gồm các cột cần nhập thông số
data = {
    "Phòng": [f"P{i}" for i in range(1, 11)],
    "Số điện cũ": [0.0] * 10,
    "Số điện mới": [0.0] * 10,
    "Số nước cũ": [0.0] * 10,
    "Số nước mới": [0.0] * 10,
    "Tiền phòng": [0.0] * 10,
    "Phí khác": [0.0] * 10
}

df_input = pd.DataFrame(data)

# Sidebar nhập đơn giá
st.sidebar.header("Thông số cài đặt")
don_gia_dien = st.sidebar.number_input("Đơn giá điện (VNĐ/số)", value=3000)
don_gia_nuoc = st.sidebar.number_input("Đơn giá nước (VNĐ/số)", value=15000)

st.subheader("Nhập liệu thông số tháng")
# Bảng chỉ để nhập liệu
edited_df = st.data_editor(df_input, use_container_width=True)

# Hàm tính toán kết quả
def calculate_results(df):
    results = df.copy()
    
    # Tính toán số sử dụng (đảm bảo không âm)
    so_dien_dung = (results["Số điện mới"] - results["Số điện cũ"]).clip(lower=0)
    so_nuoc_dung = (results["Số nước mới"] - results["Số nước cũ"]).clip(lower=0)
    
    # Tính tiền điện/nước
    results["Tiền điện"] = so_dien_dung * don_gia_dien
    results["Tiền nước"] = so_nuoc_dung * don_gia_nuoc
    
    # Đảm bảo Tiền phòng và Phí khác không âm
    results["Tiền phòng"] = results["Tiền phòng"].clip(lower=0)
    results["Phí khác"] = results["Phí khác"].clip(lower=0)
    
    # Tính tổng
    results["Tổng tiền"] = results["Tiền điện"] + results["Tiền nước"] + results["Tiền phòng"] + results["Phí khác"]
    
    # Sắp xếp lại thứ tự cột cho giống yêu cầu
    cols = ["Phòng", "Số điện cũ", "Số điện mới", "Tiền điện", 
            "Số nước cũ", "Số nước mới", "Tiền nước", 
            "Tiền phòng", "Phí khác", "Tổng tiền"]
    return results[cols]

# Hiển thị bảng kết quả
final_df = calculate_results(edited_df)

st.subheader("Bảng kết quả chi tiết")
st.dataframe(final_df, use_container_width=True)

# Nút xuất file
csv = final_df.to_csv(index=False).encode('utf-8')
st.download_button("Tải kết quả về máy (CSV)", csv, "Bang_Tinh_Tien_Tro.csv", "text/csv")

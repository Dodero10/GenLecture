import os

import streamlit as st
from extract_metadata import extract_metadata

# Tựa đề ứng dụng
st.title("Chuyển Slide Thành Video Bài Giảng")

# Upload slide
uploaded_file = st.file_uploader("Tải lên file slide (PowerPoint hoặc PDF)", type=["pptx", "pdf"])

# Đường dẫn thư mục tạm và thư mục metadata
temp_upload_folder = "temp_uploads"
output_folder = "data/metadata"

# Tạo thư mục tạm nếu chưa tồn tại
os.makedirs(temp_upload_folder, exist_ok=True)

if uploaded_file:
    # Lưu file tải lên
    file_path = os.path.join(temp_upload_folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.write(f"File được tải lên: {uploaded_file.name}")

    # Chạy pipeline extract_metadata
    try:
        st.write("Đang trích xuất metadata...")
        extract_metadata(file_path, output_folder)
        st.success("Hoàn thành trích xuất metadata!")
        st.write(f"Metadata và tài nguyên được lưu tại: {output_folder}")
    except Exception as e:
        st.error(f"Đã xảy ra lỗi: {e}")

    # Xóa file tạm
    os.remove(file_path)

# Hướng dẫn sử dụng
st.sidebar.title("Hướng dẫn")
st.sidebar.info(
    "1. Tải lên file slide (PPTX hoặc PDF).\\n"
    "2. Ứng dụng sẽ tự động trích xuất metadata và lưu tài nguyên.\\n"
    "3. Kiểm tra kết quả trong thư mục 'data/metadata'."
)

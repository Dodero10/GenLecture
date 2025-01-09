import os
import streamlit as st
from extract_metadata import extract_metadata
from slide_to_script import slide_to_script

st.title("Chuyển Slide Thành Video Bài Giảng")

uploaded_file = st.file_uploader("Tải lên file slide (PowerPoint hoặc PDF)", type=["pptx", "pdf"])

model_type = st.radio(
    "Chọn model để sinh script:",
    ('gemini', 'qwen'),
    help="Gemini: Sử dụng Google Gemini Pro. Qwen: Sử dụng Qwen-1.5B"
)

temp_upload_folder = "temp_uploads"
input_folder = "data/input"
output_folder = "data/metadata"
scripts_folder = "data/scripts"
videos_folder = "data/output/videos"

os.makedirs(temp_upload_folder, exist_ok=True)
os.makedirs(input_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)
os.makedirs(scripts_folder, exist_ok=True)
os.makedirs(videos_folder, exist_ok=True)

if uploaded_file:

    temp_file_path = os.path.join(temp_upload_folder, uploaded_file.name)
    input_file_path = os.path.join(input_folder, uploaded_file.name)
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.getbuffer())

    with open(input_file_path, "wb") as input_file:
        input_file.write(uploaded_file.getbuffer())

    st.write(f"File được tải lên: {uploaded_file.name}")

    try:
        st.write("Đang trích xuất metadata...")
        extract_metadata(temp_file_path, output_folder)
        st.success("Hoàn thành trích xuất metadata!")
        st.write(f"Metadata và tài nguyên được lưu tại: {output_folder}")
    except Exception as e:
        st.error(f"Đã xảy ra lỗi: {e}")
    os.remove(temp_file_path)


if st.button(f"Generate Script using {model_type.upper()}"):
    try:
        st.write(f"Đang sinh script từ metadata sử dụng {model_type.upper()}...")
        input_metadata_path = os.path.join(output_folder, f"{os.path.splitext(uploaded_file.name)[0]}.json")
        slide_to_script(input_metadata_path, output_folder, scripts_folder, model_type=model_type)
        st.success(f"Scripts đã được sinh và lưu tại: {scripts_folder}")
    except Exception as e:
        st.error(f"Đã xảy ra lỗi khi sinh script: {e}")

video_path = os.path.join(videos_folder, "slide_1.mp4")
if os.path.exists(video_path):
    st.subheader("Preview Video Slide 1")
    st.video(video_path)

st.sidebar.title("Hướng dẫn")
st.sidebar.info(
    "1. Tải lên file slide (PPTX hoặc PDF).\n"
    "2. Ứng dụng sẽ tự động trích xuất metadata và lưu tài nguyên.\n"
    "3. Chọn model (Gemini hoặc Qwen) để sinh script.\n"
    "4. Nhấn nút 'Generate Script' để sinh script từ metadata.\n"
    "5. Kiểm tra kết quả trong thư mục 'data/scripts'.\n"
    "6. Xem preview video slide đầu tiên ở cuối trang."
)

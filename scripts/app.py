import streamlit as st

# Tựa đề ứng dụng
st.title("Generate slide to Lecture Video")

# Upload slide
uploaded_file = st.file_uploader("Tải lên file slide (PowerPoint hoặc PDF)", type=["pptx", "pdf"])

# Hiển thị pipeline
if uploaded_file:
    st.write("File được tải lên:", uploaded_file.name)
    st.write("Chạy pipeline...")

    # Gọi các bước trong pipeline
    st.write("1. Trích xuất metadata...")
    # Gọi hàm từ scripts/extract_metadata.py

    st.write("2. Chuyển slide thành kịch bản...")
    # Gọi hàm từ scripts/slide_to_script.py

    st.write("3. Chuyển kịch bản thành âm thanh...")
    # Gọi hàm từ scripts/script_to_audio.py

    st.write("4. Tạo video từ slide và âm thanh...")
    # Gọi hàm từ scripts/audio_slide_to_video.py

    st.success("Hoàn thành pipeline!")

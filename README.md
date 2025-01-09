# GenLecture - Tự động tạo video bài giảng từ slide

GenLecture là một ứng dụng giúp tự động chuyển đổi slide PowerPoint hoặc PDF thành video bài giảng có giọng nói. Ứng dụng sử dụng AI để sinh script bài giảng và chuyển văn bản thành giọng nói.

## Tính năng

- Hỗ trợ file PowerPoint (PPTX) và PDF
- Trích xuất metadata và hình ảnh từ slide
- Sinh script bài giảng tự động với 2 lựa chọn model:
  - Google Gemini Pro
  - Qwen-1.5B
- Chuyển văn bản thành giọng nói tiếng Việt
- Tạo video bài giảng với hình ảnh và âm thanh
- Gộp tất cả video slide thành một video hoàn chỉnh
- Giao diện web thân thiện với người dùng

## Cấu trúc thư mục

```
GenLecture/
├── data/
│   ├── input/          # Thư mục chứa file slide đầu vào
│   ├── metadata/       # Metadata và hình ảnh được trích xuất
│   ├── scripts/        # Script bài giảng được sinh bởi AI
│   ├── audio/          # File âm thanh được tạo từ script
│   └── output/         # Video đầu ra
│       └── videos/     # Video cho từng slide và video cuối cùng
├── scripts/
│   ├── app.py                     # Giao diện web Streamlit
│   ├── extract_metadata.py        # Trích xuất metadata từ slide
│   ├── generate_description_image.py  # Sinh mô tả cho hình ảnh
│   ├── slide_to_script.py         # Sinh script bài giảng
│   ├── script_to_audio.py         # Chuyển script thành audio
│   └── audio_slide_to_video.py    # Tạo video từ slide và audio
└── .env                # File cấu hình API key và model mặc định
```

## Yêu cầu hệ thống

- Python 3.8 trở lên
- PowerPoint (để xử lý file PPTX)
- [Poppler](https://github.com/oschwartz10612/poppler-windows/releases/) (để xử lý PDF)
- [ImageMagick](https://imagemagick.org/script/download.php) (để xử lý video)

## Cài đặt

1. Clone repository:
```bash
git clone https://github.com/yourusername/GenLecture.git
cd GenLecture
```

2. Tạo môi trường ảo và kích hoạt:
```bash
python -m venv env_l2s
source env_l2s/bin/activate  # Linux/Mac
env_l2s\Scripts\activate     # Windows
```

3. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

4. Cấu hình file .env:
```env
GEMINI_API_KEY=your_api_key_here
DEFAULT_MODEL=qwen  # hoặc gemini
```

5. Cài đặt Poppler và ImageMagick:
   - Tải và cài đặt Poppler
   - Tải và cài đặt ImageMagick (chọn "Install legacy utilities")
   - Thêm đường dẫn vào PATH hoặc cập nhật trong code

## Sử dụng

1. Khởi động ứng dụng web:
```bash
streamlit run scripts/app.py
```

2. Trên giao diện web:
   - Tải lên file slide (PPTX hoặc PDF)
   - Chọn model để sinh script (Gemini hoặc Qwen)
   - Nhấn nút "Generate Script"
   - Đợi quá trình xử lý hoàn tất
   - Xem preview video slide đầu tiên

3. Kết quả:
   - Script được lưu trong `data/scripts/scripts.json`
   - Audio được lưu trong `data/audio/`
   - Video từng slide được lưu trong `data/output/videos/`
   - Video cuối cùng được lưu tại `data/output/final_lecture.mp4`

## Quy trình xử lý

1. **Trích xuất metadata**:
   - Đọc file PPTX/PDF
   - Trích xuất text, hình ảnh
   - Lưu metadata dạng JSON

2. **Sinh script**:
   - Sử dụng AI (Gemini hoặc Qwen) để sinh script
   - Tối ưu hóa nội dung cho bài giảng
   - Lưu script cho từng slide

3. **Tạo audio**:
   - Chuyển script thành giọng nói
   - Sử dụng Google Text-to-Speech
   - Tạo file MP3 cho từng slide

4. **Tạo video**:
   - Kết hợp hình ảnh slide và audio
   - Tạo video cho từng slide
   - Gộp tất cả thành video cuối cùng
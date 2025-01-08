# README: Chuyển Slide Thành Video Bài Giảng

## Mô tả Dự án

Dự án này tự động hóa quá trình chuyển đổi các slide thành video bài giảng hoàn chỉnh, hỗ trợ giáo viên trong việc chuẩn bị nội dung bài giảng và mang lại trải nghiệm học tập trực quan cho học sinh. Hệ thống được chia thành các bước:

1. **Extract Metadata**: Trích xuất nội dung và hình ảnh từ slide.
2. **Slide to Script**: Chuyển đổi nội dung slide thành kịch bản.
3. **Script to Audio**: Chuyển đổi kịch bản thành audio.
4. **Audio and Slide to Video**: Kết hợp slide và audio để tạo video bài giảng.

## Cấu trúc Thư mục

```
project/
│
├── data/
│   ├── input/          # Slide gốc (file PowerPoint hoặc PDF)
│   ├── metadata/       # Metadata trích xuất từ slide (JSON)
│   ├── scripts/        # Kịch bản bài giảng
│   ├── audio/          # File âm thanh (MP3)
│   └── output/         # Video bài giảng
│
├── scripts/
│   ├── extract_metadata.py  # Trích xuất metadata từ slide
│   ├── slide_to_script.py   # Chuyển đổi slide thành kịch bản
│   ├── script_to_audio.py   # Chuyển đổi kịch bản thành âm thanh
│   └── audio_slide_to_video.py # Tạo video từ slide và âm thanh
│
├── README.md           # Mô tả dự án
└── requirements.txt     # Danh sách thư viện Python cần thiết
```

## Hướng dẫn Sử dụng

### 1. Cài đặt môi trường

Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

### 2. Các bước thực hiện

Bạn có thể chạy dòng lệnh sau để xem giao diện upload slide đơn giản
```bash
streamlit run app.py
```

Hoặc bạn có thể chạy thử để test từng phase của project chạy
#### a. Trích xuất Metadata

Chạy script để trích xuất metadata từ slide:

```bash
python scripts/extract_metadata.py
```

File metadata sẽ được lưu trong thư mục `data/metadata/`.

#### b. Chuyển đổi Kịch bản thành Audio

Chạy script để chuyển kịch bản thành audio:

```bash
python scripts/script_to_audio.py
```

File audio sẽ được lưu trong thư mục `data/audio/`.


## Yêu cầu Hệ thống

- Python 3.8 trở lên
- Thư viện:
  - `transformers`
  - `gtts`
  - `moviepy`
  - `python-pptx`
  - `pdf2image`


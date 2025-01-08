import os
from gtts import gTTS

def create_folder(path):
    """Tạo thư mục nếu chưa tồn tại."""
    if not os.path.exists(path):
        os.makedirs(path)

def text_to_audio(script_path, output_folder, language="vi"):
    """Chuyển đổi script thành audio với ngôn ngữ tiếng Việt."""
    create_folder(output_folder)

    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Script file {script_path} không tồn tại.")

    import json
    with open(script_path, "r", encoding="utf-8") as f:
        scripts = json.load(f)

    for script in scripts:
        slide_number = script.get("slide_number", "unknown")
        title = script.get("title", "Untitled")
        content = script.get("script", "")

        if not content.strip():
            print(f"Slide {slide_number} không có nội dung để chuyển đổi.")
            continue

        audio = gTTS(text=content, lang=language, slow=False)
        audio_filename = f"slide_{slide_number}.mp3"
        audio_path = os.path.join(output_folder, audio_filename)

        audio.save(audio_path)
        print(f"Slide {slide_number}: Audio đã được lưu tại {audio_path}.")

if __name__ == "__main__":
    script_path = "data/scripts/scripts.json"
    output_folder = "data/audio"
    text_to_audio(script_path, output_folder)

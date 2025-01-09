import os
from moviepy.editor import *
import json
from pdf2image import convert_from_path
from comtypes import client
from moviepy.config import change_settings

# Thêm đường dẫn đến Poppler và ImageMagick
POPPLER_PATH = r"C:\Users\truon\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
IMAGEMAGICK_BINARY = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"  

change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_BINARY})

def convert_pptx_to_pdf(pptx_path, pdf_path):
    """Chuyển đổi PPTX thành PDF."""
    powerpoint = client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = True
    presentation = powerpoint.Presentations.Open(os.path.abspath(pptx_path))
    presentation.SaveAs(os.path.abspath(pdf_path), 32)  
    presentation.Close()
    powerpoint.Quit()


def convert_pdf_to_images(pdf_path, output_folder):
    """Chuyển đổi PDF thành hình ảnh."""
    os.makedirs(output_folder, exist_ok=True)
    try:
        pages = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
        for i, page in enumerate(pages):
            slide_path = os.path.join(output_folder, f"slide_{i + 1}.png")
            page.save(slide_path, "PNG")
            print(f"Đã lưu hình ảnh: {slide_path}")
    except Exception as e:
        print(f"Lỗi khi chuyển đổi PDF sang hình ảnh: {str(e)}")
        raise


def extract_slides(input_file, output_folder):
    """Trích xuất các slide từ file PPTX hoặc PDF và lưu thành hình ảnh."""
    os.makedirs(output_folder, exist_ok=True)
    file_extension = os.path.splitext(input_file)[1].lower()

    if file_extension == ".pptx":
        pdf_path = os.path.splitext(input_file)[0] + ".pdf"
        convert_pptx_to_pdf(input_file, pdf_path)
        convert_pdf_to_images(pdf_path, output_folder)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)  
    elif file_extension == ".pdf":
        convert_pdf_to_images(input_file, output_folder)
    else:
        raise ValueError("Unsupported file type. Please upload a PPTX or PDF file.")


def create_video_for_each_slide(slides_folder, audio_folder, scripts_file, output_folder):
    """Tạo video cho từng slide từ hình ảnh, audio và script."""
    os.makedirs(output_folder, exist_ok=True)

    with open(scripts_file, "r", encoding="utf-8") as f:
        scripts = json.load(f)

    for script in scripts:
        slide_number = script.get("slide_number", "unknown")
        script_text = script.get("script", "")

        slide_path = os.path.join(slides_folder, f"slide_{slide_number}.png")
        audio_path = os.path.join(audio_folder, f"slide_{slide_number}.mp3")
        output_video_path = os.path.join(output_folder, f"slide_{slide_number}.mp4")

        if not os.path.exists(slide_path) or not os.path.exists(audio_path):
            if not os.path.exists(slide_path):
                print(f"Slide {slide_number}: Thiếu file hình ảnh tại {slide_path}.")
            if not os.path.exists(audio_path):
                print(f"Slide {slide_number}: Thiếu file audio tại {audio_path}.")
            continue

        try:
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration

            slide_image = ImageClip(slide_path).set_duration(duration)
            
            final_clip = slide_image.set_audio(audio_clip)

            final_clip.write_videofile(output_video_path, 
                                     fps=24, 
                                     codec="libx264",
                                     audio_codec="aac")
            
            print(f"Video cho Slide {slide_number} đã được lưu tại {output_video_path}.")
            
            audio_clip.close()
            final_clip.close()
            
        except Exception as e:
            print(f"Lỗi khi tạo video cho slide {slide_number}: {str(e)}")


def concatenate_videos(video_folder, output_path):
    """Gộp tất cả video slides thành một video duy nhất."""
    try:
        video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]
        video_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
        
        if not video_files:
            print("Không tìm thấy file video nào để gộp.")
            return
        
        print("Đang gộp các video...")
        
        video_clips = []
        for video_file in video_files:
            video_path = os.path.join(video_folder, video_file)
            video_clip = VideoFileClip(video_path)
            video_clips.append(video_clip)
            print(f"Đã thêm {video_file}")
        
        final_clip = concatenate_videoclips(video_clips)
        
        final_clip.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio_codec="aac"
        )
        
        print(f"Đã gộp thành công! Video được lưu tại: {output_path}")
        
        for clip in video_clips:
            clip.close()
        final_clip.close()
        
    except Exception as e:
        print(f"Lỗi khi gộp video: {str(e)}")


if __name__ == "__main__":
    input_file = "./data/input/hbh.pptx"
    slides_folder = "./data/input/slides"
    audio_folder = "./data/audio"
    scripts_file = "./data/scripts/scripts.json"
    output_folder = "./data/output/videos"
    final_video_path = "./data/output/final_lecture.mp4"

    os.makedirs(output_folder, exist_ok=True)

    try:
        extract_slides(input_file, slides_folder)
        create_video_for_each_slide(slides_folder, audio_folder, scripts_file, output_folder)
        
        print("\nBắt đầu gộp video...")
        concatenate_videos(output_folder, final_video_path)
        
    except Exception as e:
        print(f"Lỗi: {str(e)}")

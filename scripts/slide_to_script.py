import json
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'qwen')

def setup_gemini():
    """Khởi tạo Gemini model."""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        return model
    except Exception as e:
        print(f"Lỗi khi khởi tạo Gemini: {str(e)}")
        raise

def setup_qwen():
    """Khởi tạo Qwen model và tokenizer."""
    model_name = "Qwen/Qwen2-1.5B"
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="cpu",
            trust_remote_code=True,
            torch_dtype=torch.float32
        )
        return model, tokenizer
    except Exception as e:
        print(f"Lỗi khi tải Qwen: {str(e)}")
        raise

def generate_with_gemini(model, prompt, max_length=1000):
    """Sinh script bài giảng sử dụng Gemini."""
    try:
        system_prompt = """Bạn là một giảng viên chuyên nghiệp. Nhiệm vụ của bạn là tạo ra một bài giảng từ nội dung slide được cung cấp.
        Hãy tạo ra một bài giảng tự nhiên, dễ hiểu và lôi cuốn, bao gồm:
        1. Giới thiệu nội dung
        2. Giải thích các khái niệm
        3. Liên hệ với ví dụ thực tế nếu có
        4. Nhấn mạnh các điểm quan trọng
        Đảm bảo giọng văn tự nhiên như đang giảng bài trực tiếp."""

        full_prompt = f"{system_prompt}\n\nNội dung slide:\n{prompt}\n\nBài giảng:"
        
        response = model.generate_content(full_prompt)
        return response.text

    except Exception as e:
        print(f"Lỗi khi sinh script với Gemini: {str(e)}")
        return ""

def generate_with_qwen(model, tokenizer, prompt, max_length=1000):
    """Sinh script bài giảng sử dụng Qwen."""
    try:
        system_prompt = """Bạn là một giảng viên chuyên nghiệp. Nhiệm vụ của bạn là tạo ra một bài giảng từ nội dung slide được cung cấp.
        Hãy tạo ra một bài giảng tự nhiên, dễ hiểu và lôi cuốn, bao gồm:
        1. Giới thiệu nội dung
        2. Giải thích các khái niệm
        3. Liên hệ với ví dụ thực tế nếu có
        4. Nhấn mạnh các điểm quan trọng
        Đảm bảo giọng văn tự nhiên như đang giảng bài trực tiếp."""

        full_prompt = f"{system_prompt}\n\nNội dung slide:\n{prompt}\n\nBài giảng:"

        inputs = tokenizer(full_prompt, return_tensors="pt")
        outputs = model.generate(
            inputs.input_ids,
            max_length=max_length,
            num_beams=5,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
        
        script = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return script.split("Bài giảng:")[-1].strip()

    except Exception as e:
        print(f"Lỗi khi sinh script với Qwen: {str(e)}")
        return ""

def process_slide(model_type, model, tokenizer, slide_data):
    """Xử lý từng slide để tạo script."""
    try:
        slide_number = slide_data.get("slide_number", "unknown")
        title = slide_data.get("title", "")
        text_content = slide_data.get("text_content", "")
        description = slide_data.get("description", "")
        
        prompt = f"""Tiêu đề: {title}
Nội dung chính: {text_content}
Mô tả hình ảnh: {description}"""

        if model_type == "gemini":
            script = generate_with_gemini(model, prompt)
        else:  
            script = generate_with_qwen(model, tokenizer, prompt)

        return {
            "slide_number": slide_number,
            "script": script
        }
    except Exception as e:
        print(f"Lỗi khi xử lý slide {slide_number}: {str(e)}")
        return {
            "slide_number": slide_number,
            "script": "Không thể tạo script cho slide này."
        }

def slide_to_script(input_metadata_path, output_folder, scripts_folder, model_type=None):
    """Xử lý tất cả các slide và tạo script."""
    try:
        os.makedirs(scripts_folder, exist_ok=True)
        
        model_type = model_type or DEFAULT_MODEL
        print(f"Sử dụng model: {model_type}")

        print("Đang tải model...")
        if model_type == "gemini":
            model = setup_gemini()
            tokenizer = None
        else:
            model, tokenizer = setup_qwen()
        
        print("Đang đọc metadata...")
        with open(input_metadata_path, "r", encoding="utf-8") as f:
            slides = json.load(f)
        
        print("Đang tạo script cho từng slide...")
        scripts = []
        for slide in slides:
            print(f"Đang xử lý slide {slide.get('slide_number', 'unknown')}...")
            script_data = process_slide(model_type, model, tokenizer, slide)
            scripts.append(script_data)
        
        output_path = os.path.join(scripts_folder, "scripts.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(scripts, f, ensure_ascii=False, indent=4)
        
        print(f"Đã lưu scripts tại: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Lỗi trong quá trình tạo script: {str(e)}")
        raise

if __name__ == "__main__":
    input_metadata_path = "data/metadata/hbh.json"
    output_folder = "data/metadata"
    scripts_folder = "data/scripts"
    
    slide_to_script(input_metadata_path, output_folder, scripts_folder, model_type='gemini')

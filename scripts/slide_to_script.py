import os
from transformers import AutoTokenizer, AutoModelForCausalLM

def create_folder(path):
    """Tạo thư mục nếu chưa tồn tại."""
    if not os.path.exists(path):
        os.makedirs(path)

def load_model_and_tokenizer(model_name="qwen-2-1b"):
    """Tải mô hình và tokenizer."""
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        load_in_8bit=True,  # Quantization to 8-bit for performance
        device_map="auto"
    )
    return model, tokenizer

def process_slide_text(slide_text, model, tokenizer):
    """Chuyển đổi nội dung slide thành kịch bản."""
    prompt = f"Hãy tạo một đoạn script chi tiết cho nội dung sau:\n{slide_text}\n"
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    output = model.generate(inputs["input_ids"], max_length=500, num_beams=5, early_stopping=True)
    generated_script = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_script

def slide_to_script(metadata_path, output_folder):
    """Xử lý metadata và tạo script cho từng slide."""
    # Tạo thư mục lưu script
    create_folder(output_folder)

    # Tải mô hình và tokenizer
    model, tokenizer = load_model_and_tokenizer()

    # Đọc metadata từ file JSON
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Metadata file {metadata_path} không tồn tại.")

    import json
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Xử lý từng slide
    scripts = []
    for slide in metadata:
        slide_number = slide.get("slide_number", "unknown")
        slide_title = slide.get("title", "Untitled")
        slide_text = slide.get("text_content", "")

        # Sinh script từ nội dung slide
        script = process_slide_text(slide_text, model, tokenizer)
        scripts.append({
            "slide_number": slide_number,
            "title": slide_title,
            "script": script
        })

    # Lưu kết quả thành file JSON
    output_path = os.path.join(output_folder, "scripts.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(scripts, f, ensure_ascii=False, indent=4)

    print(f"Scripts đã được lưu tại: {output_path}")
    return scripts

if __name__ == "__main__":
    # Đường dẫn metadata và thư mục output
    metadata_path = "data/metadata/Vintern-1B Architecture.json"  # Cập nhật theo tên file metadata
    output_folder = "data/scripts_test"

    # Chạy hàm slide_to_script
    slide_to_script(metadata_path, output_folder)
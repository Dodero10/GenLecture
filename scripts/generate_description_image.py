import torch
import torchvision.transforms as T
from PIL import Image
from torchvision.transforms.functional import InterpolationMode
from transformers import AutoModel, AutoTokenizer
import google.generativeai as genai
from dotenv import load_dotenv
import os


load_dotenv()


GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'vintern')

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)

def get_project_root():
    """Lấy đường dẫn gốc của project."""
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    return project_root

def setup_gemini():
    """Khởi tạo Gemini model."""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-pro-vision-latest')
        return model
    except Exception as e:
        print(f"Lỗi khi khởi tạo Gemini: {str(e)}")
        raise

def setup_vintern():
    """Khởi tạo Vintern model."""
    try:
        model = AutoModel.from_pretrained(
            "5CD-AI/Vintern-1B-v2",
            torch_dtype=torch.float32,  
            low_cpu_mem_usage=True,
            trust_remote_code=True,
            device_map="cpu"
        ).eval()
        
        tokenizer = AutoTokenizer.from_pretrained(
            "5CD-AI/Vintern-1B-v2", 
            trust_remote_code=True, 
            use_fast=False
        )
        return model, tokenizer
    except Exception as e:
        print(f"Lỗi khi tải Vintern: {str(e)}")
        raise

def build_transform(input_size=448):
    """Tạo hàm transform cho hình ảnh."""
    transform = T.Compose([
        T.Resize((input_size, input_size), interpolation=InterpolationMode.BICUBIC),
        T.ToTensor(),
        T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])
    return transform

def load_image(image_path, input_size=448):
    """Tải và xử lý hình ảnh."""
    image = Image.open(image_path).convert('RGB')
    if DEFAULT_MODEL == 'vintern':
        transform = build_transform(input_size)
        return transform(image).unsqueeze(0)  
    return image

def generate_with_gemini(model, image):
    """Tạo mô tả hình ảnh sử dụng Gemini Vision."""
    try:
        prompt = """Hãy mô tả chi tiết nội dung của hình ảnh này bằng tiếng Việt.
        Bao gồm:
        1. Các đối tượng chính trong hình
        2. Bố cục và vị trí của các đối tượng
        3. Màu sắc và chi tiết quan trọng
        4. Nội dung văn bản nếu có
        """
        
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        response = model.generate_content(
            contents=[prompt, image],
            generation_config=generation_config
        )
        
        return response.text
    except Exception as e:
        print(f"Lỗi khi sinh mô tả với Gemini: {str(e)}")
        return ""

def generate_with_vintern(model, tokenizer, pixel_values):
    """Tạo mô tả hình ảnh sử dụng Vintern."""
    try:
        question = "<image>\nMô tả hình ảnh chi tiết."
        generation_config = {
            "max_new_tokens": 1024,
            "do_sample": True,
            "num_beams": 3,
            "repetition_penalty": 2.5,
        }
        response, _ = model.chat(
            tokenizer, 
            pixel_values, 
            question, 
            generation_config, 
            history=None, 
            return_history=True
        )
        return response
    except Exception as e:
        print(f"Lỗi khi sinh mô tả với Vintern: {str(e)}")
        return ""

def generate_image_description(image_path, model_type=None):
    """
    Tạo mô tả hình ảnh sử dụng model được chọn.
    Args:
        image_path: Đường dẫn đến file hình ảnh
        model_type: 'gemini' hoặc 'vintern' (mặc định theo DEFAULT_MODEL)
    """
    try:

        model_type = model_type or DEFAULT_MODEL
        print(f"Sử dụng model: {model_type}")

        image = load_image(image_path)

        if model_type == "gemini":
            model = setup_gemini()
            description = generate_with_gemini(model, image)
        else: 
            model, tokenizer = setup_vintern()
            description = generate_with_vintern(model, tokenizer, image)

        return description

    except Exception as e:
        print(f"Lỗi khi tạo mô tả hình ảnh: {str(e)}")
        return "Không thể tạo mô tả cho hình ảnh này."

if __name__ == "__main__":
    project_root = get_project_root()
    image_path = os.path.join(project_root, "data", "metadata", "hbh", "slide_1_image_1.png")
    
    if not os.path.exists(image_path):
        print(f"Không tìm thấy file ảnh tại: {image_path}")
    else:
        description = generate_image_description(image_path, model_type='gemini')
        print(description)

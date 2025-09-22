from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

# Khởi tạo ứng dụng Flask
app = Flask(__name__)
CORS(app)

# ====================================================================================
# BƯỚC 1: DÁN KHÓA API CỦA BẠN VÀO DÒNG DƯỚI ĐÂY
# ====================================================================================
api_key = "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"

client = OpenAI(api_key=api_key)

@app.route('/generate_image', methods=['POST'])
def generate_image_api():
    try:
        # Lấy prompt từ yêu cầu POST của trang HTML
        data = request.json
        prompt = data.get('prompt')

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        print(f"Received prompt: {prompt}")
        
        # Gọi API OpenAI để tạo ảnh
        # DALL-E 3 trả về URL, không phải base64
        res = client.images.generate(
            prompt=prompt,
            model="dall-e-3",
            size="1024x1024"
        )
        
        print("✅ Yêu cầu thành công!")
        
        # Hiển thị thông tin response
        print("\n" + "=" * 30)
        print("Thông tin phản hồi:")
        print("=" * 30)
        
        image_url = res.data[0].url
        revised_prompt = res.data[0].revised_prompt
        
        print(f"\n URL ảnh: {image_url}")
        if revised_prompt:
            print(f"Sửa đổi yêu cầu (revised prompt): {revised_prompt}")
            
        return jsonify({"image_url": image_url})

    except Exception as e:
        print(f"❌ Xảy ra lỗi:")
        print(f"Loại lỗi: {type(e).__name__}")
        print(f"Thông điệp lỗi: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Chạy máy chủ trên cổng 5000, bật chế độ gỡ lỗi (debug)
    app.run(debug=True, port=5000)
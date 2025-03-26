import openai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import uvicorn

# Tải các biến môi trường từ tệp .env
load_dotenv()

# Lấy API key từ biến môi trường
openai.api_key = os.getenv("OPENAI_API_KEY")

# Kiểm tra xem API key có được thiết lập không
if not openai.api_key:
    print("API key chưa được thiết lập. Vui lòng thiết lập OPENAI_API_KEY.")
    exit()

# Khởi tạo FastAPI app
app = FastAPI()


# Thêm CORS middleware để cho phép frontend giao tiếp với backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP
    allow_headers=["*"],  # Cho phép tất cả các tiêu đề
)

# Định nghĩa mô hình yêu cầu từ người dùng
class UserQuestion(BaseModel):
    user_question: str


# Tạo hàm trả lời câu hỏi từ GPT-4
def get_gpt4_reply(messages):
    try:
        chat_completion = openai.ChatCompletion.create(
            model="gpt-4",  # Sử dụng GPT-4
            messages=messages
        )
        return chat_completion["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        return None

# Danh sách tin nhắn ban đầu
messages = [{"role": "system", "content": "Hi ChatGPT, You are a helpful assistant!"}]

@app.post("/chat/")
async def chatbot(request: UserQuestion):
    user_question = request.user_question
    if user_question:
        messages.append({"role": "user", "content": user_question})
        reply = get_gpt4_reply(messages)
        if reply:
            messages.append({"role": "assistant", "content": reply})
            return {"answer": reply}
        else:
            raise HTTPException(status_code=500, detail="Lỗi khi gọi GPT-4.")
    else:
        raise HTTPException(status_code=400, detail="Không có câu hỏi người dùng.")

# Tự động chạy FastAPI khi tệp được chạy trực tiếp
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

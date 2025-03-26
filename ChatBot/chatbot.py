import tkinter as tk
from tkinter import messagebox
import requests

# URL của endpoint FastAPI
API_URL = "http://localhost:8000/chat/"

def send_question():
    question = entry.get()
    if question:
        response = requests.post(API_URL, json={"user_question": question})
        if response.status_code == 200:
            result = response.json()
            answer = result.get("answer", "Không có câu trả lời.")
            messagebox.showinfo("Trả lời từ GPT-3", f"Câu hỏi: {question}\nTrả lời: {answer}")
        else:
            messagebox.showerror("Lỗi", "Có lỗi xảy ra khi kết nối với API.")
    else:
        messagebox.showwarning("Lỗi nhập liệu", "Vui lòng nhập câu hỏi.")

# Cấu hình cửa sổ chính
root = tk.Tk()
root.title("Chatbot với GPT-3")

# Tạo một label cho ô nhập câu hỏi
entry_label = tk.Label(root, text="Nhập câu hỏi của bạn:")
entry_label.pack(pady=10)
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Tạo nút gửi câu hỏi
send_button = tk.Button(root, text="Gửi câu hỏi", command=send_question)
send_button.pack(pady=10)

# Bắt đầu giao diện
root.mainloop()

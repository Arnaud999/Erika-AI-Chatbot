from customtkinter import *
import tkinter.messagebox as msgbh
import requests
import config
import time
import threading
from PIL import Image, ImageTk

# ----------------- API Function -----------------
API_URL = config.API_URL
MODEL = config.MODEL
Model_name = config.Model_name

def AIChat(user_message):
    headers = {
        "Authorization": f"Bearer {config.API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": user_message},
                      {"role": "system", "content": "You are Erika, a friendly, helpful AI chatbot. Always call yourself Erika. Respond in a cheerful tone and provide helpful answers. "}]
    }

    response = requests.post(API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# ----------------- GUI Setup -----------------
set_appearance_mode("dark")
set_default_color_theme("blue")

app = CTk()
app.minsize(width=300, height=400)
app.maxsize(1920, 1080)
app.geometry("500x600")
app.title("Erika AI Chatbot")

app.iconbitmap("images/logo.ico")

bg_img = Image.open("images/background.png")
bg_ctk_image = CTkImage(light_image=bg_img, dark_image=bg_img, size=(1920, 1080))

# Place image to cover entire window
bg_label = CTkLabel(app, image=bg_ctk_image, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ----------------- Chat Frame -----------------
chat_frame = CTkFrame(app)
chat_frame.pack(padx=10, pady=(10,0), fill="both", expand=True)  # Chat frame grows

bg_label = CTkLabel(chat_frame, image=bg_ctk_image, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

chat_text = CTkTextbox(chat_frame,state="disabled",wrap="word",font=("Helvetica", 14),fg_color="#000000")
chat_text.pack(padx=10, pady=10, fill="both", expand=True)  # expand=True lets it grow/shrink


# ----------------- Input Frame -----------------
input_frame = CTkFrame(app,fg_color="#000000")
input_frame.pack(side="bottom", padx=10, pady=10, fill="x")  # always at bottom


user_input = CTkTextbox(input_frame ,height=60, corner_radius=8, border_width=1, font=("Helvetica", 17), fg_color="#000000")
user_input.pack(side="left", padx=5, pady=5, fill="x", expand=True)

# ----------------- Header / Logo -----------------

def show_popup():
    msgbh.showinfo("Made By:", "github.com/KrishnaSingh-bit/")
    
header_img = Image.open("images/logo1.png") 
header_ctk_image = CTkImage(light_image=header_img, dark_image=header_img, size=(200, 50))

bottom_frame = CTkFrame(app, height=80,fg_color="#000000")
bottom_frame.pack(side="top", fill="x",before=chat_frame)

header_label = CTkButton(bottom_frame, image=header_ctk_image, text="",hover_color="#000000",fg_color="#000000",command= show_popup)  # text="" removes any label text
header_label.pack(fill = "x")

# ----------------- Helper Functions -----------------
def display_message(sender, message):
    """Insert message with different colors for user and AI"""
    chat_text.configure(state="normal")
    if sender == "You":
        chat_text.insert("end", f"{sender}: {message}\n", ("user",))
    else:
        chat_text.insert("end", f"{sender}: ", ("ai_name",))
        chat_text.see("end")
        # Type out AI message slowly
        for char in message:
            chat_text.insert("end", char)
            chat_text.see("end")
            chat_text.update()
            time.sleep(0.02)  # delay per character (adjust for typing speed)
        chat_text.insert("end", "\n\n")
    chat_text.configure(state="disabled")
    chat_text.see("end")

# Add tags for coloring
chat_text.tag_config("user", foreground="#00ff00")      # Green for You
chat_text.tag_config("ai_name", foreground="#00bfff")  # Blue bold for Erika

def send_message(event=None):
    msg = user_input.get("0.0", "end").strip()
    if msg == "":
        return
    display_message("You", msg)
    user_input.delete("0.0", "end")
    
    # Run AI response in a separate thread to avoid freezing GUI
    threading.Thread(target=ai_response, args=(msg,), daemon=True).start()

def ai_response(user_msg):
    response = AIChat(user_msg)
    display_message("Erika AI", response)

send_img = Image.open("images/send1.png") 
send_ctk_img = CTkImage(light_image=send_img, dark_image=send_img,size=(120, 30))

send_button = CTkButton(input_frame, image= send_ctk_img ,text="", width=100, command=send_message,fg_color="#222222",hover_color="#222222")
send_button.pack(side="right", padx=5, pady=5)

# Bind Enter key
user_input.bind("<Return>", send_message)

# ----------------- Welcome Message -----------------
chat_text.configure(state="normal")
chat_text.insert("end", f"Erika AI: Hi there! I am your AI chatbot powered by {Model_name} model.\nHow can I assist you today?\n\n")
chat_text.configure(state="disabled")

app.mainloop()

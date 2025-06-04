import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
from PIL import Image, ImageTk
from Aice_Lit_Pro_Review import deep_lit_review
from Aice_Lang_Pro_Review import deep_lang_review
from review_personal import deep_personal_review
import sys

# Set appearance and theme                   Future update maybe
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("1000x750")
app.title("EMA ✍️")

# Splash screen
splash = ctk.CTkToplevel(app)
splash.geometry("1000x750")
splash.overrideredirect(True)
splash.lift()
splash.attributes("-topmost", True)

texts = [
    ("Welcome to", ("Helvetica", 28), "#333", 180),
    ("EMA", ("Helvetica", 42, "bold"), "#FFA69E", 240),
    ("Made by Adam Awadalla", ("Arial", 16), "#666", 290),
    ("Your cozy, professional essay-reviewing companion\nto a better academic future.", ("Arial", 12), "#444", 330)
]

for text, font, color, y in texts:
    label = ctk.CTkLabel(splash, text=text, font=font, text_color=color)
    label.place(relx=0.5, y=y, anchor="center")

def fade_out(opacity=1.0):
    if opacity <= 0:
        splash.destroy()
    else:
        splash.attributes("-alpha", opacity)
        app.after(100, fade_out, opacity - 0.05)

app.after(1800, fade_out)

# Clock
clock_label = ctk.CTkLabel(app, font=("Courier", 16))
clock_label.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

def update_clock():
    now = datetime.now().strftime("%I:%M:%S %p")
    clock_label.configure(text=now)
    app.after(1000, update_clock)

update_clock()

# Title
title = ctk.CTkLabel(app, text="EssayMaster AI", font=("Helvetica", 28, "bold"), text_color="#FFA69E")
title.pack(pady=15)

# Radio Buttons
review_type = ctk.StringVar(value="AICE Literature")
radio_frame = ctk.CTkFrame(app)
radio_frame.pack(pady=10)

for label in ["AICE Literature", "AICE Language", "Personal Writing"]:
    ctk.CTkRadioButton(radio_frame, text=label, variable=review_type, value=label).pack(side="left", padx=15)

# Essay Input
essay_label = ctk.CTkLabel(app, text="📄 Paste Your Essay Below:", font=("Arial", 14))
essay_label.pack(pady=(10, 0))
essay_input = ctk.CTkTextbox(app, height=200, width=850, font=("Consolas", 12), wrap="word")
essay_input.pack(pady=10)

# Output Box
output_label = ctk.CTkLabel(app, text="🗘 Feedback Output:", font=("Arial", 14))
output_label.pack(pady=(10, 0))
output_box = ctk.CTkTextbox(app, height=250, width=850, font=("Georgia", 12, "italic"), wrap="word")
output_box.pack(pady=10)
output_box.configure(state="disabled")

# Submit Button
def run_selected_analysis():
    essay_text = essay_input.get("1.0", "end").strip()
    if not essay_text:
        messagebox.showwarning("Missing Text", "Please enter or paste your essay first.")
        return

    selected = review_type.get()
    try:
        if selected == "AICE Literature":
            feedback = deep_lit_review(essay_text)
        elif selected == "AICE Language":
            feedback = deep_lang_review(essay_text)
        elif selected == "Personal Writing":
            feedback = deep_personal_review(essay_text)
        else:
            raise ValueError("Invalid review type selected")

        feedback_str = str(feedback) if feedback else "No feedback returned."
    except Exception as e:
        feedback_str = f"An error occurred during analysis:\n{str(e)}"

    output_box.configure(state="normal")
    output_box.delete("1.0", "end")
    output_box.insert("1.0", feedback_str)
    output_box.configure(state="disabled")

submit_btn = ctk.CTkButton(app, text="🔍 Analyze Essay", command=run_selected_analysis, font=("Arial", 13, "bold"), fg_color="#FFA69E", hover_color="#FF8C8C")
submit_btn.pack(pady=10)

# Clear Output Button
def clear_output():
    output_box.configure(state="normal")
    output_box.delete("1.0", "end")
    output_box.configure(state="disabled")

clear_btn = ctk.CTkButton(app, text="🩹 Clear Feedback", command=clear_output, font=("Arial", 12), fg_color="#FFC1B4", hover_color="#FF8C8C")
clear_btn.pack(pady=(0, 10))

# Export Button
def export_feedback():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[["Text files", "*.txt"]])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(output_box.get("1.0", "end").strip())
        messagebox.showinfo("Export Successful", f"Feedback saved to {file_path}")

export_btn = ctk.CTkButton(app, text="📂 Export Feedback", command=export_feedback, font=("Arial", 12), fg_color="#FFB8A9", hover_color="#FF8C8C")
export_btn.pack(pady=(5, 15))

app.mainloop()

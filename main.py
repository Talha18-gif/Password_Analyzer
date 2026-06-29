import customtkinter as ctk
import threading
from tkinter import messagebox
from analyzer import evaluate_password, generate_strong_password
from hibp import check_pwned_api, HIBPAPIError

# Configure global theme settings
ctk.set_appearance_mode("System")  # Uses OS default (Dark/Light)
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Password Strength Analyzer")
        self.geometry("600x650")
        self.resizable(False, False)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Password Strength Analyzer", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        # Main Frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Password Input
        self.password_var = ctk.StringVar()
        self.password_var.trace_add('write', self.on_password_change)

        self.password_entry = ctk.CTkEntry(
            self.main_frame, 
            textvariable=self.password_var, 
            show="*", 
            placeholder_text="Enter password...", 
            width=400, 
            font=ctk.CTkFont(size=14)
        )
        self.password_entry.pack(pady=(20, 10))

        # Buttons Frame
        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.pack(pady=5)

        self.show_password_var = ctk.BooleanVar(value=False)
        self.show_pwd_checkbox = ctk.CTkCheckBox(
            self.btn_frame, text="Show", variable=self.show_password_var, command=self.toggle_password_visibility
        )
        self.show_pwd_checkbox.grid(row=0, column=0, padx=10)

        self.generate_btn = ctk.CTkButton(
            self.btn_frame, text="Generate Strong Password", command=self.generate_password
        )
        self.generate_btn.grid(row=0, column=1, padx=10)

        # Strength Indicator
        self.strength_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.strength_frame.pack(pady=20, fill="x", padx=40)

        self.strength_label = ctk.CTkLabel(
            self.strength_frame, text="Strength: N/A", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.strength_label.pack(anchor="w")

        self.progress_bar = ctk.CTkProgressBar(self.strength_frame, width=500, height=10)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(5, 10))

        # Feedback text
        self.feedback_textbox = ctk.CTkTextbox(
            self.main_frame, width=500, height=120, state="disabled", wrap="word", font=ctk.CTkFont(size=13)
        )
        self.feedback_textbox.pack(pady=10)

        # HIBP Section
        self.hibp_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.hibp_frame.pack(pady=10, fill="x", padx=40)

        self.check_breach_btn = ctk.CTkButton(
            self.hibp_frame, 
            text="Check Data Breaches (HIBP)", 
            command=self.check_breach, 
            fg_color="#c85a17", 
            hover_color="#9e4712"
        )
        self.check_breach_btn.pack(side="left")

        self.breach_status_label = ctk.CTkLabel(
            self.hibp_frame, text="", font=ctk.CTkFont(size=14)
        )
        self.breach_status_label.pack(side="left", padx=15)
        
        self.pwned_cache = {}

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def on_password_change(self, *args):
        password = self.password_var.get()
        self.update_strength(password)
        self.breach_status_label.configure(text="") # Reset breach status when password changes

    def update_strength(self, password):
        result = evaluate_password(password)
        
        score = result['score']
        percentage = result['score_percentage']
        
        # Determine color and text
        if not password:
            text = "Strength: N/A"
            color = "gray"
            pb_value = 0
        elif score == 0:
            text = "Strength: Very Weak"
            color = "#ff4d4d" # red
        elif score == 1:
            text = "Strength: Weak"
            color = "#ff9933" # orange
        elif score == 2:
            text = "Strength: Fair"
            color = "#ffcc00" # yellow
        elif score == 3:
            text = "Strength: Strong"
            color = "#33cc33" # light green
        else:
            text = "Strength: Very Strong"
            color = "#009933" # dark green
            
        if result.get('is_common', False):
            text += " (Common Password Found!)"
            color = "#ff4d4d"

        pb_value = percentage / 100.0

        self.strength_label.configure(text=text, text_color=color)
        self.progress_bar.set(pb_value)
        self.progress_bar.configure(progress_color=color)

        # Update feedback
        self.feedback_textbox.configure(state="normal")
        self.feedback_textbox.delete("1.0", "end")
        
        if password:
            self.feedback_textbox.insert("end", f"Mathematical Entropy: {result['math_entropy']} bits (H = L × log₂(N))\n")
            self.feedback_textbox.insert("end", f"Estimated time to crack: {result['time_to_crack']}\n\n")
            if result['warning']:
                self.feedback_textbox.insert("end", f"⚠️ Warning: {result['warning']}\n\n")
            if result['suggestions']:
                self.feedback_textbox.insert("end", "Suggestions:\n")
                for s in result['suggestions']:
                    self.feedback_textbox.insert("end", f"- {s}\n")
            if not result['warning'] and not result['suggestions'] and score >= 3:
                self.feedback_textbox.insert("end", "✅ This password looks great!")
        
        self.feedback_textbox.configure(state="disabled")

    def generate_password(self):
        new_pwd = generate_strong_password(16)
        self.password_var.set(new_pwd)
        if not self.show_password_var.get():
            self.show_password_var.set(True)
            self.toggle_password_visibility()

    def check_breach(self):
        password = self.password_var.get()
        if not password:
            messagebox.showwarning("Warning", "Please enter a password to check.")
            return

        self.breach_status_label.configure(text="Checking API...", text_color="gray")
        self.check_breach_btn.configure(state="disabled")
        
        threading.Thread(target=self._check_breach_bg, args=(password,), daemon=True).start()

    def _check_breach_bg(self, password):
        try:
            if password in self.pwned_cache:
                count = self.pwned_cache[password]
            else:
                count, _, _, _ = check_pwned_api(password)
                self.pwned_cache[password] = count

            self.after(0, self._update_breach_ui, count)
        except HIBPAPIError as e:
            self.after(0, self._update_breach_ui_error, str(e))
        except Exception as e:
            self.after(0, self._update_breach_ui_error, "Unknown error occurred.")
            
    def _update_breach_ui(self, count):
        self.check_breach_btn.configure(state="normal")
        if count > 0:
            self.breach_status_label.configure(text=f"Pwned! Found {count:,} times.", text_color="#ff4d4d")
        else:
            self.breach_status_label.configure(text="Safe! Not found in breaches.", text_color="#33cc33")

    def _update_breach_ui_error(self, error_msg):
        self.check_breach_btn.configure(state="normal")
        self.breach_status_label.configure(text=error_msg, text_color="#ff4d4d")


if __name__ == "__main__":
    app = App()
    app.mainloop()

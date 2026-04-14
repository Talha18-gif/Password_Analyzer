import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import requests
import random
import string
import threading
import os
import sys
import secrets

# ---------------- Helper: resource_path (needed for exe bundling) ---------------- #
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller exe"""
    try:
        base_path = sys._MEIPASS  # PyInstaller sets this
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ---------------- Password Strength Analyzer Functions ---------------- #
def check_password_strength(password):
    """Returns a strength score (0-100) and list of suggestions."""
    suggestions = []
    score = 0

    # length
    if len(password) < 8:
        suggestions.append("Password too short (min 8 chars).")
    else:
        score += 20

    # lowercase
    if any(c.islower() for c in password):
        score += 15
    else:
        suggestions.append("Add lowercase letters.")

    # uppercase
    if any(c.isupper() for c in password):
        score += 15
    else:
        suggestions.append("Add uppercase letters.")

    # digits
    if any(c.isdigit() for c in password):
        score += 15
    else:
        suggestions.append("Add digits.")

    # special chars
    if any(c in string.punctuation for c in password):
        score += 15
    else:
        suggestions.append("Add special characters (!,@,#,$, etc).")

    # extra points for length >=12
    if len(password) >= 12:
        score += 20
    else:
        suggestions.append("Use at least 12 characters for strong security.")

    # Some minimal penalization for obvious weak patterns
    if password.isdigit() or password.isalpha():
        # only digits or only letters -> reduce score by 20 (but keep >=0)
        score = max(score - 20, 0)
        suggestions.append("Avoid using only letters or only digits.")

    return min(score, 100), suggestions


def generate_strong_password(length=12):
    """Generates a strong random password with enforced diversity using secrets."""
    if length < 4:
        raise ValueError("Minimum length is 4")

    # ensure at least one of each required category
    categories = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation),
    ]
    # fill remaining
    all_chars = string.ascii_letters + string.digits + string.punctuation
    for _ in range(length - 4):
        categories.append(secrets.choice(all_chars))

    random.shuffle(categories)  # pseudo-random shuffle is fine for ordering
    return ''.join(categories)


# ---------------- HIBP Breach Check Functions ---------------- #
def check_pwned_api(password, timeout=10):
    """
    Returns a tuple (count, prefix, matched_suffix, matched_count)
    Uses k-anonymity model (only prefix sent).
    """
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f'https://api.pwnedpasswords.com/range/{prefix}'
    headers = {'User-Agent': 'PasswordStrengthAnalyzer/1.0 (student project)'}
    resp = requests.get(url, headers=headers, timeout=timeout)
    if resp.status_code != 200:
        raise RuntimeError(f"HIBP API returned {resp.status_code}")

    matched_suffix = None
    matched_count = 0
    for line in resp.text.splitlines():
        if ':' not in line:
            continue
        h, cnt = line.split(':', 1)
        if h == suffix:
            try:
                matched_suffix = h
                matched_count = int(cnt)
            except Exception:
                matched_suffix = h
                matched_count = 1
            break

    total = matched_count
    return total, prefix, matched_suffix, matched_count


# ---------------- Tkinter GUI Class ---------------- #
class PasswordGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Analyzer")
        self.root.geometry("720x520")

        frame = ttk.Frame(root, padding=15)
        frame.pack(fill='both', expand=True)

        # Entry + buttons
        ttk.Label(frame, text="Enter Password:").grid(row=0, column=0, sticky='w')
        self.password_entry = ttk.Entry(frame, width=40, show="*")
        self.password_entry.grid(row=0, column=1, padx=5, pady=5)

        self.show_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Show", variable=self.show_var,
                        command=self.toggle_password).grid(row=0, column=2)

        ttk.Button(frame, text="Check Strength", command=self.check_strength)\
            .grid(row=1, column=1, pady=6, sticky='w')

        ttk.Button(frame, text="Generate Password", command=self.generate_password)\
            .grid(row=1, column=2, pady=6, sticky='w')

        # Strength label + colored indicator
        self.strength_label = ttk.Label(frame, text="Strength: N/A")
        self.strength_label.grid(row=2, column=0, sticky='w', pady=(6,0))

        # small colored circle as indicator
        self.indicator_canvas = tk.Canvas(frame, width=16, height=16, highlightthickness=0)
        self.indicator_canvas.grid(row=2, column=1, sticky='w', pady=(6,0))
        # draw circle
        self.indicator_circle = self.indicator_canvas.create_oval(2, 2, 14, 14, fill='gray')

        # Progress bar styling (make sure to use a theme that supports color)
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            # fallback if 'clam' not available
            try:
                style.theme_use('default')
            except Exception:
                pass

        # Configure styles - troughcolor helps show the track
        style.configure("Weak.Horizontal.TProgressbar", troughcolor='#e6e6e6', background='red')
        style.configure("Medium.Horizontal.TProgressbar", troughcolor='#e6e6e6', background='orange')
        style.configure("Strong.Horizontal.TProgressbar", troughcolor='#e6e6e6', background='blue')
        style.configure("VeryStrong.Horizontal.TProgressbar", troughcolor='#e6e6e6', background='green')

        self.progress = ttk.Progressbar(frame, length=380, mode='determinate',
                                        maximum=100, style="Weak.Horizontal.TProgressbar")
        self.progress.grid(row=2, column=1, columnspan=2, sticky='we', padx=(26,0), pady=(6,0))

        ttk.Label(frame, text="Suggestions:").grid(row=3, column=0, sticky='nw', pady=(12,0))
        self.suggestions = tk.Text(frame, height=8, width=70, wrap='word')
        self.suggestions.grid(row=3, column=1, columnspan=2, pady=5)

        # Breach check
        self.breach_btn = ttk.Button(frame, text="Check Breach (HIBP)", command=self.check_breach)
        self.breach_btn.grid(row=5, column=1, pady=(10, 0), sticky='w')

        self.breach_status = tk.Label(frame, text="Breach status: N/A", fg="blue")
        self.breach_status.grid(row=5, column=0, pady=(10, 0), sticky='w')

        # Show Details button (disabled initially)
        self.details_btn = ttk.Button(frame, text="Show Details",
                                      command=self.show_breach_details, state='disabled')
        self.details_btn.grid(row=5, column=2, pady=(10, 0), sticky='w')

        # Storage for last breach info
        self.last_pwned_info = None
        self.pwned_cache = {}

    # ---------------- GUI Methods ---------------- #
    def toggle_password(self):
        self.password_entry.config(show="" if self.show_var.get() else "*")

    def check_strength(self):
        password = self.password_entry.get()
        score, suggestions = check_password_strength(password)

        # Determine color and text range
        if score <= 30:
            color = "red"
            style_name = "Weak.Horizontal.TProgressbar"
            strength_text = "Weak"
        elif score <= 60:
            color = "orange"
            style_name = "Medium.Horizontal.TProgressbar"
            strength_text = "Medium"
        elif score <= 80:
            color = "blue"
            style_name = "Strong.Horizontal.TProgressbar"
            strength_text = "Strong"
        else:
            color = "green"
            style_name = "VeryStrong.Horizontal.TProgressbar"
            strength_text = "Very Strong"

        # Update label, progress and indicator
        self.strength_label.config(text=f"Strength: {score}/100 ({strength_text})", foreground=color)
        self.progress['value'] = score
        self.progress.configure(style=style_name)
        self.indicator_canvas.itemconfig(self.indicator_circle, fill=color)

        # Suggestions box
        self.suggestions.delete('1.0', tk.END)
        if suggestions:
            for s in suggestions:
                self.suggestions.insert(tk.END, f"- {s}\n")
        else:
            self.suggestions.insert(tk.END, "Password looks strong!")

    def generate_password(self):
        new_pass = generate_strong_password(14)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, new_pass)
        self.check_strength()

    def check_breach(self):
        password = self.password_entry.get().strip()
        if not password:
            messagebox.showwarning("Warning", "Enter a password first.")
            return
        self.breach_status.config(text="Checking HIBP...", fg="blue")
        threading.Thread(target=self._check_breach_background, args=(password,), daemon=True).start()

    def _check_breach_background(self, password):
        try:
            sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            # Use cached result if available
            if sha1 in self.pwned_cache:
                count, prefix, matched_suffix, matched_count = self.pwned_cache[sha1]
            else:
                count, prefix, matched_suffix, matched_count = check_pwned_api(password)
                self.pwned_cache[sha1] = (count, prefix, matched_suffix, matched_count)

            self.last_pwned_info = (sha1, count, prefix, matched_suffix, matched_count)
            # update UI on main thread
            self.root.after(0, lambda: self._update_breach_status(count))
        except Exception as e:
            print("Error checking HIBP:", e)
            self.root.after(0, lambda: self.breach_status.config(
                text="Breach status: error", fg="red"))

    def _update_breach_status(self, count):
        if count and count > 0:
            self.breach_status.config(
                text=f"Breach status: FOUND — seen {count} times", fg="red")
            # Avoid inserting duplicate breach warning lines
            existing = self.suggestions.get('1.0', tk.END)
            warning_line = f"- This password was found in breaches ({count} times). Do NOT use it.\n"
            if "This password was found in breaches" not in existing:
                self.suggestions.insert('1.0', warning_line)
            self.details_btn.config(state='normal')
        else:
            self.breach_status.config(
                text="Breach status: Not found in known breaches", fg="green")
            self.details_btn.config(state='disabled')
            self.last_pwned_info = None

    def show_breach_details(self):
        """Open popup with HIBP details."""
        info = self.last_pwned_info
        if not info:
            messagebox.showinfo("Details", "No breach details available.")
            return

        sha1_full, total_count, prefix, matched_suffix, matched_count = info
        masked_sha1 = sha1_full[:6] + "..." + sha1_full[-6:]

        txt_lines = [
            f"Full SHA-1 (masked): {masked_sha1}",
            f"Total times seen: {total_count}",
            f"Prefix sent to HIBP: {prefix}",
        ]
        if matched_suffix:
            txt_lines.append(f"Matched suffix: {matched_suffix}")
            txt_lines.append(f"Count for this suffix: {matched_count}")
        txt_lines.append("")
        txt_lines.append("Important: HIBP does NOT provide site names for password checks.")
        txt_lines.append("It only reports how many times this password hash appeared in breaches.")
        details_text = "\n".join(txt_lines)

        top = tk.Toplevel(self.root)
        top.title("HIBP Breach Details")
        top.geometry("560x320")
        tk.Label(top, text="HIBP Details", font=('Arial', 12, 'bold')).pack(pady=6)
        txt = tk.Text(top, wrap='word')
        txt.pack(fill='both', expand=True, padx=8, pady=4)
        txt.insert('1.0', details_text)
        txt.config(state='disabled')

        def copy_details():
            self.root.clipboard_clear()
            self.root.clipboard_append(details_text)
            messagebox.showinfo("Copied", "Details copied to clipboard.")

        btn_frame = ttk.Frame(top)
        btn_frame.pack(pady=6)
        ttk.Button(btn_frame, text="Copy Details", command=copy_details).pack(side='left', padx=6)
        ttk.Button(btn_frame, text="Close", command=top.destroy).pack(side='left', padx=6)


# ---------------- Main Entry ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGUI(root)
    root.mainloop()

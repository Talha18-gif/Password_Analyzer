# 🔐 Password Strength Analyzer

<div align="center">
  <h3>A professional, cross-platform Password Strength Analyzer built as both a Python Desktop App and a Static Web App.</h3>
</div>

---

## 📖 About

The **Password Entropy — Advanced Password Strength Analyzer** is a robust application designed to accurately evaluate the security of user passwords across 5 critical factors: length, character variety, entropy value, pattern detection, and breach exposure.

Unlike basic regex-based checkers, this tool uses the mathematically advanced `zxcvbn` library (the industry standard) to detect keyboard patterns and dictionary words. Additionally, it integrates securely with the **Have I Been Pwned (HIBP)** API, which indexes over 600M+ compromised passwords, to detect if a password has been exposed in known data breaches.

---

## 🚀 Features

- ✔ **Real-Time Evaluation:** Calculates strength and provides suggestions instantly as you type.
- ✔ **Accurate Entropy Check:** Uses `zxcvbn` to detect keyboard walks (e.g., "qwerty"), names, dates, and dictionary words.
- ✔ **Data Breach Detection:** Connects to the Have I Been Pwned API using k-anonymity (meaning your password is never sent over the network).
- ✔ **Custom Dictionary Attack:** Instantly flags passwords found in a local `common_passwords.txt` file.
- ✔ **Strong Password Generator:** A built-in generator that suggests cryptographically secure alternatives when the entered password is weak.

---

## 💻 Key Skills & Expertise Demonstrated

This repository highlights a comprehensive, full-stack cybersecurity skill set:

- **Python**: Used for the Desktop Application and deployment packaging.
- **CustomTkinter (GUI Design)**: Used to build a sleek, modern, Dark-Mode enabled desktop interface.
- **JavaScript, HTML, CSS**: Used to build the fast, client-side Web Application version.
- **API Integration**: Securely fetching data from external web services (HIBP).
- **Cryptography & Cybersecurity**: Understanding of true entropy (`zxcvbn`), secure hashing algorithms (SHA-1 for k-anonymity), and random secure generation.

---

## 📂 Project Structure

This project is available in two formats:

### 1. Python Desktop Version (Root Folder)
- `main.py` - The main entry point. Houses the UI and real-time update logic.
- `analyzer.py` - The core logic for evaluating password strength and generating random passwords.
- `hibp.py` - The API integration for Have I Been Pwned with built-in error handling.

### 2. Static Web App Version (`web/` Folder)
- `index.html` - The modern, glassmorphic layout.
- `style.css` - Premium styling and micro-animations.
- `app.js` - Client-side JS handling `zxcvbn`, the HIBP API fetch, and generation logic.

---

## 📥 Installation (Python Version)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Talha18-gif/Password_Analyzer.git
   cd Password_Analyzer
   ```

2. **Install the required dependencies:**
   ```bash
   pip install customtkinter zxcvbn requests
   ```

3. **Run the Application:**
   ```bash
   python main.py
   ```

---

## 🎉 Thank You! 👏

Thank you for checking out the Password Strength Analyzer! If you found this project helpful or interesting, please consider leaving a ⭐ on the repository. Feedback and contributions are always welcome!

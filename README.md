# 🔐 Password Strength Analyzer

<div align="center">
  <h3>A professional, modern Password Strength Analyzer built using Python and CustomTkinter.</h3>
</div>

---

## 📖 About

The **Password Strength Analyzer** is a robust desktop application designed to accurately evaluate the security of user passwords. Unlike basic regex-based checkers, this tool uses the mathematically advanced `zxcvbn` library (the industry standard) to detect entropy, keyboard patterns, and dictionary words. Additionally, it ensures your password hasn't been compromised in a known data breach by securely checking the Have I Been Pwned (HIBP) API.

---

## 🎯 Project Purpose

In today's digital landscape, weak passwords are the leading cause of security breaches. The purpose of this project is to provide a clean, accessible, and highly accurate tool for individuals to test their passwords locally. By giving users real-time feedback on *why* their password is weak (e.g., "this is a top-10 common password" or "this takes 3 seconds to crack"), it educates them and encourages better cybersecurity hygiene. 

---

## 🚀 Features

- ✔ **Real-Time Evaluation:** Calculates strength and provides suggestions instantly as you type.
- ✔ **Accurate Entropy Check:** Uses `zxcvbn` to detect keyboard walks (e.g., "qwerty"), names, dates, and dictionary words.
- ✔ **Data Breach Detection:** Connects to the Have I Been Pwned API using k-anonymity (meaning your password is never sent over the network).
- ✔ **Custom Dictionary Attack:** Instantly flags passwords found in a local `common_passwords.txt` file.
- ✔ **Strong Password Generator:** Generate a cryptographically secure password with a single click.

---

## 🎨 Design Tools

- **CustomTkinter:** Used to transform the standard Python GUI into a sleek, modern, and responsive interface featuring native Dark Mode support and rounded UI elements.
- **Figma / UI Principles:** Adhered to modern UX/UI principles, employing color-coded progress bars (Red/Yellow/Green) to provide instant visual feedback on password strength.

---

## 💻 Technologies Used

- **Language:** Python 3
- **GUI Framework:** CustomTkinter
- **Security Engine:** `zxcvbn` (Password strength estimator)
- **API Integration:** `requests` (Have I Been Pwned API)
- **Deployment:** PyInstaller (Compiled to standalone `.exe`)

### 📂 Project Structure

- `main.py` - The main entry point. Houses the UI and real-time update logic.
- `analyzer.py` - The core logic for evaluating password strength and generating random passwords.
- `hibp.py` - The API integration for Have I Been Pwned with built-in error handling.
- `common_passwords.txt` - A local text file containing common passwords to instantly flag.

---

## 📥 Installation

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

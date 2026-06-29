# 🔐 Password Entropy

<div align="center">
  <h3>The Ultimate, Industry-Grade Password Strength Analyzer</h3>
  <p>Available as a native Python Desktop App and a lightning-fast Static Web App.</p>
</div>

---

## 📖 About

**Password Entropy** is an advanced, industry-oriented cybersecurity application designed to definitively evaluate the security of user passwords. In an era where data breaches affect millions of users globally, simple length-based password checkers are no longer sufficient.

This tool checks passwords across 5 critical dimensions:
1. **Length**
2. **Character Variety** (Mathematical Cryptographic Entropy)
3. **Pattern Detection** (Keyboard walks, dictionary words)
4. **Crack Time Estimation**
5. **Breach Exposure** (Real-time checks against 600M+ compromised passwords)

---

## 📸 GUI Previews

> *(Note: You can add your screenshots here! Replace `screenshot.png` with your image link)*

![Desktop Application Preview](screenshot1.png)
![Web Application Preview](screenshot2.png)

---

## 🚀 Key Features

### 1. True Cryptographic Entropy (H = L × log₂(N))
Calculates the raw mathematical bit entropy based on the exact character pool utilized, proving true cryptographic strength.

### 2. Intelligent Pattern Detection
Powered by the industry-standard `zxcvbn` engine. It doesn't just look for "1 uppercase and 1 number"—it actively detects names, dates, common dictionary words, and keyboard walks (like `qwerty` or `12345`).

### 3. Have I Been Pwned (HIBP) Integration
Securely queries the global HIBP database to see if a password has been leaked in a known data breach. 
> [!IMPORTANT]
> **Zero-Knowledge Architecture**: Uses the **k-anonymity** protocol. We securely hash your password locally using SHA-1 and only send the first 5 characters of the hash over the network. Your actual password *never* leaves your device.

### 4. Custom Dictionary Attack
Instantly flags user inputs that are found in the local `common_passwords.txt` database (covering the most notoriously weak passwords).

### 5. Smart Password Generator
A built-in cryptographic generator that provides highly secure, mathematically complex alternatives with a single click (includes 1-click Copy to Clipboard).

---

## 📊 Understanding the Strength Score

The application returns a score from 0 to 4 based on real-world crack times, not arbitrary rules:
- **Score 0 (Risky):** Too guessable (e.g., "password123", "qwerty"). Crack time: Instantly.
- **Score 1 (Weak):** Very guessable. Crack time: Minutes.
- **Score 2 (Fair):** Somewhat guessable. Crack time: Days.
- **Score 3 (Strong):** Safely unguessable. Crack time: Months/Years.
- **Score 4 (Very Strong):** Highly secure. Crack time: Centuries.

---

## 💻 Tech Stack & Requirements

- **Python Desktop Version:** `Python 3`, `CustomTkinter` (Modern GUI), `zxcvbn`, `requests`.
- **Web App Version:** `Vanilla JavaScript`, `HTML5`, `CSS3` (Glassmorphism design).

---

## 📥 How to Install and Run

### Running the Python Desktop Application
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Talha18-gif/Password_Analyzer.git
   cd Password_Analyzer
   ```
2. **Install the dependencies:**
   ```bash
   pip install customtkinter zxcvbn requests
   ```
3. **Run the App:**
   ```bash
   python main.py
   ```

### Running the Web Application
Because the web app is 100% client-side (secure and serverless), you don't need to install anything!
1. Navigate to the `web/` folder.
2. Double-click `index.html` to open it in your browser.
*(You can also host this directory on GitHub Pages for free global access!)*

---

## 🎉 Thank You! 👏

Thank you for exploring Password Entropy! If this tool helps you secure your digital life, please consider leaving a ⭐ on the repository. Feedback and industry contributions are always welcome!

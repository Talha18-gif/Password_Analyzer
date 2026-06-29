document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const passwordInput = document.getElementById('password-input');
    const toggleVisibilityBtn = document.getElementById('toggle-visibility');
    const eyeIcon = document.getElementById('eye-icon');
    const strengthBar = document.getElementById('strength-bar');
    const strengthText = document.getElementById('strength-text');
    const crackTimeText = document.getElementById('crack-time');
    
    const warningBox = document.getElementById('warning-box');
    const warningText = document.getElementById('warning-text');
    const suggestionsBox = document.getElementById('suggestions-box');
    const suggestionsList = document.getElementById('suggestions-list');
    const successBox = document.getElementById('success-box');
    
    const generateBtn = document.getElementById('generate-btn');
    const checkBreachBtn = document.getElementById('check-breach-btn');
    const breachResult = document.getElementById('breach-result');

    // Colors mapping
    const strengthColors = {
        0: 'var(--color-weak)',   // Very Weak
        1: 'var(--color-weak)',   // Weak
        2: 'var(--color-fair)',   // Fair
        3: 'var(--color-good)',   // Good
        4: 'var(--color-strong)'  // Strong
    };

    const strengthLabels = {
        0: 'Very Weak',
        1: 'Weak',
        2: 'Fair',
        3: 'Strong',
        4: 'Very Strong'
    };

    // Toggle Password Visibility
    toggleVisibilityBtn.addEventListener('click', () => {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        if (type === 'text') {
            // Eye off icon
            eyeIcon.innerHTML = `<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line>`;
        } else {
            // Eye on icon
            eyeIcon.innerHTML = `<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle>`;
        }
    });

    // Evaluate Password Strength
    passwordInput.addEventListener('input', () => {
        const password = passwordInput.value;
        breachResult.classList.add('hidden'); // Hide breach result when typing

        if (!password) {
            resetUI();
            return;
        }

        // Use zxcvbn to evaluate
        const result = zxcvbn(password);
        const score = result.score; // 0 to 4
        
        // Update Meter
        strengthBar.style.width = `${(score === 0 ? 0.5 : score) * 25}%`;
        strengthBar.style.backgroundColor = strengthColors[score];
        
        // Update Text
        strengthText.textContent = `Strength: ${strengthLabels[score]}`;
        strengthText.style.color = strengthColors[score];
        crackTimeText.textContent = `Crack time: ${result.crack_times_display.offline_fast_hashing_1e10_per_second}`;

        // Feedback Logic
        updateFeedback(score, result.feedback);
    });

    function resetUI() {
        strengthBar.style.width = '0%';
        strengthText.textContent = 'Strength: N/A';
        strengthText.style.color = 'var(--text-secondary)';
        crackTimeText.textContent = '';
        warningBox.classList.add('hidden');
        suggestionsBox.classList.add('hidden');
        successBox.classList.add('hidden');
    }

    function updateFeedback(score, feedback) {
        // Reset hiding
        warningBox.classList.add('hidden');
        suggestionsBox.classList.add('hidden');
        successBox.classList.add('hidden');

        if (feedback.warning) {
            warningText.textContent = feedback.warning;
            warningBox.classList.remove('hidden');
        }

        if (feedback.suggestions && feedback.suggestions.length > 0) {
            suggestionsList.innerHTML = '';
            feedback.suggestions.forEach(sug => {
                const li = document.createElement('li');
                li.textContent = sug;
                suggestionsList.appendChild(li);
            });
            suggestionsBox.classList.remove('hidden');
        }

        if (!feedback.warning && feedback.suggestions.length === 0 && score >= 3) {
            successBox.classList.remove('hidden');
        }
    }

    // Password Generator
    generateBtn.addEventListener('click', () => {
        const length = 16;
        const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+~`|}{[]:;?><,./-=";
        let retVal = "";
        
        // Ensure at least one of each required type
        retVal += "abcdefghijklmnopqrstuvwxyz"[Math.floor(Math.random() * 26)];
        retVal += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[Math.floor(Math.random() * 26)];
        retVal += "0123456789"[Math.floor(Math.random() * 10)];
        retVal += "!@#$%^&*()_+"[Math.floor(Math.random() * 12)];

        // Fill the rest
        for (let i = 4, n = charset.length; i < length; ++i) {
            retVal += charset.charAt(Math.floor(Math.random() * n));
        }

        // Shuffle
        retVal = retVal.split('').sort(() => 0.5 - Math.random()).join('');
        
        passwordInput.value = retVal;
        
        // Trigger input event to re-evaluate
        passwordInput.dispatchEvent(new Event('input'));
        
        if (passwordInput.getAttribute('type') === 'password') {
            toggleVisibilityBtn.click(); // Show it to the user
        }
    });

    // Have I Been Pwned API Integration (k-anonymity)
    checkBreachBtn.addEventListener('click', async () => {
        const password = passwordInput.value;
        if (!password) return;

        checkBreachBtn.disabled = true;
        checkBreachBtn.textContent = 'Checking...';
        breachResult.classList.add('hidden');

        try {
            // 1. Hash password using SHA-1
            const encoder = new TextEncoder();
            const data = encoder.encode(password);
            const hashBuffer = await crypto.subtle.digest('SHA-1', data);
            
            // Convert buffer to hex string
            const hashArray = Array.from(new Uint8Array(hashBuffer));
            const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();

            // 2. K-Anonymity (Split prefix and suffix)
            const prefix = hashHex.substring(0, 5);
            const suffix = hashHex.substring(5);

            // 3. Fetch from HIBP API
            const response = await fetch(`https://api.pwnedpasswords.com/range/${prefix}`);
            if (!response.ok) throw new Error('API Error');
            
            const text = await response.text();
            const hashes = text.split('\n');
            
            let pwnedCount = 0;
            for (let i = 0; i < hashes.length; i++) {
                const [h, count] = hashes[i].split(':');
                if (h === suffix) {
                    pwnedCount = parseInt(count.trim(), 10);
                    break;
                }
            }

            // 4. Update UI
            breachResult.classList.remove('hidden', 'breach-safe', 'breach-danger');
            
            if (pwnedCount > 0) {
                breachResult.textContent = `Pwned! Found ${pwnedCount.toLocaleString()} times in data breaches.`;
                breachResult.classList.add('breach-danger');
            } else {
                breachResult.textContent = "Safe! Not found in known breaches.";
                breachResult.classList.add('breach-safe');
            }

        } catch (error) {
            console.error(error);
            breachResult.textContent = "Error connecting to breach database.";
            breachResult.classList.remove('hidden');
            breachResult.classList.add('breach-danger');
        } finally {
            checkBreachBtn.disabled = false;
            checkBreachBtn.textContent = 'Check Data Breaches (HIBP)';
        }
    });
});

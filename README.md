```markdown
# Matrix-Themed Encrypted Login (Tkinter)

A **Python** desktop application that manages **encrypted user credentials** with a **Matrix-like** animated background.  
The first user to sign up becomes **Admin**, who can then create additional (non-admin) users. On a successful login, a **secret JPEG** image is displayed in a new window.

---

## Table of Contents
1. [Features](#features)
2. [Getting Started](#getting-started)
3. [Project Structure](#project-structure)
4. [Usage](#usage)
5. [How It Works](#how-it-works)
6. [Notes on Security](#notes-on-security)
7. [Credits](#credits)

---

## Features

- **Encrypted Credentials**:  
  - Uses the [Fernet](https://cryptography.io/en/latest/fernet/) encryption scheme for secure storage in `credentials.enc`.
- **Admin Control**:  
  - The **first** signup automatically becomes **Admin**, allowing creation of additional users.
- **Matrix Background**:  
  - Continuously updating lines of green text simulate falling Matrix code.
- **Secret Image**:  
  - Shows `images.jpeg` in a new window upon successful login.
- **Tkinter GUI**:  
  - A desktop-based interface that runs on Windows, Mac, or Linux with Python 3.x.

---

## Getting Started

### Prerequisites

1. **Python 3.x**  
   Make sure Python is installed and available in your `PATH`.
2. **Install Libraries**:
   ```bash
   pip install cryptography pillow
   ```
   - [cryptography](https://pypi.org/project/cryptography/) for Fernet encryption.
   - [pillow](https://pypi.org/project/Pillow/) for JPEG image handling in Tkinter.

3. **Fernet Key**  
   - The script requires a **Fernet key** to encrypt/decrypt credentials.
   - If you haven’t generated one yet:
     ```python
     from cryptography.fernet import Fernet
     print(Fernet.generate_key())
     ```
   - Copy the printed `b'...'` string into `main.py` at `ENCRYPTION_KEY`.

### Installation

1. **Clone** or **download** this repository.
2. **Open** the folder in your terminal or command prompt.
3. **Check** that `main.py` and `images.jpeg` are in the same directory (optional: you can rename the image in the code if desired).
4. **Confirm** dependencies are installed:
   ```bash
   pip install cryptography pillow
   ```

---

## Project Structure

```
Matrix-Encrypted-Login/
├── main.py              # The main Tkinter application
├── credentials.enc      # Auto-generated, encrypted credentials file
├── images.jpeg          # The image shown upon successful login
├── key.py               # (Optional) Used to generate a Fernet key
└── README.md            # This readme file
```

- **`main.py`**: Contains all the logic for encryption, user sign-up, login, admin checks, and the Matrix background.
- **`credentials.enc`**: Created automatically after the first Sign Up (encrypted data).
- **`images.jpeg`**: Displayed upon successful login.
- **`key.py`**: An optional script to generate a Fernet key for testing.

---

## Usage

1. **Insert Your Fernet Key**  
   - In `main.py`, find:
     ```python
     ENCRYPTION_KEY = b'nek9yQUQdpinoDAlNzoYn_w-0-NcYXWEF6lzL10bBMM='
     ```
     Replace with your own key if needed (`b'...'` format).

2. **Run the App**  
   ```bash
   python main.py
   ```

3. **Sign Up / Login**  
   - The **first** user to sign up becomes **Admin** automatically.  
   - As Admin, you can create additional user accounts.  
   - Log in with valid credentials to see the **secret image** popup.

### Admin vs. Non-Admin

- **Admin** can create new users (Sign Up) after logging in.  
- **Non-Admin** users can only log in; they cannot create other accounts.

---

## How It Works

1. **Encryption**:  
   - Credentials are stored in a dictionary, serialized to JSON, then **encrypted** with Fernet into `credentials.enc`.
   - On startup or sign up, the code calls `load_credentials()` or `save_credentials()` to read/write that file.

2. **First User is Admin**:  
   - If `credentials.enc` is empty or missing, the first `Sign Up` call sets `is_admin = True`.

3. **Matrix Animation**:  
   - A `Canvas` with multiple text lines randomly updates with letters/digits to mimic falling code.

4. **Image on Login**:  
   - On successful login, a new `Toplevel` window shows `images.jpeg` (using `PIL`).

---

## Notes on Security

- **Hardcoded Key**:  
  - Storing your Fernet key in `main.py` is convenient for testing but not recommended for production. You could store it in an environment variable or a separate config file not committed to version control.
- **No Password Hashing**:  
  - Currently, the passwords are stored “as is” in encrypted form. For stronger security, you’d combine **password hashing** (bcrypt, Argon2, etc.) with encryption.

---

## Credits

- **Author**: Vijaysingh Puwar
- **Libraries**:  
  - [cryptography](https://pypi.org/project/cryptography/)  
  - [Pillow](https://pypi.org/project/Pillow/)  
- **Inspiration**:  
  - Tkinter docs, online Matrix examples, Python tutorials.

Feel free to **star** this repository if you found it useful, and open any **issues** or **pull requests** for improvements or feature requests!

---
```

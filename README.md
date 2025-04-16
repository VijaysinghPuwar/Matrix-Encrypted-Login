# Matrix-Themed Encrypted Login (Tkinter)

A **Python** desktop application that manages **encrypted user credentials** with a **Matrix-like** animated background.  
The first user to sign up becomes **Admin**, who can then create additional (non-admin) users. On a successful login, a **secret JPEG** image is displayed in a new window.

---

## Table of Contents
1. [Features](#features)
2. [Getting Started](#getting-started)
3. [Project Structure](#project-structure)
4. [Usage](#usage)
5. [Admin & Credentials Reset](#admin--credentials-reset)
6. [How It Works](#how-it-works)
7. [Notes on Security](#notes-on-security)
8. [Credits](#credits)

---

## Features

- **Encrypted Credentials**  
  Stores multiple users with passwords in `credentials.enc`, protected via [Fernet](https://cryptography.io/en/latest/fernet/).
- **Admin Control**  
  The first user to sign up is **Admin**. Admin can create additional user accounts.
- **Matrix Background**  
  Continuously updating lines of green text, simulating Matrix code.
- **Secret Image**  
  Displays `images.jpeg` upon successful login.
- **Tkinter GUI**  
  Cross-platform desktop interface in Python 3.x.

---

## Getting Started

### Prerequisites

1. **Python 3.x**  
2. **Pip Install**:
   ```bash
   pip install cryptography pillow
   ```
   - [cryptography](https://pypi.org/project/cryptography/) for encryption
   - [pillow](https://pypi.org/project/Pillow/) for JPEG image handling

3. **Fernet Key**  
   - Required to encrypt/decrypt the credentials file.
   - Generate one if you don’t have it:
     ```python
     from cryptography.fernet import Fernet
     print(Fernet.generate_key())
     ```
   - Paste the output (e.g. `b'abc123...'`) into `ENCRYPTION_KEY` in `main.py`.

---

## Project Structure

```
Matrix-Encrypted-Login/
├── main.py              # Main Tkinter application
├── images.jpeg          # Secret image displayed after login
├── credentials.enc      # Auto-generated encrypted credentials file
├── key.py               # (Optional) Used to generate a Fernet key
└── README.md            # This readme file
```

- **`main.py`**: Contains logic for sign-up, login, admin checks, encryption, matrix background.
- **`credentials.enc`**: Encrypted credentials. If deleted or emptied, the next Sign Up becomes Admin again.
- **`images.jpeg`**: The image shown upon successful login.
- **`key.py`**: Optional script to generate a new Fernet key.

---

## Usage

1. **Insert Your Fernet Key**  
   In `main.py`:
   ```python
   ENCRYPTION_KEY = b'nek9yQUQdpinoDAlNzoYn_w-0-NcYXWEF6lzL10bBMM='
   ```
   Replace with your own key if necessary.

2. **Run the App**
   ```bash
   python main.py
   ```
3. **Sign Up & Login**
   - The **first** Sign Up becomes **Admin**.
   - As Admin, create more users.  
   - Logging in successfully displays `images.jpeg` in a new window.

---

## Admin & Credentials Reset

- By default, the **first** user to sign up has **Admin** privileges.  
- If you want to **reset** the system (e.g., forget all existing users), **delete or empty** the `credentials.enc` file.  
  - The **next** Sign Up after that becomes the new Admin.  
- You can also manually log in as the existing Admin to create additional users.

---

## How It Works

1. **Encryption**  
   - User credentials are serialized to JSON, then encrypted with **Fernet** into `credentials.enc`.
2. **Admin vs. Non-Admin**  
   - If `credentials.enc` is empty, the first Sign Up user becomes Admin.  
   - Only Admin can create new users thereafter.
3. **Matrix Animation**  
   - A `Canvas` with lines of random characters updates every 100ms for the Matrix feel.
4. **Secret Image**  
   - On successful login, a `Toplevel` window displays `images.jpeg`.

---

## Notes on Security

- **Hardcoded Fernet Key**  
  - Convenient for testing but insecure for production use; consider using environment variables or a secret manager.
- **Plaintext Passwords (in encrypted form)**  
  - Real-world apps typically **hash** passwords (bcrypt, Argon2, etc.) before encrypting.

---

## Credits

- **Author**: [Your Name / GitHub Link]
- **Libraries**:  
  - [cryptography](https://pypi.org/project/cryptography/) for encryption  
  - [Pillow](https://pypi.org/project/Pillow/) for image support  
- **Inspiration**:  
  - Various Matrix-themed Python projects and Tkinter docs

Feel free to **star** this repo if you find it useful, or open **issues** for questions or suggestions!
```

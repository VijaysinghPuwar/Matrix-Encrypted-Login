import tkinter as tk
from tkinter import messagebox
import random
import string
import os
import json

# Pillow for JPEG images
from PIL import Image, ImageTk

# Cryptography for encryption
from cryptography.fernet import Fernet

# -------------------------------------------------------------------------
# 1. GLOBAL CONFIGURATION
# -------------------------------------------------------------------------
ENCRYPTED_FILE = "credentials.enc"  # Encrypted credentials file
IMAGE_FILENAME = "images.jpeg"       # Image to show after login

# Replace with your generated Fernet key (44 chars, e.g. b'xxxxx=')
ENCRYPTION_KEY = b'nek9yQUQdpinoDAlNzoYn_w-0-NcYXWEF6lzL10bBMM='

# We store the "currently logged in user" and "is_admin" state in these variables
CURRENT_USER = None
IS_ADMIN = False

# -------------------------------------------------------------------------
# 2. ENCRYPTION/DECRYPTION UTILITIES
# -------------------------------------------------------------------------
def encrypt_data(plaintext: bytes) -> bytes:
    """Encrypt raw bytes using the global Fernet key."""
    f = Fernet(ENCRYPTION_KEY)
    return f.encrypt(plaintext)

def decrypt_data(ciphertext: bytes) -> bytes:
    """Decrypt bytes using the global Fernet key."""
    f = Fernet(ENCRYPTION_KEY)
    return f.decrypt(ciphertext)

# -------------------------------------------------------------------------
# 3. LOAD/SAVE CREDENTIALS (STORING is_admin)
# -------------------------------------------------------------------------
"""
We store credentials in this format (dict):
{
  "username1": { "password": "pass1", "is_admin": true },
  "username2": { "password": "pass2", "is_admin": false },
  ...
}
"""

def load_credentials() -> dict:
    """Return the credentials dict from the encrypted file, or empty if none."""
    if not os.path.exists(ENCRYPTED_FILE):
        return {}

    try:
        with open(ENCRYPTED_FILE, "rb") as f:
            encrypted_content = f.read()
        decrypted_content = decrypt_data(encrypted_content)
        data = json.loads(decrypted_content.decode("utf-8"))
        if isinstance(data, dict):
            return data
        return {}
    except Exception:
        # Could be FileNotFoundError, Decryption error, JSON decode error, etc.
        return {}

def save_credentials(creds: dict):
    """Encrypt and save the credentials dict to ENCRYPTED_FILE."""
    data_bytes = json.dumps(creds).encode("utf-8")
    encrypted = encrypt_data(data_bytes)
    with open(ENCRYPTED_FILE, "wb") as f:
        f.write(encrypted)

# -------------------------------------------------------------------------
# 4. MATRIX BACKGROUND
# -------------------------------------------------------------------------
def generate_matrix_line() -> str:
    """Generate one line of random characters (letters/digits)."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=80))

def update_matrix():
    """Refresh matrix lines every 100ms for the "falling code" effect."""
    for text_item in matrix_items:
        line = generate_matrix_line()
        canvas.itemconfig(text_item, text=line)
    root.after(100, update_matrix)

# -------------------------------------------------------------------------
# 5. SIGN UP
# -------------------------------------------------------------------------
def signup():
    """
    1) If no users exist, this first sign-up becomes Admin.
    2) Otherwise, only the logged-in Admin can create new accounts.
    """
    global CURRENT_USER, IS_ADMIN

    username = entry_user.get().strip()
    password = entry_pass.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty.")
        return

    creds = load_credentials()

    # Check if it's the first user sign-up (no existing accounts)
    if len(creds) == 0:
        # First account => becomes Admin
        creds[username] = {"password": password, "is_admin": True}
        save_credentials(creds)
        messagebox.showinfo("Success", f"Admin account created for {username}!")
        status_label.config(text="Admin Sign Up Complete")
    else:
        # Not the first user => must be logged in as Admin
        if not IS_ADMIN:
            messagebox.showerror("Access Denied", "Only Admin can create new users. Please log in as Admin.")
            status_label.config(text="Sign Up Failed: Not Admin")
            return

        # If admin is logged in, create a regular account
        if username in creds:
            messagebox.showwarning("Account Exists", "Username already taken. Choose another.")
            status_label.config(text="Sign Up Failed: Account Exists")
        else:
            # Create a non-admin user
            creds[username] = {"password": password, "is_admin": False}
            save_credentials(creds)
            messagebox.showinfo("Success", f"New user '{username}' created!")
            status_label.config(text="New User Sign Up Complete")

# -------------------------------------------------------------------------
# 6. LOGIN
# -------------------------------------------------------------------------
def login():
    """
    1) Checks if the entered credentials match an existing user.
    2) Sets CURRENT_USER and IS_ADMIN accordingly.
    3) Shows image on success.
    """
    global CURRENT_USER, IS_ADMIN

    username = entry_user.get().strip()
    password = entry_pass.get().strip()

    creds = load_credentials()

    if username in creds and creds[username]["password"] == password:
        # Successful login
        CURRENT_USER = username
        IS_ADMIN = creds[username]["is_admin"]

        messagebox.showinfo("Login Success", f"Welcome, {username}!")
        status_label.config(text="Login Successful")
        show_image()
    else:
        # Failed login
        CURRENT_USER = None
        IS_ADMIN = False
        messagebox.showerror("Login Failed", "Incorrect username or password.")
        status_label.config(text="Login Failed")

# -------------------------------------------------------------------------
# 7. SHOW IMAGE AFTER LOGIN
# -------------------------------------------------------------------------
def show_image():
    """Open a new window displaying the JPEG image."""
    new_window = tk.Toplevel(root)
    new_window.title("Secret Image")
    new_window.configure(bg="black")

    if not os.path.exists(IMAGE_FILENAME):
        messagebox.showerror("File Not Found", f"Could not find '{IMAGE_FILENAME}'.")
        return

    try:
        img = Image.open(IMAGE_FILENAME)
    except Exception as e:
        messagebox.showerror("Image Error", str(e))
        return

    img_tk = ImageTk.PhotoImage(img)
    label_img = tk.Label(new_window, image=img_tk, bg="black")
    label_img.image = img_tk  # Keep a reference to avoid garbage collection
    label_img.pack(padx=20, pady=20)

# -------------------------------------------------------------------------
# 8. TKINTER SETUP
# -------------------------------------------------------------------------
root = tk.Tk()
root.title("Matrix-Themed Login (Encrypted) - Admin/Users")
root.geometry("800x600")
root.configure(bg="black")

# Canvas for Matrix background
canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.place(x=0, y=0, relwidth=1, relheight=1)

matrix_items = []
font_size = 14
line_height = font_size + 4
num_lines = int(root.winfo_screenheight() / line_height)

for i in range(num_lines):
    text_item = canvas.create_text(
        10, i * line_height,
        anchor="nw",
        text=generate_matrix_line(),
        font=("Courier", font_size),
        fill="#00FF00"
    )
    matrix_items.append(text_item)

update_matrix()

# UI Frame
ui_frame = tk.Frame(root, bg="black")
ui_frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(ui_frame, text="Username:", bg="black", fg="white").pack(pady=(10, 0))
entry_user = tk.Entry(ui_frame)
entry_user.pack()

tk.Label(ui_frame, text="Password:", bg="black", fg="white").pack(pady=(10, 0))
entry_pass = tk.Entry(ui_frame, show="*")
entry_pass.pack()

tk.Button(ui_frame, text="Sign Up", command=signup, bg="black", fg="#00FF00", activebackground="green").pack(pady=5)
tk.Button(ui_frame, text="Login", command=login, bg="black", fg="#00FF00", activebackground="green").pack(pady=5)

status_label = tk.Label(ui_frame, text="", bg="black", fg="white", font=("Arial", 14))
status_label.pack(pady=10)

root.mainloop()

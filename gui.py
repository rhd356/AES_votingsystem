import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from matcher import compare_fingerprints
from encryption import (
    encrypt_image_aes, decrypt_image_aes,
    encrypt_text_aes, decrypt_text_aes,
    key
)
from voter import Voter, voter_records, save_to_csv, load_from_csv

def get_fingerprint_file():
    file_path = filedialog.askopenfilename(
        title="Select a fingerprint image",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg *.bmp *.tif"),
            ("All Files", "*.*")
        ]
    )
    return file_path

def registration_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("Voter Registration")
    dialog.geometry("500x300")

    tk.Label(dialog, text="Enter full name:", font=("Arial", 12)).pack(pady=(15, 0))
    entry_name = tk.Entry(dialog, width=50, font=("Arial", 12))
    entry_name.pack(pady=5)

    tk.Label(dialog, text="Enter address:", font=("Arial", 12)).pack(pady=(15, 0))
    entry_address = tk.Entry(dialog, width=50, font=("Arial", 12))
    entry_address.pack(pady=5)

    tk.Label(dialog, text="Enter SSN (format: XXX-XX-XXXX):", font=("Arial", 12)).pack(pady=(15, 0))
    entry_ssn = tk.Entry(dialog, width=50, font=("Arial", 12))
    entry_ssn.pack(pady=5)

    def submit():
        name = entry_name.get()
        address = entry_address.get()
        ssn = entry_ssn.get()
        if not name or not address:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        if len(ssn) != 11 or ssn.count('-') != 2:
            messagebox.showerror("Error", "SSN must be in the format XXX-XX-XXXX.")
            return
        dialog.destroy()
        register_voter_with_data(name, address, ssn)

    tk.Button(dialog, text="Submit", font=("Arial", 12), command=submit).pack(pady=20)

def register_voter_with_data(name, address, ssn):                           # Encrypt and store the voter record
    fingerprint_path = get_fingerprint_file()                               # Ask user to select fingerprint image
    if not fingerprint_path:                                                # If no image selected
        messagebox.showerror("Error", "No fingerprint image selected!")     
        return

    # Encrypt voter data and fingerprint image
    encrypted_name = encrypt_text_aes(name, key)
    encrypted_address = encrypt_text_aes(address, key)
    encrypted_ssn = encrypt_text_aes(ssn, key)
    encrypted_fp = encrypt_image_aes(fingerprint_path, key)

    # Create Voter object and save it
    voter = Voter(encrypted_name, encrypted_address, encrypted_ssn, encrypted_fp)
    voter_records.append(voter)  # Add to voter list
    messagebox.showinfo("Success", f"Voter {name} registered successfully!")  # Success message

def verify_fingerprint():  # Delay verification slightly to allow GUI to update
    root.after(200, run_verification_dialog)

def run_verification_dialog():                                      # Opens a file and checks for matching fingerprint
    fingerprint_path = get_fingerprint_file()                       # Let user pick fingerprint image
    if not fingerprint_path:
        messagebox.showerror("Error", "No fingerprint image selected!") 
        return

    input_img = cv2.imread(fingerprint_path, cv2.IMREAD_COLOR)  # Load selected image
    best_match = None                                           # Initialize best match
    best_score = float('inf')                                   # Initialize best score (lower is better)

    for voter in voter_records:                                                 # Loop over all registered voters
        decrypted_img = decrypt_image_aes(voter.encrypted_fingerprint, key)     # Decrypt their fingerprint
        score = compare_fingerprints(input_img, decrypted_img)                  # Compare with input
        if score < best_score:                                                  # If it's the best match so far
            best_score = score
            best_match = voter

    threshold = 1 / 20                                                          # Similarity threshold
    if best_match and best_score < threshold:          
        voter_info = best_match.decrypt_info(key)      
        messagebox.showinfo("Match Found", f"Match: {voter_info['name']}, {voter_info['address']}, {voter_info['ssn']}")  # Show match
    else:
        messagebox.showerror("No Match", "No matching voter found.")               # Show error if no match

def setup_gui():
    global root
    root = tk.Tk()
    root.withdraw()

    load_from_csv()  # Load existing voter records from CSV and .bin image file

    main_window = tk.Toplevel(root)
    main_window.title("Fingerprint Voter System")
    main_window.geometry("400x300")

    tk.Label(main_window, text="Fingerprint Voter System", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Button(main_window, text="Register Voter", font=("Arial", 12), command=lambda: root.after(200, registration_dialog)).pack(pady=10)
    tk.Button(main_window, text="Verify Fingerprint", font=("Arial", 12), command=verify_fingerprint).pack(pady=10)
    tk.Button(main_window, text="Save", font=("Arial", 12), command=save_to_csv).pack(pady=10)
    tk.Button(main_window, text="Exit", font=("Arial", 12), command=lambda: (save_to_csv(), root.quit())).pack(pady=10)

    root.mainloop()
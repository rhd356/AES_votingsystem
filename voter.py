from encryption import decrypt_text_aes
import base64
import csv

class Voter:
    def __init__(self, encrypted_name, encrypted_address, encrypted_ssn, encrypted_fingerprint):
        self.encrypted_name = encrypted_name  # Encrypted bytes
        self.encrypted_address = encrypted_address  # Encrypted bytes
        self.encrypted_ssn = encrypted_ssn  # Encrypted bytes
        self.encrypted_fingerprint = encrypted_fingerprint  # Encrypted binary image bytes

    def decrypt_info(self, key):
        return {
            "name": decrypt_text_aes(self.encrypted_name, key),
            "address": decrypt_text_aes(self.encrypted_address, key),
            "ssn": decrypt_text_aes(self.encrypted_ssn, key)
        }

voter_records = []  # List to hold all voter objects in memory

def save_to_csv(filename="voters.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["encrypted_name", "encrypted_address", "encrypted_ssn", "fingerprint_path"])
        for i, voter in enumerate(voter_records):
            fp_filename = f"fingerprint_{i:03}.bin"
            with open(fp_filename, "wb") as fp_file:
                fp_file.write(voter.encrypted_fingerprint)
            writer.writerow([
                base64.b64encode(voter.encrypted_name).decode('utf-8'),
                base64.b64encode(voter.encrypted_address).decode('utf-8'),
                base64.b64encode(voter.encrypted_ssn).decode('utf-8'),
                fp_filename
            ])

def load_from_csv(filename="voters.csv"):
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                encrypted_name = base64.b64decode(row['encrypted_name'])
                encrypted_address = base64.b64decode(row['encrypted_address'])
                encrypted_ssn = base64.b64decode(row['encrypted_ssn'])
                with open(row['fingerprint_path'], "rb") as fp_file:
                    encrypted_fp = fp_file.read()
                voter = Voter(encrypted_name, encrypted_address, encrypted_ssn, encrypted_fp)
                voter_records.append(voter)
    except FileNotFoundError:
        print("No existing voter file found. Starting fresh.")

from encryption import decrypt_text_aes

class Voter:
    def __init__(self, encrypted_name, encrypted_address, encrypted_ssn, encrypted_fingerprint):
        self.encrypted_name = encrypted_name
        self.encrypted_address = encrypted_address
        self.encrypted_ssn = encrypted_ssn
        self.encrypted_fingerprint = encrypted_fingerprint

    def decrypt_info(self, key):
        return {
            "name": decrypt_text_aes(self.encrypted_name, key),
            "address": decrypt_text_aes(self.encrypted_address, key),
            "ssn": decrypt_text_aes(self.encrypted_ssn, key)
        }

voter_records = []
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import csv


def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ct


def aes_decrypt(iv, ct, key):
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
    return decrypted


def rsa_encrypt(data, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher.encrypt(data.encode())
    return base64.b64encode(encrypted_data).decode('utf-8')


def rsa_decrypt(encrypted_data, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_data = cipher.decrypt(base64.b64decode(encrypted_data))
    return decrypted_data.decode('utf-8')


def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def process_and_encrypt_csv(input_csv_filename, output_csv_filename, encryption_method="AES"):
    with open(input_csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    headers = rows[0]
    data_rows = rows[1:]

    if encryption_method == "RSA":
        private_key, public_key = generate_rsa_keys()
        public_key_obj = RSA.import_key(public_key)
        private_key_obj = RSA.import_key(private_key)

    aes_key = get_random_bytes(16)

    with open(output_csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(headers + ['Encrypted Data', 'Encryption Method'])

        for row in data_rows:
            data_to_encrypt = ','.join(row)

            if encryption_method == "AES":
                iv, encrypted_data = aes_encrypt(data_to_encrypt, aes_key)
                writer.writerow(row + [f"{iv},{encrypted_data}", "AES"])
                print(f"AES Encryption applied for row: {row}")

            elif encryption_method == "RSA":
                encrypted_data_rsa = rsa_encrypt(data_to_encrypt, public_key_obj)
                writer.writerow(row + [encrypted_data_rsa, "RSA"])
                print(f"RSA Encryption applied for row: {row}")

            else:
                print("Unsupported encryption method!")

    print(f"Encrypted data saved to {output_csv_filename}")


input_csv_filename = "latest_news.csv"
output_csv_filename = "encrypted_news_data_aes.csv"
process_and_encrypt_csv(input_csv_filename, output_csv_filename, encryption_method="AES")

output_csv_filename = "encrypted_news_data_rsa.csv"
process_and_encrypt_csv(input_csv_filename, output_csv_filename, encryption_method="RSA")

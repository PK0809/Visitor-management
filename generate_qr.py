import qrcode
import os

# URL to open when QR is scanned
registration_url = "https://visitor-management-eqd9.onrender.com/register"

# Folder to save QR code
qr_folder = os.path.join('static', 'qr_codes')
os.makedirs(qr_folder, exist_ok=True)

# Generate QR code image
img = qrcode.make(registration_url)

# Save QR code
img_path = os.path.join(qr_folder, "visitor_registration.png")
img.save(img_path)

print(f"QR code saved at {img_path}")


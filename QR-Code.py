# A QR code (Quick Response code) is a type of two-dimensional barcode that stores information in a pattern of # black and white squares, which can be quickly read by a smartphone camera. Unlike standard barcodes, QR
# codes can store large amounts of data, such as website URLs, text, contact information, or Wi-Fi details, 
# and can even be read in two directions, making them very efficient. They serve as a digital bridge,
# providing a fast and convenient way for users to access online information or perform actions from the
# physical world, such as visiting a website, making a payment, or getting more details about a product

import qrcode

# The web page you want to open when scanning
url = "https://laptop-price-prediction-11.streamlit.app/"

# Generate QR code
qr = qrcode.QRCode(
    version=1,  # auto adjust size if None
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

qr.add_data(url)
qr.make(fit=True)

# Create QR image
img = qr.make_image(fill_color="black", back_color="white")

# Save the QR code as an image file
img.save("laptop-price-prediction-qr.png")

print("QR Code saved as laptop-price-prediction-qr.png")

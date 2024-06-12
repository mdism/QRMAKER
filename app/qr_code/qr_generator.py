import qrcode
from PIL import Image
from io import BytesIO

def generate_qr(data, logo_path=None, color="black"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=5,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=color, back_color="white")

    if logo_path:
        logo = Image.open(logo_path)
        basewidth = 100
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)

        pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
        img.paste(logo, pos, mask=logo)

    byte_arr = BytesIO()
    img.save(byte_arr, format='PNG')
    return byte_arr.getvalue()

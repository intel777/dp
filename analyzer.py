import os
import io

import cv2
from matplotlib import pyplot as plt
from PIL import Image, ImageCms
from PIL.ExifTags import TAGS

mode_to_bpp = {'1': 1, 'L': 8, 'P': 8, 'RGB': 24, 'RGBA': 32, 'CMYK': 32, 'YCbCr': 24, 'I': 32, 'F': 32}


def analyze_and_respond(image_path, update):
    print(f'[analyzer]Analyzing image: {image_path}')
    file_size = os.path.getsize(image_path)
    image = Image.open(image_path)
    image_format = image.format
    width, height = image.size
    color_model = image.mode
    bit_depth = mode_to_bpp[color_model]
    icc = image.info.get('icc_profile')
    if icc:
        f = io.BytesIO(icc)
        image_profile = ImageCms.ImageCmsProfile(f).profile.profile_description
    exif_data = image.getexif()

    reply = '====[Basic information]====\n'
    reply += f'File size: {file_size} bytes\n'
    reply += f'Format: {image_format}\n'
    reply += f'Resolution: {width}x{height}\n'
    reply += f'Bit depth: {bit_depth}\n'
    reply += f'Color model: {color_model}\n'
    if icc:
        reply += f'Profile: {image_profile}\n'

    if exif_data:
        reply += '\n====[EXIF information]====\n'
        for tag_id in exif_data:
            tag = TAGS.get(tag_id, tag_id)
            data = exif_data.get(tag_id)
            if isinstance(data, bytes):
                data = data.decode(errors='replace')
            reply += f'{tag}: {data}\n'

    # Generating histogram
    img = cv2.imread(image_path)
    plt.switch_backend('agg')
    for i, col in enumerate(('b', 'g', 'r')):
        hist = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(hist, color=col)
    plt.xlim([0, 256])
    hist_path = image_path + '_hist.png'
    plt.savefig(hist_path)

    update.message.reply_text(reply)
    update.message.reply_photo(open(hist_path, 'rb'))
    os.remove(hist_path)

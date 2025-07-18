import hashlib
import html
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np
import pytesseract
from django.conf import settings
from django.core.files.base import ContentFile
from google.cloud import translate_v2 as translate
from PIL import Image, ImageDraw, ImageFont
from pytesseract import Output

from .models import TranslatedImage

translate_client = None
initialization_error = None

try:
    translate_client = translate.Client.from_service_account_json(settings.GOOGLE_APPLICATION_CREDENTIALS)
except Exception as e:
    initialization_error = e
    print(f"CRITICAL: Помилка ініціалізації Google Cloud Translate API: {initialization_error}")

pytesseract.pytesseract.tesseract_cmd = str(settings.TESSERACT_CMD)


def process_image_translation(image_file, target_language="en", user=None):
    if initialization_error:
        raise Exception(f"Помилка конфігурації Google Translate API: {initialization_error}")

    if not translate_client:
        raise Exception("Клієнт Google Translate не ініціалізований. Перевірте ключ API.")

    if not user:
        raise ValueError("Для обробки перекладу необхідно надати користувача.")

    image_file.seek(0)
    image_bytes = image_file.read()
    image_hash = hashlib.sha256(image_bytes).hexdigest()

    existing_record = TranslatedImage.objects.filter(
        user=user, image_hash=image_hash, target_language=target_language
    ).first()

    if existing_record:
        return existing_record

    file_bytes_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(file_bytes_array, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"Не вдалося декодувати зображення: {image_file.name}.")

    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    data = pytesseract.image_to_data(img, lang="eng+rus", output_type=Output.DICT)
    lines = defaultdict(list)
    for i in range(len(data["text"])):
        if int(data["conf"][i]) > 30:
            line_key = (data["block_num"][i], data["par_num"][i], data["line_num"][i])
            lines[line_key].append(
                {
                    "text": data["text"][i],
                    "left": data["left"][i],
                    "top": data["top"][i],
                    "width": data["width"][i],
                    "height": data["height"][i],
                }
            )

    original_text_lines = [
        " ".join(word["text"] for word in lines[line_key]).strip()
        for line_key in sorted(lines.keys())
        if lines[line_key]
    ]
    full_original_text = "\n".join(filter(None, original_text_lines))

    source_language = "und"
    if full_original_text.strip():
        try:
            detection_sample = (
                (full_original_text[:500] + "..") if len(full_original_text) > 500 else full_original_text
            )
            detection_result = translate_client.detect_language(detection_sample)
            source_language = detection_result["language"]
        except Exception as e:
            print(f"Помилка визначення мови: {e}")

    if source_language != target_language and source_language != "und":
        translated_text_lines = []
        for line in original_text_lines:
            if not line.strip():
                translated_text_lines.append(line)
                continue
            try:
                result = translate_client.translate(line, target_language=target_language)
                translated = html.unescape(result["translatedText"])
                translated_text_lines.append(translated)
            except Exception as e:
                print(f"Помилка під час перекладу для рядка '{line}': {e}")
                translated_text_lines.append(line)
    else:

        translated_text_lines = original_text_lines

    full_translated_text = "\n".join(translated_text_lines)

    for line_key, original_line in zip(sorted(lines.keys()), original_text_lines):

        translated_line = translated_text_lines[original_text_lines.index(original_line)]
        words_in_line = lines[line_key]
        x_min, y_min = min(w["left"] for w in words_in_line), min(w["top"] for w in words_in_line)
        x_max = max(w["left"] + w["width"] for w in words_in_line)
        y_max = max(w["top"] + w["height"] for w in words_in_line)
        w_line, h_line = x_max - x_min, y_max - y_min
        if w_line <= 0 or h_line <= 0:
            continue

        font_size = h_line if h_line > 5 else 10
        font = ImageFont.truetype(str(settings.FONT_PATH), int(font_size))
        text_bbox = draw.textbbox((0, 0), translated_line, font=font)
        while text_bbox[2] > w_line and font.size > 5:
            font = ImageFont.truetype(str(settings.FONT_PATH), font.size - 1)
            text_bbox = draw.textbbox((0, 0), translated_line, font=font)
        try:
            bg_color = img_pil.getpixel((max(0, x_min - 5), y_min + h_line // 2))
        except IndexError:
            bg_color = (18, 26, 38)
        draw.rectangle([(x_min, y_min), (x_max, y_max)], fill=bg_color)
        text_color = "white" if sum(bg_color) < 384 else "black"
        text_height = text_bbox[3] - text_bbox[1]
        y_offset = (h_line - text_height) / 2
        draw.text((x_min, y_min + y_offset), translated_line, fill=text_color, font=font)

    new_record = TranslatedImage(
        user=user,
        image_hash=image_hash,
        source_language=source_language,
        target_language=target_language,
        original_text=full_original_text,
        translated_text=full_translated_text,
    )

    original_extension = Path(image_file.name).suffix
    original_filename = f"{new_record.id}{original_extension}"
    new_record.original_image.save(original_filename, image_file, save=False)

    final_image_bgr = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    is_success, buffer = cv2.imencode(".png", final_image_bgr)
    if not is_success:
        raise Exception("Could not encode translated image.")
    new_record.translated_image.save(f"{new_record.id}_translated.png", ContentFile(buffer.tobytes()), save=False)

    new_record.original_text_file.save(
        f"{new_record.id}_original.txt",
        ContentFile(full_original_text.encode("utf-8")),
        save=False,
    )

    new_record.translated_text_file.save(
        f"{new_record.id}_translated.txt",
        ContentFile(full_translated_text.encode("utf-8")),
        save=False,
    )

    new_record.save()

    return new_record

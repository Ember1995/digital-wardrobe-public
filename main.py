# main.py

import os
import uuid
import glob
import csv
from dotenv import load_dotenv
from google import genai
from pipeline.video_utils import *
from pipeline.schema import INVENTORY_RESPONSE_SCHEMA, TYPE_TO_LAYER_MAP

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Тимчасовий приклад профілю користувача
CURRENT_USER_PROFILE = {
    "": ""
}


def get_client():
    """Ініціалізація клієнта AI-сервісу."""
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    return genai.Client(api_key=api_key)


def get_next_id(file):
    """Отримання наступного ідентифікатора запису."""
    if not os.path.exists(file):
        return 1

    with open(file, 'r', encoding='utf-8') as f:
        data = list(csv.reader(f))
        if len(data) <= 1:
            return 1
        try:
            return int(data[-1][0]) + 1
        except Exception:
            return 1


CSV_FIELDNAMES = [
    'id',
    '',
    'item_name',
    'brand',
    'type',
    'layer',
    'main_color',
    'additional_colors',
    'print',
    'material',
    'details',
    'style_category',
    'mood',
    'matched_with_weather',
    '',
    '',
    '',
    'basic_file_pic_url',
    'refined_file_pic_url',
    'studio_file_pic_url'
]


def append_item_to_csv(item_data, output_file="wardrobe.csv"):
    """Додавання запису про предмет гардероба до CSV-файлу."""
    file_exists = os.path.isfile(output_file)
    with open(output_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(item_data)


if __name__ == "__main__":
    client = get_client()
    output_db = "wardrobe.csv"

    for p in ["data/videos", "data/frames", "data/refined_frames", "data/studio_frames"]:
        os.makedirs(p, exist_ok=True)

    for path in glob.glob("data/videos/*.mp4") + glob.glob("data/videos/*.mov"):
        v_id = str(uuid.uuid4())[:8]
        print(f"\n>>> ОБРОБКА ВІДЕО: {os.path.basename(path)}")

        uploaded = upload_video(client, path)
        inv_data = analyze_video(client, uploaded, INVENTORY_RESPONSE_SCHEMA, TYPE_TO_LAYER_MAP)

        if 'items' in inv_data:
            current_id = get_next_id(output_db)

            for ai_item in inv_data['items']:
                print(f"\n  --- Елемент {current_id}: {ai_item.get('item_name', 'Unnamed item')} ---")

                # Ініціалізація запису
                row = {field: "" for field in CSV_FIELDNAMES}

                row.update({
                    'id': current_id,
                    'video_id': v_id,
                    'video_source_path': path,
                    'laundry': 'no',
                    'basic_file_pic_url': f"data/frames/item_{current_id}.jpg",
                    'refined_file_pic_url': f"data/refined_frames/item_{current_id}_refined.jpg",
                    'studio_file_pic_url': f"data/studio_frames/item_{current_id}_final.jpg"
                })

                # Заповнення базових атрибутів
                for k, v in ai_item.items():
                    if k in row:
                        row[k] = ", ".join(v) if isinstance(v, list) else v

                # Узагальнений процес обробки зображення
                if extract_best_frame(path, row['timestamp'], row['basic_file_pic_url']):
                    print("    [1/3] Кадр підготовлено")

                    ref_data = analyze_image_refinement(client, row['basic_file_pic_url'])

                    if refine_image_geometry(
                        row['basic_file_pic_url'],
                        row['refined_file_pic_url'],
                        ref_data
                    ):
                        print("    [2/3] Зображення оброблено")

                        if generate_studio_photo(
                            client,
                            row['refined_file_pic_url'],
                            row['studio_file_pic_url'],
                            CURRENT_USER_PROFILE,
                            row
                        ):
                            print("    [3/3] Фінальне зображення готове")

                # Збереження результату
                append_item_to_csv(row, output_db)
                current_id += 1

    print("\n[FINISH] Усі елементи оброблено та збережено.")
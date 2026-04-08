# pipeline/video_utils.py

import time
import cv2
import subprocess
import os
import json
import io
from PIL import Image
from google.genai import types
import shutil

from pipeline.schema import (
    INVENTORY_RESPONSE_SCHEMA,
    TYPE_TO_LAYER_MAP,
    IMAGE_REFINEMENT_RESPONSE_SCHEMA
)
from pipeline.prompts import (
    WARDROBE_ITEM_SYSTEM_INSTRUCTION,
    IMAGE_REFINEMENT_SYSTEM_INSTRUCTION,
    AI_BACKGROUND_REMOVAL_PROMPT,
    STUDIO_RETOUCH_SYSTEM_PROMPT
)


# @weave.op()
def upload_video(client, path):
    """Завантаження відео та очікування статусу ACTIVE."""
    print(f"\n[INFO] Uploading: {os.path.basename(path)}...")
    print("[INFO] Публічна версія: логіку завантаження відео приховано.")
    return None


# @weave.op()
def analyze_video(client, video_file, schema, taxonomy_map):
    """Аналіз відео для подальшого структурованого запису в БД."""
    print("[INFO] Analyzing with Gemini 3 Flash Preview...")
    print("[INFO] Публічна версія: логіку аналізу відео приховано.")
    return {"items": []}


def extract_best_frame(video_path, timestamp_str, output_path):
    """
    Витягує кадр із відео за тайм-кодом MM:SS.mmm.
    """
    try:
        print("[INFO] Публічна версія: логіку екстракції кадру приховано.")
        return False

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] FFmpeg failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected extraction error: {e}")
        return False


def analyze_image_refinement(client, image_path):
    """Аналіз параметрів повороту та обрізки зображення."""
    print("  - AI analyzing frame geometry...")
    print("[INFO] Публічна версія: логіку аналізу кадру приховано.")
    return {
        "ai_rotation_angle": 0,
        "ai_bounding_box": [0, 0, 1000, 1000]
    }


def refine_image_geometry(image_path, output_path, ref_data):
    """Корекція геометрії зображення: поворот і обрізка."""
    try:
        print("[INFO] Публічна версія: логіку корекції геометрії приховано.")

        if os.path.exists(image_path):
            shutil.copy(image_path, output_path)
            return True

        return False
    except Exception:
        return False


def generate_studio_photo(client, input_image_path, output_path, user_profile, item_data=None):
    """
    Об’єднаний пайплайн генерації фінального студійного зображення.
    """
    print("    [AI Pipeline] Running full process...")
    print("[INFO] Публічна версія: логіку видалення фону та генерації зображення приховано.")

    try:
        if os.path.exists(input_image_path):
            shutil.copy(input_image_path, output_path)
            return True
        return False
    except Exception as e:
        print(f"[ERROR] Full AI Pipeline failed: {e}")
        return False


def _save_image_from_response(response, output_path, fallback_path):
    """Допоміжна функція для збереження зображення з відповіді моделі."""
    print("[INFO] Публічна версія: логіку збереження зображення приховано.")

    try:
        if os.path.exists(fallback_path):
            shutil.copy(fallback_path, output_path)
            return True
        return False
    except Exception:
        return False
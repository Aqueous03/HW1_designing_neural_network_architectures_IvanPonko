import os
import shutil
import random
from pathlib import Path

# === НАСТРОЙКИ ===
SRC_IMAGES = "C:\\Users\\IVAN\\Desktop\\Study\\Mag sem2\\Computer Vision\\HW1\\obj_train_data"
DST_ROOT = "C:\\Users\\IVAN\\Desktop\\Study\\Mag sem2\\Computer Vision\\HW1\\detectin"   # готовый датасет
TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
# TEST_RATIO = 0.15 (остаток)
SEED = 42

random.seed(SEED)

# Создаём папки
for split in ("train", "val", "test"):
    (Path(DST_ROOT) / split / "images").mkdir(parents=True, exist_ok=True)
    (Path(DST_ROOT) / split / "labels").mkdir(parents=True, exist_ok=True)

# Получаем список всех изображений (ищем jpg, png, jpeg)
image_files = []
for ext in ("*.jpg", "*.png", "*.jpeg"):
    image_files.extend(Path(SRC_IMAGES).glob(ext))
image_files = sorted(image_files)

# Убедимся, что для каждого изображения есть txt
pairs = []
for img_path in image_files:
    txt_path = img_path.with_suffix(".txt")
    if txt_path.exists():
        pairs.append((img_path, txt_path))
print(f"Найдено пар: {len(pairs)}")

# Перемешиваем
random.shuffle(pairs)

# Разбиваем
train_end = int(len(pairs) * TRAIN_RATIO)
val_end = train_end + int(len(pairs) * VAL_RATIO)

splits = {
    "train": pairs[:train_end],
    "val":   pairs[train_end:val_end],
    "test":  pairs[val_end:]
}

# Копируем
for split_name, files in splits.items():
    for img_path, txt_path in files:
        shutil.copy(img_path, Path(DST_ROOT) / split_name / "images" / img_path.name)
        shutil.copy(txt_path, Path(DST_ROOT) / split_name / "labels" / txt_path.name)
    print(f"{split_name}: {len(files)} изображений")
import pytesseract
from PIL import Image
from ultralytics import YOLO
import re

def imageToString(image_path):
    image = image_path
    text = pytesseract.image_to_string(Image.open(image), lang="tur")
    pattern = re.compile(r'ÜNİVERSİTESİ\n\n(.*?)\n\n', re.DOTALL)
    patternSN = re.compile(r'Öğrenci No:(.*?)\n', re.DOTALL)
    matches = pattern.search(text)
    matchesSN = patternSN.search(text)
    student_number = matchesSN.group(1).strip()
    if matches:
        next_line = matches.group(1)
        if "." in next_line:
            next_line = next_line.replace(".", "")
    else:
        print("There is no any match up!")

    return next_line, student_number

def translateEnglishToTurkish(text):
    
    turkce_ingilizce = {
        "ç": "c",
        "ğ": "g",
        "ı": "i",
        "ö": "o",
        "ş": "s",
        "ü": "u",
        "Ç": "C",
        "Ğ": "G",
        "İ": "I",
        "Ö": "O",
        "Ş": "S",
        "Ü": "U"
    }
    
    for turkce, ingilizce in turkce_ingilizce.items():
        text = text.replace(turkce, ingilizce)
    
    return text


def cleanString(text):
    
    clean_text = ''
    
    
    for char in text:
        
        if char.isprintable():
            clean_text += char
        else:
            print("rrrr",char)
    
    return clean_text


def aiModel(model, image, name):
    model_path = model
    detected_objects = []
    model = YOLO(model_path, "v8")
    results = model.predict(image, conf=0.5, save=True, save_crop=True, save_dir="fp", project=f"uploads/profile_pics/{name}")
    for result in results:
        for box in result.boxes:
            class_id = result.names[box.cls[0].item()]
            detected_objects.append(class_id)
    if ("card" in detected_objects) and ("face" in detected_objects):
        return True
    else:
        return False
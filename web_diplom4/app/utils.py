import os
import uuid
from werkzeug.utils import secure_filename

# Разрешённые расширения для текстовых файлов
ALLOWED_EXTENSIONS = {'docx', 'doc', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file_old(file):
    if not file or not allowed_file(file.filename):
        raise ValueError('Недопустимый тип файла. Разрешены: ' + ', '.join(ALLOWED_EXTENSIONS))
    
    original_filename = file.filename
    
    # Разделяем на имя и расширение
    name_part, ext_part = os.path.splitext(original_filename)
    
    # Безопасное имя (только имя, без расширения)
    safe_name = secure_filename(name_part) if name_part else 'file'
    
    # Безопасное расширение: обрабатываем расширение отдельно, но гарантируем точку
    if ext_part:
        # Убираем не-ASCII символы, но сохраняем точку
        safe_ext = secure_filename(ext_part)
        # Если точка исчезла, добавляем её принудительно
        if not safe_ext.startswith('.'):
            safe_ext = '.' + safe_ext
    else:
        safe_ext = ''
    
    # Собираем уникальное имя: uuid + безопасное имя + расширение
    unique_name = f"{uuid.uuid4().hex}_{safe_name}{safe_ext}"
    
    # Папка для загрузок
    upload_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, unique_name)
    file.save(file_path)
    
    return unique_name, original_filename

def save_uploaded_file(file):
    if not file or not allowed_file(file.filename):
        raise ValueError('Недопустимый тип файла. Разрешены: ' + ', '.join(ALLOWED_EXTENSIONS))
    
    original_filename = file.filename
    
    # Разделяем на имя и расширение
    name_part, ext_part = os.path.splitext(original_filename)
    
    # Безопасное имя (только имя, без расширения)
    safe_name = secure_filename(name_part) if name_part else 'file'
    
    # Безопасное расширение: обрабатываем расширение отдельно, но гарантируем точку
    # if ext_part:
    #     # Убираем не-ASCII символы, но сохраняем точку
    #     safe_ext = secure_filename(ext_part)
    #     # Если точка исчезла, добавляем её принудительно
    #     if not safe_ext.startswith('.'):
    #         safe_ext = '.' + safe_ext
    # else:
    #     safe_ext = ''
    
    safe_ext = '.' + ext_part

    # Собираем уникальное имя: uuid + безопасное имя + расширение
    # unique_name = f"{uuid.uuid4().hex}_{safe_name}{safe_ext}"
    unique_name = f"{'document'}{safe_ext}"
    
    # Папка для загрузок
    upload_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, unique_name)
    file.save(file_path)
    
    return unique_name, original_filename

def delete_uploaded_file(filename):
    """
    Удаляет файл из папки uploads, если он существует.
    filename — имя файла (без пути).
    Возвращает True, если файл удалён, False — если не найден.
    """
    upload_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))
    file_path = os.path.abspath(os.path.join(upload_dir, filename))
    
    # Защита: файл должен быть внутри папки uploads
    if not file_path.startswith(upload_dir):
        raise ValueError("Некорректное имя файла")
    
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

from flask import request, jsonify, render_template, send_from_directory
import os
from app.utils import save_uploaded_file, delete_uploaded_file
from pathlib import Path

from src.report_and_list_handler import ReportAndListHandler

def home():
    return render_template('index.html')

def get_list_rules():
     
    #  rule_id: str
    # section: str
    # description: str
    # severity: str  # CRITICAL | RECOMMENDATION
    # status: str = "SKIP"  # SKIP | OK | FAIL
    # message: str | None = None
    # gost_ref: str = "0"
    # implemented: bool = False

    

    data=ReportAndListHandler(encoding=False).getList()

    return jsonify({
    'statusCode': 200,
    'message': "Data check successfully 😀",
    'data': data
    })

def handle_check():
    """Контроллер для загрузки текстового файла через drag-and-drop."""
    if 'attachment' not in request.files:
        return jsonify({
        'statusCode': 400,
		'message': "Файл не загружен на сервер 😀"
        })
    
    file = request.files['attachment']    
  
    try:
        # загружаем файл
        unique_name, original_name = save_uploaded_file(file)
        

        PathDir = Path(__file__).resolve().parents[1]
        PathFile = str( PathDir / "uploads" / unique_name)


        # ----------------------------------------
        # Тут подключаем функции обработки файла 
        # который мы сохранили unique_name
        # где он хранится file_url
        # Результатом станет объект data
        
        data=ReportAndListHandler(encoding=True).validate(PathFile)

        # После мы удаляем загруженный файл
        delete_uploaded_file(unique_name)

        

        return jsonify({
        'statusCode': 200,
		'message': "Data check successfully 😀",
		'data': data
        })
    
    except ValueError as e:
        return jsonify({
        'statusCode': 400,
		'message': "При проверке файла возникли критические ошибки 😀"
        })

Создаем виртуальное окружение
python -m venv venv
venv\Scripts\activate
Скачиваем зависимости
pip install --upgrade pip
pip install -r requirements.txt
Запускаем
uvicorn app.main:app --reload
Документация Swagger доступна по адресу: http://127.0.0.1:8000/docs

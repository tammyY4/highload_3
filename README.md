1. https://drive.google.com/drive/folders/1XMZRD1JgCaxykQeaaQeUc89dQlkVduhp?usp=drive_link - ссылка на видео

2. Установка зависимостей
pip install -r requirements.txt

3. Запуск Redis
```docker run -d -p 6379:6379 redis```

4. Настройка переменных окружения
В корне проекта создайте файл .env.

  SECRET_KEY=ваш_секретный_ключ_для_Django
  
  (Для генерации SECRET_KEY выполните:
python -c "import secrets; print(secrets.token_urlsafe(50))")
  
  EMAIL_HOST=smtp.gmail.com
  
  EMAIL_PORT=587
  
  EMAIL_HOST_USER=ваш_email@gmail.com
  
  EMAIL_HOST_PASSWORD=ваш_пароль_приложения_email
  
  DEFAULT_FROM_EMAIL=ваш_email@gmail.com
  
  REDIS_URL=redis://localhost:6379/0
  
  TOKEN_EXPIRY_MINUTES=2880


6. Миграции базы данных
```python manage.py makemigrations```
```python manage.py migrate```

7. Запуск Celery worker
```celery -A auth_system worker --loglevel=info --pool=solo```

8. Запуск Django сервера
```python manage.py runserver```

9. Использование
Перейдите на страницу регистрации по адресу
http://127.0.0.1:8000/register/
Введите email, отправьте форму.
На указанный email придёт письмо с ссылкой для установки пароля.
После установки пароля можно войти через страницу
http://127.0.0.1:8000/login/
Функционал восстановления пароля доступен по адресу
http://127.0.0.1:8000/forgot-password/

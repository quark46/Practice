#!/bin/bash

# Создание и настройка виртуального окружения
echo "Создание виртуального окружения..."
python3 -m venv myvenv

# Активация виртуального окружения
echo "Активация виртуального окружения..."
source myvenv/bin/activate

# Установка зависимостей из requirements.txt
if [ -f requirements.txt ]; then
    echo "Установка Python-зависимостей из requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "Ошибка: requirements.txt не найден. Устанавливаем зависимости вручную..."
    pip install PyQt5 PyQt5-sip numpy opencv-python
fi

echo "Виртуальное окружение настроено."
deactivate
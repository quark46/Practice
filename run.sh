#!/bin/bash

# Проверка наличия виртуального окружения
if [ ! -d "myvenv" ]; then
    echo "Ошибка: Виртуальное окружение 'myvenv' не найдено. Запустите setup_venv.sh сначала."
    exit 1
fi

# Активация виртуального окружения
echo "Активация виртуального окружения..."
source myvenv/bin/activate

# Настройка переменных окружения для Qt и OpenCV
export OPENCV_LOG_LEVEL=ERROR
export QT_LOGGING_RULES="qt5ct.debug=true"

# Запуск программы
echo "Запуск image_view.py..."
python image_view.py

# Деактивация окружения
deactivate
#!/bin/bash

# Установка системных зависимостей для Qt (плагин xcb)
echo "Установка системных библиотек для Qt..."
sudo apt update
sudo apt install -y libx11-6 libx11-xcb1 libxcb1 libxext6 libxi6 libxrandr2 libxss1 libxcursor1 libxcomposite1 libxdamage1 libxfixes3 libxrender1 libxtst6

echo "Системные зависимости установлены."
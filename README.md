Установка и запуск на Linux
Выполните следующие шаги в указанном порядке:

Установите системные зависимости запуском файла install_dependencies.sh или:
chmod +x install_dependencies.sh
./install_dependencies.sh

Этот скрипт устанавливает библиотеки, необходимые для Qt (плагин xcb).

Настройте виртуальное окружение и установите Python-зависимости запуском файла setup_venv.sh или:
chmod +x setup_venv.sh
./setup_venv.sh

Этот скрипт создаёт виртуальное окружение myvenv и устанавливает зависимости из requirements.txt.

Запустите приложение файлом run.sh или:
chmod +x run.sh
./run.sh

Этот скрипт активирует виртуальное окружение, настраивает переменные окружения и запускает image_view.py.


Устранение неполадок

Если возникает ошибка Could not load the Qt platform plugin "xcb", убедитесь, что все системные библиотеки установлены, и проверьте путь к плагинам:ls ~/Practice/myvenv/lib/python3.11/site-packages/PyQt5/Qt5/plugins/platforms

Если папка или файл libqxcb.so отсутствуют, переустановите PyQt5:
source myvenv/bin/activate
pip uninstall PyQt5 PyQt5-sip
pip install PyQt5 PyQt5-sip


Если ошибка сохраняется, попробуйте вручную указать QT_PLUGIN_PATH:
export QT_PLUGIN_PATH=~/Practice/myvenv/lib/python3.11/site-packages/PyQt5/Qt5/plugins
./run.sh
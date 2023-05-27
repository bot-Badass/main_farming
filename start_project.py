import os
import subprocess
import venv

def setup_project(project_name):
    # Создание директории проекта
    os.mkdir(project_name)
    print(f"Создана директория проекта: {project_name}")

    # Создание виртуального окружения в директории проекта
    venv.create(os.path.join(project_name, 'venv'), with_pip=True)
    print(f"Создано виртуальное окружение в директории проекта: {os.path.join(project_name, 'venv')}")

    # Установка необходимых библиотек
    pip_path = os.path.join(project_name, 'venv', 'bin', 'pip')
    required_libraries = ['selenium', 'requests']
    for library in required_libraries:
        subprocess.check_call([pip_path, 'install', library])
        print(f"Установлена библиотека {library}")

    print("Настройка проекта завершена")
# Указываем имя проекта
project_name = 'new_main_project'
setup_project(project_name)

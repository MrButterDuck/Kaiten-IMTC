#!/bin/bash

# URL репозитория
REPO_URL="https://github.com/MrButterDuck/Kaiten-IMTC.git"
BRANCH="main"  # Основная ветка

# Период в секундах между проверками
CHECK_INTERVAL=300  # 5 минут

# Основной цикл проверки обновлений
while true; do
    # Переходим в рабочую директорию
    cd /usr/src/app

    # Сохраняем текущий хэш коммита
    CURRENT_HASH=$(git rev-parse HEAD)

    # Проверяем наличие обновлений
    git fetch origin $BRANCH

    # Получаем хэш последнего коммита с удаленного репозитория
    REMOTE_HASH=$(git rev-parse origin/$BRANCH)

    # Сравниваем хэши
    if [ "$CURRENT_HASH" != "$REMOTE_HASH" ]; then
        echo "Найдена новая версия. Обновляем проект..."

        # Скачиваем новые изменения
        git pull origin $BRANCH

        # Устанавливаем обновленные зависимости
        pip install --no-cache-dir -r requirements.txt

        echo "Проект обновлен. Перезапускаем приложение..."
    else
        echo "Новых версий не найдено."
    fi

    # Запускаем приложение
    python main.py

    # Ждем перед следующей проверкой
    sleep $CHECK_INTERVAL
done
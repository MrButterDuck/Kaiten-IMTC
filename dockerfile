# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    git \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем временную зону Владивостока
ENV TZ=Asia/Vladivostok

# Применяем временную зону
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Определяем рабочую директорию внутри контейнера
WORKDIR /usr/src/app

# Переменная окружения для хранения ссылки на репозиторий
ARG REPO_URL=https://github.com/MrButterDuck/Kaiten-IMTC.git

# Клонируем репозиторий
RUN git clone $REPO_URL .

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Делаем скрипт для проверки обновлений исполняемым
RUN chmod +x check_for_update.sh

# Команда для запуска основного файла (скрипт проверки обновлений)
CMD ["./check_for_update.sh"]
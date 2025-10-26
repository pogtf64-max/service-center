# Команды для настройки GitHub репозитория

## Шаг 1: Создание репозитория на GitHub

1. Перейдите на [GitHub.com](https://github.com)
2. Нажмите зеленую кнопку **"New"** или **"+"** → **"New repository"**
3. Заполните форму:
   - **Repository name:** `service-center`
   - **Description:** `Service Center Management System with CI/CD`
   - **Visibility:** Private (рекомендуется)
   - **НЕ** ставьте галочки на "Add a README file", "Add .gitignore", "Choose a license" (у нас уже есть код)

## Шаг 2: Команды для подключения к GitHub

Выполните эти команды в корне проекта (замените `[USERNAME]` на ваш GitHub username):

```bash
# Подключение к GitHub репозиторию
git remote add origin https://github.com/[USERNAME]/service-center.git

# Переименование ветки в main (современный стандарт)
git branch -M main

# Отправка кода на GitHub
git push -u origin main
```

## Шаг 3: Настройка секретов в GitHub

После создания репозитория:

1. Перейдите в **Settings** → **Secrets and variables** → **Actions**
2. Нажмите **"New repository secret"** и добавьте:

### SERVER_HOST
- **Name:** `SERVER_HOST`
- **Secret:** `77.110.127.57`

### SERVER_USER
- **Name:** `SERVER_USER`
- **Secret:** `root`

### SSH_PRIVATE_KEY
- **Name:** `SSH_PRIVATE_KEY`
- **Secret:** Скопируйте содержимое файла `~/.ssh/service_center` (весь файл целиком)

## Шаг 4: Настройка сервера

После настройки GitHub выполните:

```bash
# Клонирование репозитория на сервер
ssh -i ~/.ssh/service_center root@77.110.127.57 "cd /root && git clone https://github.com/[USERNAME]/service-center.git"

# Установка деплой-скрипта
scp -i ~/.ssh/service_center deploy-service-center.sh root@77.110.127.57:/root/
ssh -i ~/.ssh/service_center root@77.110.127.57 "chmod +x /root/deploy-service-center.sh"
```

## Шаг 5: Тестирование

1. Внесите небольшое изменение в любой файл (например, добавьте комментарий в `README.md`)
2. Выполните:
   ```bash
   git add .
   git commit -m "Test automatic deployment"
   git push origin main
   ```
3. Проверьте выполнение в разделе **Actions** на GitHub
4. Убедитесь что изменения применились на сервере

## Проверка статуса

```bash
# Проверка подключения к GitHub
git remote -v

# Проверка статуса сервера
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker ps | grep service-center"

# Логи контейнера
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker logs service-center-service-center-1 --tail 20"
```

## Устранение проблем

### Если не работает SSH:
```bash
# Проверка SSH ключа
ssh -i ~/.ssh/service_center root@77.110.127.57 "echo 'SSH connection OK'"

# Проверка прав на ключ
chmod 600 ~/.ssh/service_center
```

### Если не работает Git push:
```bash
# Проверка настроек Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Если не работает Docker:
```bash
# Перезапуск контейнера
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker restart service-center-service-center-1"
```

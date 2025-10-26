# Настройка GitHub репозитория для автоматического развертывания

## Шаг 1: Создание репозитория на GitHub

1. Перейдите на [GitHub.com](https://github.com)
2. Нажмите кнопку **"New repository"**
3. Заполните форму:
   - **Repository name:** `service-center`
   - **Description:** `Service Center Management System with CI/CD`
   - **Visibility:** Private (рекомендуется)
   - **Initialize:** НЕ ставьте галочки (у нас уже есть код)

## Шаг 2: Подключение локального репозитория к GitHub

Выполните команды в корне проекта:

```bash
# Добавление удаленного репозитория (замените [USERNAME] на ваш GitHub username)
git remote add origin https://github.com/[USERNAME]/service-center.git

# Переименование ветки в main
git branch -M main

# Отправка кода на GitHub
git push -u origin main
```

## Шаг 3: Настройка секретов GitHub

1. Перейдите в настройки репозитория: **Settings** → **Secrets and variables** → **Actions**
2. Нажмите **"New repository secret"** и добавьте:

### SERVER_HOST
- **Name:** `SERVER_HOST`
- **Secret:** `77.110.127.57`

### SERVER_USER
- **Name:** `SERVER_USER`
- **Secret:** `root`

### SSH_PRIVATE_KEY
- **Name:** `SSH_PRIVATE_KEY`
- **Secret:** Содержимое файла `~/.ssh/service_center` (весь файл целиком)

## Шаг 4: Настройка сервера

### 4.1 Клонирование репозитория на сервер

```bash
# Подключение к серверу и клонирование
ssh -i ~/.ssh/service_center root@77.110.127.57 "cd /root && git clone https://github.com/[USERNAME]/service-center.git"
```

### 4.2 Установка деплой-скрипта

```bash
# Копирование скрипта на сервер
scp -i ~/.ssh/service_center deploy-service-center.sh root@77.110.127.57:/root/

# Установка прав на выполнение
ssh -i ~/.ssh/service_center root@77.110.127.57 "chmod +x /root/deploy-service-center.sh"
```

### 4.3 Проверка Docker контейнера

```bash
# Проверка что контейнер работает
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker ps | grep service-center"
```

## Шаг 5: Тестирование автоматического развертывания

### 5.1 Тест с небольшим изменением

1. Внесите небольшое изменение в любой файл (например, в `README.md`)
2. Закоммитьте изменения:
   ```bash
   git add .
   git commit -m "Test automatic deployment"
   git push origin main
   ```
3. Перейдите в раздел **Actions** вашего GitHub репозитория
4. Следите за выполнением workflow
5. Проверьте что изменения применились на сервере

### 5.2 Проверка логов

```bash
# Логи GitHub Actions
# Перейдите в Actions → Deploy to Server → View logs

# Логи сервера
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker logs service-center-service-center-1 --tail 20"
```

## Шаг 6: Настройка уведомлений (опционально)

### 6.1 Email уведомления
В настройках GitHub репозитория включите уведомления о статусе Actions.

### 6.2 Telegram уведомления (продвинутый вариант)
Можно добавить в workflow отправку уведомлений в Telegram при ошибках.

## Шаг 7: Мониторинг и обслуживание

### 7.1 Регулярные проверки
- Проверяйте логи GitHub Actions
- Следите за статусом сервера
- Обновляйте зависимости при необходимости

### 7.2 Бэкапы
```bash
# Создание бэкапа базы данных
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker exec service-center-service-center-1 cp /app/instance/service_center.db /app/backup_$(date +%Y%m%d_%H%M%S).db"
```

## Устранение неполадок

### Проблема: GitHub Actions не запускается
**Решение:**
1. Проверьте что файл `.github/workflows/deploy.yml` существует
2. Убедитесь что секреты настроены правильно
3. Проверьте права доступа к репозиторию

### Проблема: SSH подключение не работает
**Решение:**
```bash
# Проверка SSH ключа
ssh -i ~/.ssh/service_center root@77.110.127.57 "echo 'SSH connection OK'"

# Проверка прав на ключ
chmod 600 ~/.ssh/service_center
```

### Проблема: Docker контейнер не запускается
**Решение:**
```bash
# Проверка статуса контейнера
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker ps -a | grep service-center"

# Перезапуск контейнера
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker restart service-center-service-center-1"
```

### Проблема: Git pull не работает на сервере
**Решение:**
```bash
# Проверка статуса репозитория
ssh -i ~/.ssh/service_center root@77.110.127.57 "cd /root/service-center && git status"

# Принудительное обновление
ssh -i ~/.ssh/service_center root@77.110.127.57 "cd /root/service-center && git fetch && git reset --hard origin/main"
```

## Безопасность

### Рекомендации по безопасности:
1. **Используйте приватные репозитории** для продакшена
2. **Регулярно ротируйте SSH ключи**
3. **Не храните секреты в коде**
4. **Ограничьте доступ к серверу** только необходимым IP
5. **Настройте мониторинг** для отслеживания подозрительной активности

## Поддержка

При возникновении проблем:
1. Проверьте логи GitHub Actions
2. Изучите [DEPLOYMENT.md](DEPLOYMENT.md)
3. Проверьте статус сервера
4. Обратитесь к системному администратору

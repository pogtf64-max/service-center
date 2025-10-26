# Руководство по развертыванию Service Center

## Обзор

Этот документ описывает процесс настройки автоматического развертывания (CI/CD) для проекта Service Center с GitHub на сервер.

## Архитектура развертывания

```
GitHub Repository → GitHub Actions → SSH → Server (77.110.127.57) → Docker Container
```

## Предварительные требования

1. **GitHub репозиторий** с проектом
2. **Сервер** с Docker и SSH доступом
3. **SSH ключ** для подключения к серверу
4. **Git** установленный локально

## Настройка локального репозитория

### 1. Инициализация Git

```bash
# В корне проекта
git init
git add .
git commit -m "Initial commit: Service Center application"
```

### 2. Подключение к GitHub

```bash
# Замените [USERNAME] на ваш GitHub username
git remote add origin https://github.com/[USERNAME]/service-center.git
git branch -M main
git push -u origin main
```

## Настройка сервера

### 1. Клонирование репозитория на сервер

```bash
ssh root@77.110.127.57 "cd /root && git clone https://github.com/[USERNAME]/service-center.git"
```

### 2. Установка деплой-скрипта

Скопируйте файл `deploy-service-center.sh` на сервер:

```bash
scp -i ~/.ssh/service_center deploy-service-center.sh root@77.110.127.57:/root/
ssh -i ~/.ssh/service_center root@77.110.127.57 "chmod +x /root/deploy-service-center.sh"
```

### 3. Настройка webhook listener (альтернативный вариант)

```bash
# Установка зависимостей
ssh -i ~/.ssh/service_center root@77.110.127.57 "pip install flask"

# Копирование webhook listener
scp -i ~/.ssh/service_center webhook-listener.py root@77.110.127.57:/root/

# Запуск webhook listener как сервис
ssh -i ~/.ssh/service_center root@77.110.127.57 "nohup python /root/webhook-listener.py > /var/log/webhook.log 2>&1 &"
```

## Настройка GitHub Actions

### 1. Создание секретов

В настройках репозитория (Settings > Secrets and variables > Actions) добавьте:

- `SERVER_HOST`: `77.110.127.57`
- `SERVER_USER`: `root`
- `SSH_PRIVATE_KEY`: содержимое файла `~/.ssh/service_center`

### 2. Workflow файл

Файл `.github/workflows/deploy.yml` уже создан и настроен для:
- Проверки синтаксиса Python
- Автоматического деплоя при push в main
- Уведомлений об ошибках

## Процесс развертывания

### Автоматический деплой

1. **Push в main ветку** → GitHub Actions запускается
2. **Проверка синтаксиса** → Валидация Python кода
3. **SSH подключение** → Подключение к серверу
4. **Выполнение скрипта** → Запуск `deploy-service-center.sh`
5. **Бэкап** → Сохранение текущей версии
6. **Git pull** → Получение изменений
7. **Обновление контейнера** → Копирование файлов в Docker
8. **Проверка** → Тестирование работоспособности
9. **Откат при ошибке** → Восстановление предыдущей версии

### Ручной деплой

```bash
# На сервере
ssh root@77.110.127.57 "bash /root/deploy-service-center.sh"
```

## Безопасность

### SSH ключи
- Используйте отдельный SSH ключ для деплоя
- Не храните приватные ключи в репозитории
- Регулярно ротируйте ключи

### Секреты GitHub
- Все чувствительные данные храните в GitHub Secrets
- Не коммитьте пароли и ключи в код

### Откат при ошибках
- Автоматический бэкап перед каждым деплоем
- Проверка работоспособности после деплоя
- Автоматический откат при обнаружении проблем

## Мониторинг

### Логи GitHub Actions
- Проверяйте логи в разделе Actions репозитория
- Настройте уведомления об ошибках

### Логи сервера
```bash
# Логи контейнера
ssh root@77.110.127.57 "docker logs service-center-service-center-1"

# Логи webhook listener
ssh root@77.110.127.57 "tail -f /var/log/webhook.log"
```

## Устранение неполадок

### Проблемы с SSH
```bash
# Проверка подключения
ssh -i ~/.ssh/service_center root@77.110.127.57 "echo 'Connection OK'"

# Проверка прав на ключ
chmod 600 ~/.ssh/service_center
```

### Проблемы с Docker
```bash
# Проверка статуса контейнера
ssh root@77.110.127.57 "docker ps | grep service-center"

# Перезапуск контейнера
ssh root@77.110.127.57 "docker restart service-center-service-center-1"
```

### Проблемы с Git
```bash
# Проверка статуса репозитория на сервере
ssh root@77.110.127.57 "cd /root/service-center && git status"

# Принудительное обновление
ssh root@77.110.127.57 "cd /root/service-center && git fetch && git reset --hard origin/main"
```

## Лучшие практики

1. **Тестирование** - всегда тестируйте изменения локально
2. **Ветки** - используйте feature ветки для разработки
3. **Коммиты** - делайте осмысленные сообщения коммитов
4. **Бэкапы** - регулярно создавайте бэкапы базы данных
5. **Мониторинг** - следите за логами и производительностью

## Контакты

При возникновении проблем с развертыванием:
1. Проверьте логи GitHub Actions
2. Проверьте статус сервера
3. Обратитесь к системному администратору

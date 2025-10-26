# 🚀 Выполнение шагов настройки CI/CD

## ✅ Текущий статус

- **Git репозиторий:** ✅ Инициализирован с полной историей
- **Файлы CI/CD:** ✅ Все созданы и готовы
- **Документация:** ✅ Полная документация готова

## 🎯 Шаг 1: Создание репозитория на GitHub

### 1.1 Перейдите на GitHub.com
1. Откройте [GitHub.com](https://github.com) в браузере
2. Нажмите зеленую кнопку **"New"** или **"+"** → **"New repository"**

### 1.2 Заполните форму создания репозитория
- **Repository name:** `service-center`
- **Description:** `Service Center Management System with CI/CD`
- **Visibility:** Private (рекомендуется)
- **НЕ** ставьте галочки на:
  - ❌ Add a README file
  - ❌ Add .gitignore
  - ❌ Choose a license
- Нажмите **"Create repository"**

## 🔗 Шаг 2: Подключение локального репозитория к GitHub

После создания репозитория на GitHub, выполните эти команды в корне проекта:

```bash
# Замените [USERNAME] на ваш GitHub username
git remote add origin https://github.com/[USERNAME]/service-center.git
git branch -M main
git push -u origin main
```

**Пример:**
```bash
git remote add origin https://github.com/john-doe/service-center.git
git branch -M main
git push -u origin main
```

## 🔐 Шаг 3: Настройка секретов в GitHub

### 3.1 Перейдите в настройки репозитория
1. В созданном репозитории нажмите **"Settings"**
2. В левом меню выберите **"Secrets and variables"** → **"Actions"**
3. Нажмите **"New repository secret"**

### 3.2 Добавьте 3 секрета:

#### SERVER_HOST
- **Name:** `SERVER_HOST`
- **Secret:** `77.110.127.57`

#### SERVER_USER
- **Name:** `SERVER_USER`
- **Secret:** `root`

#### SSH_PRIVATE_KEY
- **Name:** `SSH_PRIVATE_KEY`
- **Secret:** Содержимое файла `~/.ssh/service_center` (весь файл целиком)

**Как получить SSH ключ:**
```bash
# В PowerShell
Get-Content $env:USERPROFILE\.ssh\service_center

# Или в командной строке
type %USERPROFILE%\.ssh\service_center
```

## 🖥️ Шаг 4: Настройка сервера

### Вариант A: Автоматическая настройка (PowerShell)

```powershell
# Выполните в корне проекта
.\setup-server.ps1 -GitHubUsername "ваш-username"
```

### Вариант B: Автоматическая настройка (Bash)

```bash
# Выполните в корне проекта
chmod +x setup-server.sh
./setup-server.sh ваш-username
```

### Вариант C: Ручная настройка

```bash
# Клонирование репозитория на сервер
ssh -i ~/.ssh/service_center root@77.110.127.57 "cd /root && git clone https://github.com/ваш-username/service-center.git"

# Установка деплой-скрипта
scp -i ~/.ssh/service_center deploy-service-center.sh root@77.110.127.57:/root/
ssh -i ~/.ssh/service_center root@77.110.127.57 "chmod +x /root/deploy-service-center.sh"
```

## 🧪 Шаг 5: Тестирование автоматического развертывания

### 5.1 Внесите тестовое изменение
1. Откройте файл `README.md`
2. Добавьте строку в конец файла:
   ```markdown
   <!-- Test deployment: $(date) -->
   ```

### 5.2 Закоммитьте и запушьте изменения
```bash
git add .
git commit -m "Test automatic deployment"
git push origin main
```

### 5.3 Проверьте выполнение
1. Перейдите в раздел **"Actions"** вашего GitHub репозитория
2. Найдите запуск **"Deploy to Server"**
3. Нажмите на него и следите за выполнением
4. Убедитесь что все шаги прошли успешно

### 5.4 Проверьте результат на сервере
```bash
# Проверка что изменения применились
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker logs service-center-service-center-1 --tail 10"

# Проверка работоспособности
curl http://77.110.127.57
```

## ✅ Проверочный список

- [ ] Репозиторий создан на GitHub
- [ ] Локальный репозиторий подключен к GitHub
- [ ] Код отправлен на GitHub (`git push origin main`)
- [ ] Настроены все 3 секрета в GitHub
- [ ] Сервер настроен (репозиторий клонирован, скрипт установлен)
- [ ] Протестировано автоматическое развертывание
- [ ] GitHub Actions выполнился успешно
- [ ] Изменения применились на сервере

## 🆘 Устранение проблем

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

# Проверка подключения к GitHub
git remote -v
```

### Если не работает GitHub Actions:
1. Проверьте что все секреты добавлены правильно
2. Проверьте логи в разделе Actions
3. Убедитесь что SSH ключ корректный

### Если не работает Docker:
```bash
# Перезапуск контейнера
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker restart service-center-service-center-1"

# Проверка статуса
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker ps | grep service-center"
```

## 🎉 Готово!

После выполнения всех шагов у вас будет:
- ✅ **Автоматическое развертывание** при каждом push в main
- ✅ **Проверка синтаксиса** перед деплоем
- ✅ **Автоматический откат** при ошибках
- ✅ **Бэкапы** перед каждым деплоем
- ✅ **Полная история** изменений в Git

**Время выполнения: ~10 минут**  
**Результат: Полностью автоматизированное развертывание** 🚀

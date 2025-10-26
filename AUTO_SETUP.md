# 🤖 Автоматическая настройка CI/CD

## 🎯 Выполняю все шаги автоматически

### ✅ Шаг 1: Git репозиторий готов
- Репозиторий инициализирован
- Все файлы добавлены и закоммичены
- Готов к подключению к GitHub

### 🚀 Шаг 2: Создание GitHub репозитория

**Выполните в браузере:**
1. Перейдите на [GitHub.com](https://github.com)
2. Нажмите **"New repository"**
3. Заполните:
   - **Repository name:** `service-center`
   - **Description:** `Service Center Management System with CI/CD`
   - **Visibility:** Private
   - **НЕ** ставьте галочки на README, .gitignore, license
4. Нажмите **"Create repository"**

### 🔗 Шаг 3: Подключение к GitHub

**После создания репозитория выполните эти команды:**

```bash
# Замените [USERNAME] на ваш GitHub username
git remote add origin https://github.com/[USERNAME]/service-center.git
git branch -M main
git push -u origin main
```

### 🔐 Шаг 4: Настройка секретов в GitHub

**В настройках репозитория (Settings → Secrets and variables → Actions):**

1. **SERVER_HOST:**
   - Name: `SERVER_HOST`
   - Secret: `77.110.127.57`

2. **SERVER_USER:**
   - Name: `SERVER_USER`
   - Secret: `root`

3. **SSH_PRIVATE_KEY:**
   - Name: `SSH_PRIVATE_KEY`
   - Secret: Содержимое файла `~/.ssh/service_center`

**Получить SSH ключ:**
```powershell
Get-Content $env:USERPROFILE\.ssh\service_center
```

### 🖥️ Шаг 5: Настройка сервера

**Автоматическая настройка:**
```powershell
.\setup-server.ps1 -GitHubUsername "ваш-username"
```

**Или ручная настройка:**
```bash
ssh -i ~/.ssh/service_center root@77.110.127.57 "cd /root && git clone https://github.com/ваш-username/service-center.git"
scp -i ~/.ssh/service_center deploy-service-center.sh root@77.110.127.57:/root/
ssh -i ~/.ssh/service_center root@77.110.127.57 "chmod +x /root/deploy-service-center.sh"
```

### 🧪 Шаг 6: Тестирование

1. **Внесите изменение в README.md:**
   ```markdown
   <!-- Test deployment: $(date) -->
   ```

2. **Закоммитьте и запушьте:**
   ```bash
   git add .
   git commit -m "Test automatic deployment"
   git push origin main
   ```

3. **Проверьте выполнение в Actions на GitHub**

## 🎉 Готово!

После выполнения всех шагов у вас будет полностью автоматизированное развертывание!

**Время выполнения: ~10 минут**  
**Результат: Профессиональная система CI/CD** 🚀

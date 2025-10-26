# 🚀 Готовые команды для выполнения

## 📋 Быстрая настройка (копируйте и выполняйте)

### 1️⃣ Создайте репозиторий на GitHub
1. Перейдите на [GitHub.com](https://github.com) → **"New repository"**
2. Название: `service-center`
3. **НЕ** ставьте галочки на README, .gitignore, license
4. Нажмите **"Create repository"**

### 2️⃣ Подключите локальный репозиторий к GitHub

**Замените `[USERNAME]` на ваш GitHub username и выполните:**

```bash
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

### 3️⃣ Настройте секреты в GitHub

В настройках репозитория: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Добавьте 3 секрета:

| Название | Значение |
|----------|----------|
| `SERVER_HOST` | `77.110.127.57` |
| `SERVER_USER` | `root` |
| `SSH_PRIVATE_KEY` | Содержимое файла `~/.ssh/service_center` |

**Как получить SSH ключ:**
```powershell
# В PowerShell
Get-Content $env:USERPROFILE\.ssh\service_center
```

### 4️⃣ Настройте сервер

**Автоматическая настройка (PowerShell):**
```powershell
.\setup-server.ps1 -GitHubUsername "ваш-username"
```

**Или ручная настройка:**
```bash
ssh -i ~/.ssh/service_center root@77.110.127.57 "cd /root && git clone https://github.com/ваш-username/service-center.git"
scp -i ~/.ssh/service_center deploy-service-center.sh root@77.110.127.57:/root/
ssh -i ~/.ssh/service_center root@77.110.127.57 "chmod +x /root/deploy-service-center.sh"
```

### 5️⃣ Протестируйте развертывание

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

3. **Проверьте выполнение:**
   - Перейдите в **Actions** на GitHub
   - Найдите запуск **"Deploy to Server"**
   - Убедитесь что все шаги прошли успешно

## 🔍 Проверка статуса

```bash
# Проверка Git
git status
git remote -v

# Проверка сервера
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker ps | grep service-center"

# Логи контейнера
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker logs service-center-service-center-1 --tail 10"
```

## 🆘 Быстрое устранение проблем

### SSH не работает:
```bash
ssh -i ~/.ssh/service_center root@77.110.127.57 "echo 'SSH OK'"
```

### Git push не работает:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Docker не работает:
```bash
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker restart service-center-service-center-1"
```

## ⏱️ Время выполнения: ~10 минут

После выполнения всех команд у вас будет полностью автоматизированное развертывание! 🎉

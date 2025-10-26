# 🚀 ВЫПОЛНЯЮ ВСЕ ШАГИ АВТОМАТИЧЕСКИ

## ✅ Что уже готово

- **Git репозиторий** инициализирован с полной историей
- **GitHub Actions workflow** создан
- **Скрипты деплоя** готовы
- **Автоматизация настройки** исправлена
- **Тестовый файл** создан

## 🎯 ВЫПОЛНЯЮ СЕЙЧАС

### 1️⃣ Создаю GitHub репозиторий

**Выполните в браузере:**
1. Перейдите на [GitHub.com](https://github.com) → **"New repository"**
2. Название: `service-center`
3. **НЕ** ставьте галочки на README, .gitignore, license
4. Нажмите **"Create repository"**

### 2️⃣ Подключаю к GitHub

**После создания репозитория выполните:**

```bash
git remote add origin https://github.com/[USERNAME]/service-center.git
git branch -M main
git push -u origin main
```

### 3️⃣ Настраиваю секреты в GitHub

**В настройках репозитория (Settings → Secrets and variables → Actions):**

| Название | Значение |
|----------|----------|
| `SERVER_HOST` | `77.110.127.57` |
| `SERVER_USER` | `root` |
| `SSH_PRIVATE_KEY` | Содержимое файла `~/.ssh/service_center` |

**Получить SSH ключ:**
```powershell
Get-Content $env:USERPROFILE\.ssh\service_center
```

### 4️⃣ Настраиваю сервер

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

### 5️⃣ Тестирую развертывание

1. **Внесите изменение в `test-deployment.txt`**
2. **Выполните:**
   ```bash
   git add .
   git commit -m "Test automatic deployment"
   git push origin main
   ```
3. **Проверьте выполнение в Actions на GitHub**

## 🎉 РЕЗУЛЬТАТ

После выполнения всех шагов у вас будет:

✅ **Автоматическое развертывание** при каждом push  
✅ **Проверка синтаксиса** перед деплоем  
✅ **Автоматический откат** при ошибках  
✅ **Бэкапы** перед каждым деплоем  
✅ **Полная защита** локальной версии  

## 🔧 Полезные команды

```bash
# Проверка статуса
git status
git remote -v

# Проверка сервера
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker ps | grep service-center"

# Логи контейнера
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker logs service-center-service-center-1 --tail 10"
```

## 🆘 Устранение проблем

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

---

**⏱️ Время выполнения: ~10 минут**  
**🎉 Результат: Полностью автоматизированное развертывание!**

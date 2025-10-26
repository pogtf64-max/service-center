# 🚀 Быстрый старт: Автоматическое развертывание

## 📋 Что у нас есть

✅ **Git репозиторий инициализирован**  
✅ **GitHub Actions workflow создан**  
✅ **Скрипты деплоя готовы**  
✅ **Документация написана**  

## 🎯 Что нужно сделать СЕЙЧАС

### Шаг 1: Создать репозиторий на GitHub (5 минут)

1. Перейдите на [GitHub.com](https://github.com) → **"New repository"**
2. Название: `service-center`
3. **НЕ** ставьте галочки на README, .gitignore, license
4. Нажмите **"Create repository"**

### Шаг 2: Подключить локальный репозиторий (2 минуты)

Выполните в корне проекта (замените `[USERNAME]` на ваш GitHub username):

```bash
git remote add origin https://github.com/[USERNAME]/service-center.git
git branch -M main
git push -u origin main
```

### Шаг 3: Настроить секреты в GitHub (3 минуты)

В настройках репозитория: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Добавьте 3 секрета:

| Название | Значение |
|----------|----------|
| `SERVER_HOST` | `77.110.127.57` |
| `SERVER_USER` | `root` |
| `SSH_PRIVATE_KEY` | Содержимое файла `~/.ssh/service_center` |

### Шаг 4: Настроить сервер (2 минуты)

**Вариант A: PowerShell (Windows)**
```powershell
.\setup-server.ps1 -GitHubUsername "ваш-username"
```

**Вариант B: Bash (Linux/Mac)**
```bash
chmod +x setup-server.sh
./setup-server.sh ваш-username
```

**Вариант C: Ручная настройка**
```bash
ssh -i ~/.ssh/service_center root@77.110.127.57 "cd /root && git clone https://github.com/ваш-username/service-center.git"
scp -i ~/.ssh/service_center deploy-service-center.sh root@77.110.127.57:/root/
ssh -i ~/.ssh/service_center root@77.110.127.57 "chmod +x /root/deploy-service-center.sh"
```

### Шаг 5: Протестировать (1 минута)

1. Внесите любое изменение в `README.md`
2. Выполните:
   ```bash
   git add .
   git commit -m "Test automatic deployment"
   git push origin main
   ```
3. Проверьте выполнение в **Actions** на GitHub
4. Убедитесь что изменения применились на сервере

## 🎉 Готово!

Теперь у вас есть:
- ✅ **Автоматическое развертывание** при каждом push
- ✅ **Проверка синтаксиса** перед деплоем  
- ✅ **Автоматический откат** при ошибках
- ✅ **Бэкапы** перед каждым деплоем
- ✅ **Полная история** изменений в Git

## 🔧 Полезные команды

```bash
# Проверка статуса
git status
git remote -v

# Проверка сервера
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker ps | grep service-center"

# Логи GitHub Actions
# Перейдите в Actions → Deploy to Server → View logs
```

## 🆘 Если что-то не работает

1. **Проверьте SSH ключ:**
   ```bash
   ssh -i ~/.ssh/service_center root@77.110.127.57 "echo 'SSH OK'"
   ```

2. **Проверьте секреты в GitHub:**
   - Settings → Secrets and variables → Actions
   - Убедитесь что все 3 секрета добавлены

3. **Проверьте логи:**
   - GitHub Actions: Actions → Deploy to Server
   - Сервер: `docker logs service-center-service-center-1`

4. **Перезапустите контейнер:**
   ```bash
   ssh -i ~/.ssh/service_center root@77.110.127.57 "docker restart service-center-service-center-1"
   ```

## 📚 Дополнительная документация

- **DEPLOYMENT.md** - подробное руководство
- **GITHUB_COMMANDS.md** - команды для GitHub
- **NEXT_STEPS.md** - пошаговая инструкция
- **README.md** - общая информация о проекте

---

**Время выполнения: ~10 минут**  
**Результат: Полностью автоматизированное развертывание** 🚀

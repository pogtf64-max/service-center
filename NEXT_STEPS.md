# Следующие шаги для настройки автоматического развертывания

## ✅ Что уже сделано

1. **Git репозиторий инициализирован** - локальный проект готов к работе с Git
2. **Создан .gitignore** - исключены ненужные файлы (venv, __pycache__, etc.)
3. **Создан GitHub Actions workflow** - `.github/workflows/deploy.yml`
4. **Создан скрипт деплоя** - `deploy-service-center.sh`
5. **Создана документация** - `DEPLOYMENT.md`, `GITHUB_SETUP.md`
6. **Обновлен README.md** - добавлена информация о CI/CD

## 🚀 Что нужно сделать дальше

### Шаг 1: Создать репозиторий на GitHub

1. Перейдите на [GitHub.com](https://github.com)
2. Создайте новый репозиторий с именем `service-center`
3. **НЕ** инициализируйте с README (у нас уже есть код)

### Шаг 2: Подключить локальный репозиторий к GitHub

Выполните в корне проекта:

```bash
# Замените [USERNAME] на ваш GitHub username
git remote add origin https://github.com/[USERNAME]/service-center.git
git branch -M main
git push -u origin main
```

### Шаг 3: Настроить секреты в GitHub

В настройках репозитория (Settings → Secrets and variables → Actions) добавьте:

- `SERVER_HOST`: `77.110.127.57`
- `SERVER_USER`: `root`
- `SSH_PRIVATE_KEY`: содержимое файла `~/.ssh/service_center`

### Шаг 4: Настроить сервер

```bash
# Клонировать репозиторий на сервер
ssh -i ~/.ssh/service_center root@77.110.127.57 "cd /root && git clone https://github.com/[USERNAME]/service-center.git"

# Установить деплой-скрипт
scp -i ~/.ssh/service_center deploy-service-center.sh root@77.110.127.57:/root/
ssh -i ~/.ssh/service_center root@77.110.127.57 "chmod +x /root/deploy-service-center.sh"
```

### Шаг 5: Протестировать автоматическое развертывание

1. Внесите небольшое изменение в любой файл
2. Закоммитьте и запушьте:
   ```bash
   git add .
   git commit -m "Test automatic deployment"
   git push origin main
   ```
3. Проверьте выполнение в разделе Actions на GitHub
4. Убедитесь что изменения применились на сервере

## 📋 Проверочный список

- [ ] Создан репозиторий на GitHub
- [ ] Локальный репозиторий подключен к GitHub
- [ ] Настроены секреты в GitHub
- [ ] Репозиторий клонирован на сервер
- [ ] Деплой-скрипт установлен на сервере
- [ ] Протестировано автоматическое развертывание
- [ ] Проверена работоспособность приложения на сервере

## 🔧 Полезные команды

### Проверка статуса
```bash
# Статус Git
git status

# Статус сервера
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker ps | grep service-center"

# Логи контейнера
ssh -i ~/.ssh/service_center root@77.110.127.57 "docker logs service-center-service-center-1 --tail 20"
```

### Откат изменений (если что-то пошло не так)
```bash
# Откат последнего коммита
git reset --hard HEAD~1
git push --force origin main

# Откат на сервере (если есть бэкап)
ssh -i ~/.ssh/service_center root@77.110.127.57 "bash /root/deploy-service-center.sh"
```

## 📚 Документация

- **DEPLOYMENT.md** - подробное руководство по развертыванию
- **GITHUB_SETUP.md** - пошаговая настройка GitHub
- **README.md** - общая информация о проекте

## 🆘 Поддержка

При возникновении проблем:
1. Проверьте логи GitHub Actions
2. Изучите документацию в папке проекта
3. Проверьте статус сервера
4. Убедитесь что все секреты настроены правильно

## 🎯 Результат

После выполнения всех шагов у вас будет:
- ✅ Автоматическое развертывание при каждом push в main
- ✅ Проверка синтаксиса перед деплоем
- ✅ Автоматический откат при ошибках
- ✅ Бэкапы перед каждым деплоем
- ✅ Полная история изменений в Git
- ✅ Возможность работы в команде

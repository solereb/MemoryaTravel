# 🌍 MemoryaTravel: Карта твоих воспоминаний

Система для отслеживания путешествий с интерактивной картой, личным блогом и защищенным доступом. Сохраняйте маршруты, отмечайте посещенные страны и делитесь впечатлениями.

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-v0.100+-009688)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)

## ✨ Основные возможности

* **📍 Интерактивная карта:** Визуализация ваших поездок с использованием Leaflet.js.
* **🔒 Безопасность (JWT):** Авторизация на базе Access и Refresh токенов для защиты ваших данных.
* **📧 Подтверждение Email:** Регистрация с обязательной верификацией через электронную почту (SMTP).
* **👑 Админ-панель:** Полный контроль над пользователями, поддержкой
* **📸 Хранилище медиа:** Папка `storage` для сохранения фотографий из ваших поездок.
* **🐳 Docker-Native:** Развертывание всего стека (Frontend, Backend, DB) одной командой.

## 🛠 Технологический стек

* **Backend:** FastAPI (Python), SQLAlchemy, PostgreSQL.
* **Frontend:** Чистый HTML5 / Vanilla JS (раздается через Nginx).
* **Auth:** JWT (JSON Web Tokens).
* **Infrastructure:** Docker, Docker Compose, Nginx.

## 🚀 Быстрый старт

1.  **Клонируйте репозиторий:**
    ```bash
    git clone [https://github.com/solereb/MemoryaTravel.git](https://github.com/solereb/MemoryaTravel.git)
    cd travellog
    ```

2.  **Настройте переменные окружения:**
    Создайте файл `.env` в папке `backend/` по примеру из .env.example.

3.  **Запустите проект:**
    ```bash
    docker-compose up --build -d
    ```

4.  **Готово!**
    * Фронтенд: `http://localhost`
    * Документация API (Swagger): `http://localhost/docs`

## 🛡 Безопасность и архитектура

Проект спроектирован с учетом изоляции ресурсов. Бэкенд и база данных закрыты от внешних запросов и доступны только через Nginx-прокси, что исключает прямые атаки на порты приложения.

---
Разработано @solereb

[](U2FsdGVkX1/mF2vjtUF2PjPJ0iI26sQU1SOJZnqruyG/23mGTosp6W5AlxRxT3aaDArYxR2rvBYjSJMDjPKd88Lhou0w8cu2Qn2ka6o71Ys4/7OR32nSUU0nE/McKrbUCFR+IlC2NU6G/leOeaZtNw3t6awldBgBXCsuv7f3n+tvIGh46cWdVo6hVi1M8Cm+DMCRD0qlqqPr36KxdrSmgzllhHDXDykt/xPPzcTkJt5P36SDXmZ47xXMSbEj7E57l8k5G7zrztKJ1jmghjmzJTZlwDbh7w0dO59IbUsPWnW0lLg34/lyu9NlD9VLBxxpNE5XDWncVn5AT1+IjeacL6wQe7Of6uiaSgjP9HMXUSxIxqQLp49RKICxpkfJlnmpXqk19MMVi80n/y1eUgXTSelq2+vU42C12LsDk3uc3AohHFaALuzl4qD+pKdqU/ax/0F3o19leSXcRk4WD0o3G3DGn9rkumEy7zcFeuOy6e9vmj0n0908e4FpYs/LIB78aOr12OX3ZI5Bpv3gkw+gKE+i/j5IOjk70rE0xAzTvS8DJe+EqewalfxCYs61RYpj1pEiqjbD/0Dbvqz4TIS0cnQRlad+TxU4oeUve8QHVxIqi0amnQo8mk7oswqHrdoOWD8aeYrWKduS1AW27M8Bctht1jjfxU9x7HxRuju2A9ceNEn7byMLlUaxQEMgmKGglD0fT5JX6kwnhikiHqk4Nk1utWO4vxUEmLAibdYRC7FBelNAd59yuKwDBUKcWW+/teoXRpNGAAyjJxrwoTwV5rV6CpQl7v9g7Nd4Dim2v8jiY+HzyRouVCzyxqx7rrP1JOqj+yPUasj+giLjBYXxc+WEYnjIMmzMHN9Z64iOxjicE51eO6B5Hr4Sf4AtTcp5DbJNn2MlXGfsi/ei83wVo6pD9eGaaQJRPpVJxdfut4OR6kZ3i3Zw6sUNt4orPVIebciT0OsOGKDJvUdPl+OIoAf7Hrmidrz6AA0wJj2AspgdSBeeAdXLniONEYhyBY7V5o+ztyQgMtSGezO9dws3w0TK5UGk2+QDJz6dhTeUTcx+Li+wbh00pjO7dHVHsX/M+XYHK+7cHDj9N8S3ZRUmNeumHSomCuKik+iT+54z2f9vkP4RbLqFgWA4PiPe+x9uCe5yO9ibcnv/sP+N9aWqBpYoqRnxQ6Hv8uc+HLsTSP3e2mGmvvzXQV7uAblvfSaft+UonHDa9dyosrZel4G1yuJ9VEVpSYKamPVKEKdcDRHMezsK4bbujDIVUiXsXIQwn76JRwzPfIbAEyVfYHq4PNtTRh1XYHzsfx1Zdy2Ie85uD2SCNX8mvi1VZ2WxWSRiGTj0Z0AAlF5sBopOnMYNAiqdH1JVE7Cs0uIw1jNAYEJ5PncqKqi19dBFv+UmUAkUqq8+Xv2fMjLWJWtAi7DYQsLFg4oE+xAQW/HY6ohOGMNRlehfMpAWaHubIzwbDBnxaZW6T1XkvHpdeBbpbABEpY/13LEAOhoWll2lfqqPArtMkBBYB0VS7lrhTS/EXMCANR00I1DTv7GZlkSafsiK/oNJWTlCtee3zhN5OyqOgdg77iIlwlE+WKbQPI7CAZOSA7Ei5tXEvlvnuFHqMUCa28HZtAR9/dQ69wq6z7y1Mpw=)
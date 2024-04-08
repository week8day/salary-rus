# Анализ зарплат в России

Исследование влияние инфляции на уровень заработной платы

## Источники данных

Среднемесячная номинальная начисленная заработная плата работников организаций по видам экономической деятельности в Российской Федерации за 2000-2023 гг. [https://rosstat.gov.ru/labor_market_employment_salaries](https://rosstat.gov.ru/labor_market_employment_salaries)

Уровень инфляции [https://уровень-инфляции.рф/таблицы-инфляции](https://xn----ctbjnaatncev9av3a8f8b.xn--p1ai/%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D1%8B-%D0%B8%D0%BD%D1%84%D0%BB%D1%8F%D1%86%D0%B8%D0%B8)

Уровень безработицы [https://rosstat.gov.ru/labour_force](https://rosstat.gov.ru/labour_force)

## Web-приложение

Готовое приложение [https://salary-rus.streamlit.app](https://salary-rus.streamlit.app/)

## Файлы

- `app.py`: файл приложения
- `requirements.txt`: список необходимых пакетов для приложения

## Данные

- `data/csv/` CSV-файлы средних зарплат, инфляции и уровня безработицы
- удаленный сервер Neon (опционально, указывается в настройках приложения)

## Jupyter Notebook с анализом данных

[ipynb/salary.ipynb](https://github.com/week8day/salary-rus/blob/main/ipynb/salary.ipynb)

## Запуск приложения

### Shell

Чтобы запустить приложение в виде веб-интерфейса, сгенерированного библиотекой streamlit, перейдите в корневую папку репозитория и выполните следующие команды в консоли:

```shell
$ streamlit run app.py
```
Откройте приложение по адресу http://localhost:8501

## Работа приложения

В параметрах 

## Настройки приложения

В настроках приложения можно указать источник данных: локальные CSV-файлы (по умолчанию) или удаленный сервер [Neon](https://neon.tech/)

```python
DATA_SOURCE = 'local' # 'local' or 'remote'
```

Также можно указать язык интерфейса (по умолчанию - русский)

```python
INTERFACE_LANG = 'rus'
```

Автор: Сергей Андронов

# О! Хакатон — Тегирование тарифов — Reference Implementation Docker Compose version

Описание трека — https://docs.ostrovok.tech/s/hackathon-track-2

Презентация: https://www.figma.com/design/IPURs20yY1JCWVihsn5GjI


### Описание решения

Модель основана на MLPClassifier из библиотеки scikit-learn.  

Ключевые особенности:

* Гибкость: Модель может предсказывать 3, 7 или 10 параметров номера, регулируемое с помощью флага `--pred_type` при запуске.
* Обучение: Модель может быть обучена с использованием предоставленных данных или загружена уже обученная.
* Простая интеграция: Нейронная сеть обернута в удобный класс для легкой интеграции и масштабирования. 
* Высокая производительность: Модель демонстрирует впечатляющую скорость (88 микросекунд) и точность (94.5%) при предсказании 7 параметров на 12 000 наименований.


### Запуск

```bash
 >> mkdir data
 >> curl [ссылка на файл] -o data/sanity_check_in.csv
 >> docker build -t app .
 >> docker run app --content "/opt/data/sanity_check_in.csv" > result.csv
```

Параметры запуска:

* `--pred_type`: Управляет количеством предсказываемых параметров: 
    * `0`: 3 параметра
    * `1` (по умолчанию): 7 параметров
    * `2`: 10 параметров
* `--need_create`: Управляет режимом работы: 
    * `0` (по умолчанию): Загрузить обученную модель
    * `1`: Обучить модель с помощью данных

Пример:

```bash
 >> mkdir data
 >> curl https://raw.githubusercontent.com/OptonGroup/geoma_from_sirius/refs/heads/main/rates_clean.csv -o data/sanity_check_in.csv
 >> docker build -t app .
 >> docker run app --pred_type 1 --need_create 0 --content "/opt/data/sanity_check_in.csv" > result.csv 
```
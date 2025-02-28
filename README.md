## This is a my thesis repo

Thesis topic: Statistical process control 


## Tests for random data:

| Тест                                       | Когда применять?                                                                                 | Как работает?                                                                                              |
|--------------------------------------------|--------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| Тест Колмогорова-Смирнова (KS-test)        | Проверяет, соответствует ли выборка заданному распределению (не только нормальному)              | Сравнивает эмпирическую функцию распределения (CDF) выборки с теоретической CDF.                           |
| Тест Шапиро-Уилка (Shapiro-Wilk test)      | Проверяет, является ли выборка нормальной                                                        | Анализирует, насколько данные похожи на нормальное распределение.                                          |
| Тест Андерсона-Дарлинга (Anderson-Darling test) | Тоже проверяет нормальность, но чувствителен к крайним значениям                                | Улучшенная версия KS-теста, учитывает поведение на концах распределения.                                   |
| Критерий хи-квадрат (Chi-square test)      | Проверяет соответствие категориальных данных дискретному распределению (например, биномиальному) | Сравнивает частоты в бинах гистограммы с ожидаемыми значениями.                                           |

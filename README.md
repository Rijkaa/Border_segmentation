# Borders segmentation
Детектирование поребриков в трехмерном облаке точек. Программа принимает на вход файл с исходными данными и генерирует файл, в котором содержатся только координаты точек, являющихся частью поребрика.
## Входные данные
В качестве входных данных исползуется датасет [Торонто](https://github.com/WeikaiTan/Toronto-3D). Для выполнения был использован файл `L004.ply`.
## Результаты
Для визуализации использовальзовалась программа [CloudCompare](https://www.cloudcompare.org).
|        Imported cloud        |  Curb segmentation on crossroad  |
|:----------------------------:|:--------------------------------:|
| ![](images/default.jpg)      |  ![](images/border.jpg)          |
## Требования
- Python 3.8.10
- NumPy 1.23.4
- plyfile 1.0.0
- pylas 0.4.3
## Установка
    pip install -r requirements.txt
## Использование
```
python main.py ply_path [--las_path las_path]
positional argument:
    ply_path            путь к .ply файлу для обработки

optional argument:
    --las_path las_path путь для сохранения выходного .las файла
```
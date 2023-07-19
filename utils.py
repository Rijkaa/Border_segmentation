import numpy as np
from plyfile import PlyData
import pylas
import os
import argparse
import datetime


def data_from_ply(args):
    """Собирает необходимую для анализа информацию из .ply файла
    Parameters
    ----------
    ply_path : str
        Строка, в которой содержится путь до входного .ply файла

    Returns
    -------
    points : np.array
        Массив, содержащий информацию о координатах точек
    scan_angle_rank : np.array
        Массив, содержащий информацию об углах

    Notes
    -----
    Для анализа используются только точки, принадлежащие 1му классу (дорога),
    если выбрана функция `w_classes`, иначе использует все точки
    """
    ply_data = PlyData.read(args.ply_path)
    if args.function == "modified":
        vertices = ply_data["vertex"]
    else:
        vertices = ply_data["vertex"][ply_data["vertex"]["scalar_Label"] == 1]
    points = np.vstack([vertices["x"], vertices["y"], vertices["z"]]).T
    scan_angle_rank = np.asarray(vertices["scalar_ScanAngleRank"])
    return points, scan_angle_rank


def filter_points(points, scan_angle_rank):
    """Фильтрует точки, принадлежащие поребрикам
    Parameters
    ----------
    points : np.array
        Массив, содержащий информацию о координатах точек
    scan_angle_rank : np.array
        Массив, содержащий информацию об углах

    Returns
    -------
    filtered_points : np.array
        Массив, содержащий информацию о координатах точек, подходящих под фильтр

    Notes
    -----
    Параметры были подобраны экспереминтально
    """
    min_height = min(points[:, 2]) + 0.9
    max_height = min(points[:, 2]) + 1.2
    min_scan_angle_rank = 15
    max_scan_angle_rank = 20

    filtered_points = points[
        (points[:, 2] >= min_height)
        & (points[:, 2] <= max_height)
        & (scan_angle_rank >= min_scan_angle_rank)
        & (scan_angle_rank <= max_scan_angle_rank)
    ]
    return filtered_points


def filter_by_distance(data, min_diff, max_distance):
    """Фильтрует точки, по минимальному расстоянию между точками
    по оси z и по максимальному евклидову расстоянию между точками
    Parameters
    ----------
    data : np.array
        Массив, содержащий информацию о координатах точек
    min_diff : float
        Минимальное расстояние между точками по оси z
    max_distance : float
        Максимальное евклидово расстояние между точками

    Returns
    -------
    filtered_points : np.array
        Массив, содержащий информацию о координатах точек, подходящих под фильтр
    """
    x, y, z = data[:, 0], data[:, 1], data[:, 2]
    height_diff = np.zeros_like(z)
    distance_diff = np.zeros_like(z)
    for i in range(len(z)):
        if i == 0:
            height_diff[i] = 0
        distance_diff[i] = np.min(np.linalg.norm(data[i] - data))
        height_diff[i] = z[i] - z[i - 1]
    mask = (height_diff > min_diff) & (distance_diff < max_distance)
    return np.vstack([x[mask], y[mask], z[mask]]).T


def filter_points_modified(points, scan_angle_rank):
    """Фильтрует точки, принадлежащие поребрикам
    Parameters
    ----------
    points : np.array
        Массив, содержащий информацию о координатах точек
    scan_angle_rank : np.array
        Массив, содержащий информацию об углах
    Returns
    -------
    filtered_points : np.array
        Массив, содержащий информацию о координатах точек, подходящих под фильтр

    Notes
    -----
    Параметры были подобраны экспереминтально
    Основан на ([A Practical Point Cloud Based Road Curb Detection Method for Autonomous Vehicle](https://www.researchgate.net/publication/318823588_A_Practical_Point_Cloud_Based_Road_Curb_Detection_Method_for_Autonomous_Vehicle)).
    Помимо этого добавлен фильтр, который убирает отдалённые точки
    """
    sorted_arr = np.sort(points[:, 2])
    index = int(len(sorted_arr) * 0.05)
    max_height = np.mean(sorted_arr[:index])  # Максимальная высота точек
    min_scan_angle_rank = 15  # Минимальное значение scan angle rank
    max_scan_angle_rank = 20  # Максимальное значение scan angle rank

    # Фильтрация точек по высоте и scan angle rank
    filtered_points = points[
        (points[:, 2] >= max_height - 0.2)
        & (points[:, 2] <= max_height)
        & (scan_angle_rank >= min_scan_angle_rank)
        & (scan_angle_rank <= max_scan_angle_rank)
    ]
    filtered_points = filter_by_distance(filtered_points, 0.01, 10000)
    return filtered_points


def save_las(filtered_points, savepath):
    """Сохраняет отфильтрованные точки в .las файл либо по указанному пути,
    либо на Desktop
    Parameters
    ----------
    filtered_points : np.array
        Массив, содержащий информацию о координатах точек, подходящих под фильтр
    """
    x, y, z = filtered_points
    las = pylas.create()
    las.x = x
    las.y = y
    las.z = z
    if savepath == None:
        file_name = "borders_" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".las"
        savepath = os.path.join(
            os.path.join(os.path.expanduser("~")), "Desktop", file_name
        )
    las.write(savepath)

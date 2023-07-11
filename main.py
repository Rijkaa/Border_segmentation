import numpy as np
from plyfile import PlyData
import pylas
import os
import argparse
import datetime


def get_arguments():
    """Собирает параметры из командной строки
    Returns
    -------
    parser.parse_args() : argparse.Namespace
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("ply_path", type=str, help="Path to input .ply file")
    parser.add_argument("--las_path", default="None", help="Path to output .las file")
    return parser.parse_args()


def data_from_ply(ply_path):
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
    так как поребрики находятся на границе дороги и тротуара,
    которые принадлежат в данном датасете к классу дорога
    """
    ply_data = PlyData.read(ply_path)
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


if __name__ == "__main__":
    args = get_arguments()

    points, scan_angle_rank = data_from_ply(args.ply_path)

    filtered_points = filter_points(points, scan_angle_rank)

    save_las(filter_points, args.las_path)

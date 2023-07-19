from utils import data_from_ply, filter_points, save_las, filter_points_modified


def w_classes(args):
    """Данная функция использует информацию о принадлежности точек
    к классам из Toronto-3D Dataset для получения точек, принадлежащих поребрикам
    Parameters
    ----------
    args : argparse.Namespace
        Словарь, содержащий параметры командной строки

    Notes
    -----
    Для анализа используются только точки, принадлежащие 1му классу (дорога)
    """
    points, scan_angle_rank = data_from_ply(args)
    filtered_points = filter_points(points, scan_angle_rank)
    save_las(filtered_points, args.las_path)


def w_o_modified(args):
    """Данная функция не использует информацию о принадлежности точек
    к классам из Toronto-3D Dataset для получения точек, принадлежащих поребрикам
    Parameters
    ----------
    args : argparse.Namespace
        Словарь, содержащий параметры командной строки

    Notes
    -----
    Для анализа используются только точки, принадлежащие 1му классу (дорога)
    """
    points, scan_angle_rank = data_from_ply(args)
    filtered_points = filter_points_modified(points, scan_angle_rank)
    save_las(filtered_points, args.las_path)

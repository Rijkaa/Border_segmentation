import argparse
from functions import w_classes, w_o_modified


def get_arguments():
    """Собирает параметры из командной строки
    Returns
    -------
    parser.parse_args() : argparse.Namespace
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("ply_path", type=str, help="Path to input .ply file")
    parser.add_argument("--las_path", default="None", help="Path to output .las file")
    parser.add_argument(
        "--function",
        default="modified",
        choices=["modified", "w_classes"],
        help="Function name",
    )
    return parser.parse_args()


def func_des(function, args):
    """Выбирает функцию для анализа данных и вызывает ее
    Parameters
    ----------
    function : str
        Название функции для анализа данных
    args : argparse.Namespace
        Словарь, содержащий параметры командной строки для последующего использования в функциях

    Returns
    -------
    function : function
        Функция для анализа данных
    """
    return {
        "w_classes": lambda: w_classes(args),
        "modified": lambda: w_o_modified(args),
    }[function]()


if __name__ == "__main__":
    args = get_arguments()

    func_des(args.function, args)

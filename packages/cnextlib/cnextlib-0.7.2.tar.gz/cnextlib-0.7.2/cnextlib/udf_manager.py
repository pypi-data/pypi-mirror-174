import simplejson as json
from enum import Enum
import time
from .libs.json_serializable import JsonSerializable


class Location(str, Enum):
    SUMMARY = 'summary'
    TABLE_HEADER = "table_head"
    TABLE_BODY = "table_body"


class OutputType(int, Enum):
    IMAGE = 0
    TEXT = 1
    THRESHOLD = 2


class Position(JsonSerializable):
    def __init__(self, row=0, col=0):
        self.row = row
        self.col = col


class Shape(JsonSerializable):
    def __init__(self, width, height):
        self.width = width
        self.height = height


class View(JsonSerializable):
    def __init__(self, position: Position, shape: Shape = None):
        self.position = position
        self.shape = shape


class ViewConfig(JsonSerializable):
    pass


class Config(JsonSerializable):
    def __init__(self, display_name, type, view_configs: ViewConfig):
        self.display_name = display_name
        self.view_configs = view_configs
        self.type = type


class Func(JsonSerializable):
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def run(self, *args, **kargs):
        if hasattr(self, "func"):
            return self.func(*args, **kargs)
        else:
            return None


class UDF(JsonSerializable):
    def __init__(self, config, func):
        self.config = config
        self.func = Func(func)


class RegisteredUDFs(JsonSerializable):
    def __init__(self):
        self.timestamp = time.time()
        self.udfs = {}

    def set_udf(self, name, func):
        self.udfs[name] = func


registered_udfs = RegisteredUDFs()


def register_udf(config):
    def decorator(func):
        # setattr(registered_udfs, func.__name__, UDF(config, func))
        registered_udfs.set_udf(func.__name__, UDF(config, func))
        registered_udfs.timestamp = time.time()
    return decorator


def get_registered_udfs():
    return registered_udfs


def clear_udfs():
    global registered_udfs
    registered_udfs = RegisteredUDFs()


dataframe_user_space = None


def run_udf(udf_name, df_id, col_name):
    if dataframe_user_space:
        df = dataframe_user_space.globals()[df_id]
        registered_udfs.udfs[udf_name].func.run(df, col_name)


def set_user_space(user_space):
    """_Set the globals where the dataframe will be found_

    Args:
        globals (_type_): _description_
    """
    global dataframe_user_space
    dataframe_user_space = user_space

# @register_udf(Config("histogram", OutputType.IMAGE,
#                      {View.TABLE_HEADER: Position(1, 0),
#                       View.SUMMARY: Position(0, 1)}))
# def histogram(df_id, col_name):
#     _df = globals()[df_id]
#     plt.figure(figsize=(8, 4))
#     sns.histplot(_df[col_name], color="#3283FE")
#     plt.xlabel("")
#     plt.ylabel("")
#     plt.show()


# @register_udf(Config("quantile", OutputType.IMAGE, {View.SUMMARY: Position(0, 0), }))
# def quantile(df_id, col_name):
#     _df = globals()[df_id]
#     if _df[col_name].dtypes not in ["object"]:
#         plt.figure(figsize=(10, 2))
#         sns.boxplot(data=_df, x=col_name, color="#3283FE")
#         plt.xlabel("")
#         plt.ylabel("")
#         plt.show()

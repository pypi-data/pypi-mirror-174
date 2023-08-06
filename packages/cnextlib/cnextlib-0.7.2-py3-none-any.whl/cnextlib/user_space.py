from enum import Enum
import importlib
import logging
from typing import Tuple, List

from .df_updates import DataFrameOp, DataFrameUpdate, get_class_fullname
from .libs.json_serializable import JsonSerializable

from .df_status_hook import DataFrameStatusHook
from . import udf_manager

logging.basicConfig(filename='./cnextlib.log', filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(funcName)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S', level=logging.DEBUG)
log = logging.getLogger(__name__)


class ExecutionMode(Enum):
    EVAL = 0
    EXEC = 1


class ModelInfoDict(JsonSerializable, dict):
    pass


class UserSpace:
    """
    Define the space where user code will be executed. 
    This is encapsulated in a python module so all the imports and variables are separated out from the rest.
    The code is executed on a kernel such as BaseKernel or IPythonKernel
    """

    def __init__(self, tracking_df_types: tuple = (), tracking_model_types: tuple = ()):
        """
        Args:
            df_types (list): a list of interested data frames types which can be either cycai.DataFrame or pandas.DataFrame
        """
        self.tracking_df_types = tracking_df_types
        self.tracking_model_types = tracking_model_types

    def globals(self):
        raise NotImplementedError('Abstract method not implemented.')

    def get_active_dfs(self) -> List[Tuple[str, str, str]]:
        """
        Get a list of data frame with type in `df_types` from `user_space`

        Returns:
            list: list of data frame with the following information (name, id, type)
        """
        user_space = self.globals()
        names = list(user_space)
        df_list: List[Tuple[str, str, str]] = []

        if isinstance(names, list):
            for obj_name in names:
                obj_type = get_class_fullname(type(user_space[obj_name]))
                # log.info(
                #     "Object name: {} - Object type: {} - Tracking: {}".format(obj_name, obj_type, self.tracking_df_types))
                if obj_type in self.tracking_df_types:
                    df_list.append(
                        (obj_name, id(user_space[obj_name]), obj_type))
        log.info(
            "df_list: {}".format(df_list))
        return df_list

    @staticmethod
    def load_class(name):
        components = name.split('.')
        mod = importlib.import_module(components[0])
        if len(components) > 1:
            for comp in components[1:]:
                mod = getattr(mod, comp)
        return mod

    def get_active_models_info(self) -> ModelInfoDict:
        """
        Get a list of model with type in `model_types` from `user_space`

        Returns:
            list: list of data frame with the following information (name, id, type)
        """
        user_space = self.globals()
        names = list(user_space)
        model_dict = ModelInfoDict()  # List[Tuple[str, str, str]] = []
        if isinstance(names, list):
            for obj_name in names:
                obj_type = type(user_space[obj_name])
                for model_type_name in self.tracking_model_types:
                    model_type = self.load_class(model_type_name)
                    log.info('Model types {} {}'.format(
                        model_type_name, model_type))
                    if isinstance(user_space[obj_name], model_type):
                        model_dict[obj_name] = {'name': obj_name, 'id': id(
                            user_space[obj_name]), 'obj_class': get_class_fullname(obj_type), 'base_class': get_class_fullname(model_type)}

        return model_dict

    # @classmethod
    def update_working_df_status(self, df, df_update: DataFrameUpdate, df_op: DataFrameOp):
        DataFrameStatusHook.update_working_df_status(
            df, df_update, df_op, self.get_active_dfs())

    # @classmethod
    def set_dfs_update(self, df_list, df_update: DataFrameUpdate, df_op: DataFrameOp):
        DataFrameStatusHook.set_dfs_update(
            df_list, df_update, df_op, self.get_active_dfs())

    # @classmethod
    def get_active_dfs_status(self) -> dict:
        return DataFrameStatusHook.get_active_dfs_status(self.get_active_dfs())

    @staticmethod
    def get_registered_udfs() -> dict:
        return udf_manager.get_registered_udfs()

    # @classmethod
    def reset_active_dfs_status(self):
        DataFrameStatusHook.reset_active_dfs_status()

    def execute(self, code, exec_mode: ExecutionMode = ExecutionMode.EVAL):
        raise NotImplementedError('Abstract method not implemented.')

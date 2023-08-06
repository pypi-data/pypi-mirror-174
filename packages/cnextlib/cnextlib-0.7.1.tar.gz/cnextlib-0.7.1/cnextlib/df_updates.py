from enum import Enum
import simplejson as json

from .libs.json_serializable import JsonSerializable


class UpdateType(str, Enum):
    add_cols = 'add_cols'
    del_cols = 'del_cols'
    add_rows = 'add_rows'
    del_rows = 'del_rows'
    update_cells = 'update_cells'
    new_index = 'update_index'
    new_df = 'new_df'
    # this is used for users to force an update so the dataframe will be reloaded,
    # used for the type of dataframe that can not automatically track the updates
    forced_update = 'forced_update'
    # `no_update` is introduced to make it easy to update the case where update might be external.
    no_update = 'no_update'
    # Need to improve this.

    def __str__(self):
        return str(self.value)


# running line value used in the case that variable is forced to be updated. see forced_update above
FORCED_UPDATE_RUNNING_LINE = -1


class DataFrameUpdate(JsonSerializable):
    def __init__(self, update_type: UpdateType, updates: list = []):
        self.update_type = update_type
        self.update_content = updates


class DataFrameOp(JsonSerializable):
    def __init__(self, name: str = '', *args, **kwargs):
        """A Dataframe Operation
           Since args and kwargs are only for the record here, we keep it as string
           to avoid json serializable problem with slice
        Args:
            name (str): op's name
            args (_type_): op's args
            kargs (_type_): op's kargs
        """
        self.name = name
        # self.args = str(args)
        # self.kargs = str(kwargs)


def get_class_fullname(klass):
    module = klass.__module__
    if module == 'builtins':
        return klass.__qualname__
    return module + '.' + klass.__qualname__

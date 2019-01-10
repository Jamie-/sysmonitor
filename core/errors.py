class SysmonError(Exception):
    """Generic system error thrown by any code in this project.
    """
    pass


class DataError(SysmonError):
    """Generic data model error.

    Models each have a child class of this specific to the model for data errors.
    """
    pass

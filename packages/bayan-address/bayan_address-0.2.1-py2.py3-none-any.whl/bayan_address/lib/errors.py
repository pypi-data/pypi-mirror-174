class InvalidValue(Exception):
    def __init__(self, err_val):
        super().__init__(f"The value passed {err_val} is an invalid string.")

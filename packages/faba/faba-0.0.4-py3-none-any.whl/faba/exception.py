class FlagError(Exception):
    def __init__(self, flag, msg: str):  # can not import flag type because of circle import
        super().__init__(f'{msg} in flag {flag.name}')


class ParseError(Exception):
    def __init__(self, argument: str, msg: str):
        super().__init__(f'parse [{argument}] failed: {msg}')


class ValueError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)

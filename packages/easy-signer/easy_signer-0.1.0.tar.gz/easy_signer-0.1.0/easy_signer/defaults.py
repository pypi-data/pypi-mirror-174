

_DEFAULT_VARIABLES = {
    "algorithm": "sha256"
}


def set_default_key(key: str):
    _DEFAULT_VARIABLES["key"] = key


def get_default_key() -> str:
    return _DEFAULT_VARIABLES["key"]


def set_default_algorithm(algorithm: str):
    _DEFAULT_VARIABLES["algorithm"] = algorithm


def get_default_algorithm() -> str:
    return _DEFAULT_VARIABLES["algorithm"]

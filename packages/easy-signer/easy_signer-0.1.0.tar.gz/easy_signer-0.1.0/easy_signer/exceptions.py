

class BadSignature(Exception):
    """Signature does not match."""
    pass


class SignatureExpired(BadSignature):
    """Signature timestamp is older than required max_age."""
    pass


class InvalidAlgorithm(ValueError):
    """Algorithm is not supported by hashlib."""
    pass

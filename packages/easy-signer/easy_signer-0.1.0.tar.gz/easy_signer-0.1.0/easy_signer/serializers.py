import orjson


class JSONSerializer:
    """
    Simple wrapper around orjson to be used in signing.dumps and
    signing.loads.
    """
    def dumps(self, obj) -> bytes:
        return orjson.dumps(obj)

    def loads(self, data: bytes):
        return orjson.loads(data)

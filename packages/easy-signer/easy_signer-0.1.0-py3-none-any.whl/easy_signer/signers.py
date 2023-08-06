
import base64
import datetime
import time
import zlib
import re

from easy_signer import baseconv
from easy_signer.crypto import constant_time_compare, salted_hmac
from easy_signer.defaults import get_default_algorithm, get_default_key
from easy_signer.exceptions import BadSignature, SignatureExpired
from easy_signer.serializers import JSONSerializer


_SEP_UNSAFE = re.compile(r'^[A-z0-9-_=]*$')


def b64_encode(s):
    return base64.urlsafe_b64encode(s).strip(b'=')


def b64_decode(s):
    pad = b'=' * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)


def base64_hmac(salt, value, key, algorithm='sha1'):
    return b64_encode(salted_hmac(salt, value, key, algorithm=algorithm).digest()).decode()


def dumps(obj, key=None, salt='django.core.signing', serializer=JSONSerializer, compress=False):
    """
    Return URL-safe, hmac signed base64 compressed JSON string. If key is
    None, use settings.SECRET_KEY instead. The hmac algorithm is the default
    Signer algorithm.

    If compress is True (not the default), check if compressing using zlib can
    save some space. Prepend a '.' to signify compression. This is included
    in the signature, to protect against zip bombs.

    Salt can be used to namespace the hash, so that a signed string is
    only valid for a given namespace. Leaving this at the default
    value or re-using a salt value across different parts of your
    application without good cause is a security risk.

    The serializer is expected to return a bytestring.
    """
    return TimestampSigner(key, salt=salt).sign_object(obj, serializer=serializer, compress=compress)


def loads(s, key=None, salt='django.core.signing', serializer=JSONSerializer, max_age=None):
    """
    Reverse of dumps(), raise BadSignature if signature fails.

    The serializer is expected to accept a bytestring.
    """
    return TimestampSigner(key, salt=salt).unsign_object(s, serializer=serializer, max_age=max_age)


class Signer:

    def __init__(self, key=None, sep=':', salt=None, algorithm=None):
        self.key = key or get_default_key()
        self.sep = sep
        if _SEP_UNSAFE.match(self.sep):
            raise ValueError(
                'Unsafe Signer separator: %r (cannot be empty or consist of '
                'only A-z0-9-_=)' % sep,
            )
        self.salt = salt or '%s.%s' % (self.__class__.__module__, self.__class__.__name__)
        self.algorithm = algorithm or get_default_algorithm()

    def signature(self, value):
        return base64_hmac(self.salt + 'signer', value, self.key, algorithm=self.algorithm)

    def _sign(self, value):
        return '%s%s%s' % (value, self.sep, self.signature(value))

    def _unsign(self, signed_value):
        if self.sep not in signed_value:
            raise BadSignature('No "%s" found in value' % self.sep)
        value, sig = signed_value.rsplit(self.sep, 1)
        if constant_time_compare(sig, self.signature(value)):
            return value
        raise BadSignature('Signature "%s" does not match' % sig)

    def sign(self, value):
        return self._sign(value)

    def unsign(self, signed_value):
        return self._unsign(signed_value)

    def sign_object(self, obj, serializer=JSONSerializer, compress=False):
        """
        Return URL-safe, hmac signed base64 compressed JSON string.

        If compress is True (not the default), check if compressing using zlib
        can save some space. Prepend a '.' to signify compression. This is
        included in the signature, to protect against zip bombs.

        The serializer is expected to return a bytestring.
        """
        data = serializer().dumps(obj)
        # Flag for if it's been compressed or not.
        is_compressed = False

        if compress:
            # Avoid zlib dependency unless compress is being used.
            compressed = zlib.compress(data)
            if len(compressed) < (len(data) - 1):
                data = compressed
                is_compressed = True
        base64d = b64_encode(data).decode()
        if is_compressed:
            base64d = '.' + base64d
        return self._sign(base64d)

    def unsign_object(self, signed_obj, serializer=JSONSerializer, **kwargs):
        # Signer.unsign() returns str but base64 and zlib compression operate
        # on bytes.
        base64d = self._unsign(signed_obj, **kwargs).encode()
        decompress = base64d[:1] == b'.'
        if decompress:
            # It's compressed; uncompress it first.
            base64d = base64d[1:]
        data = b64_decode(base64d)
        if decompress:
            data = zlib.decompress(data)
        return serializer().loads(data)


class TimestampSigner(Signer):

    def timestamp(self):
        return baseconv.base62.encode(int(time.time() * 1000))

    def validate_age(self, timestamp, max_age):
        if max_age is not None:
            if isinstance(max_age, datetime.timedelta):
                max_age = max_age.total_seconds()
            # Check timestamp is not older than max_age
            age = time.time() - timestamp
            if age > max_age:
                raise SignatureExpired(
                    'Signature age %s > %s seconds' % (age, max_age))

    def sign(self, value):
        value = '%s%s%s' % (value, self.sep, self.timestamp())
        return super().sign(value)

    def sign_object(self, obj, serializer=JSONSerializer, compress=False):
        return super().sign_object([obj, time.time()], serializer, compress)

    def unsign(self, value, max_age=None):
        """
        Retrieve original value and check it wasn't signed more
        than max_age seconds ago.
        """
        result = super().unsign(value)
        value, timestamp = result.rsplit(self.sep, 1)
        timestamp = baseconv.base62.decode(timestamp) / 1000
        self.validate_age(timestamp, max_age)
        return value

    def unsign_object(self, signed_obj, max_age=None, serializer=JSONSerializer, **kwargs):
        """
        Retrieve original object and check it wasn't signed more
        than max_age seconds ago.
        """
        result = super().unsign_object(signed_obj, serializer, **kwargs)
        value, timestamp = result
        self.validate_age(timestamp, max_age)
        return value


class EphemeralSigner(Signer):

    def expiration(self, ttl):
        return baseconv.base62.encode(int((time.time() + ttl) * 1000))

    def sign(self, value, ttl=None):
        """Sign the value valid for ttl seconds"""
        if ttl is not None:
            if isinstance(ttl, datetime.timedelta):
                ttl = ttl.total_seconds()
            value = '%s%s%s' % (value, self.sep, self.expiration(ttl))
        return super().sign(value)

    def sign_object(self, obj, ttl, serializer=JSONSerializer, compress=False):
        """Sign the object valid for ttl seconds"""
        if isinstance(ttl, datetime.timedelta):
            ttl = ttl.total_seconds()
        return super().sign_object([obj, time.time() + ttl], serializer, compress)

    def unsign(self, value):
        """
        Retrieve original value and check it hasn't expired.
        """
        result = super().unsign(value)
        value, expiration = result.rsplit(self.sep, 1)
        expiration = baseconv.base62.decode(expiration) / 1000
        # Check expiration is in the future
        if time.time() >= expiration:
            raise SignatureExpired(
                'Signature expired %s seconds ago' % (time.time() - expiration))
        return value

    def unsign_object(self, signed_obj, serializer=JSONSerializer, **kwargs):
        """
        Retrieve original object and check it hasn't expired.
        """
        result = super().unsign_object(signed_obj, serializer, **kwargs)
        value, expiration = result
        if time.time() >= expiration:
            raise SignatureExpired(
                'Signature expired %s seconds ago' % (time.time() - expiration))
        return value

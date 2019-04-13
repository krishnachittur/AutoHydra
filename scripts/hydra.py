from enum import Enum, auto

class Exploit(Enum):
    """A type of supported Hydra exploit."""
    SSH = auto()
    HTTPAUTH = auto()
    POSTGRES = auto()
    LDAP = auto()

from enum import IntEnum


class CertType(IntEnum):
    windows = 0
    linux = 1
    macos = 2
    ios = 3
    android = 4

    def get_suffix(self):
        if self == CertType.windows:
            return "p12"
        if self in (CertType.linux, CertType.macos, CertType.ios):
            return "pem"
        if self == CertType.android:
            return "cer"
        raise Exception("unsupported cert type")

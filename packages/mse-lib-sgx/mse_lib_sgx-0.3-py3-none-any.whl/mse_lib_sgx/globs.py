"""mse_lib_sgx.global module."""

import threading
from typing import Optional, Union

from mse_lib_sgx.certificate import SelfSignedCertificate, SGXCertificate

CERT: Union[SGXCertificate, SelfSignedCertificate, None] = None
SEALED_KEY: Optional[bytes] = None
EXIT_EVENT: threading.Event = threading.Event()

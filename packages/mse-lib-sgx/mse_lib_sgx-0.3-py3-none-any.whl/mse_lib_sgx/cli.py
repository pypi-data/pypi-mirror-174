"""mse_lib_sgx.cli module."""

import argparse
import asyncio
import importlib
import os
import sys
from pathlib import Path

from cryptography import x509
from cryptography.x509.oid import NameOID
from hypercorn.asyncio import serve
from hypercorn.config import Config

from mse_lib_sgx import globs
from mse_lib_sgx.certificate import SelfSignedCertificate, SGXCertificate
from mse_lib_sgx.http_server import serve as serve_sgx_unseal
from mse_lib_sgx.import_hook import import_set_key


def parse_args() -> argparse.Namespace:
    """Argument parser."""
    parser = argparse.ArgumentParser(description="Start a MSE Enclave server.")
    parser.add_argument(
        "application",
        type=str,
        help="Application to dispatch to as path.to.module:instance.path")
    parser.add_argument("--encrypted-code",
                        action="store_true",
                        default=False,
                        help="Whether the application is encrypted")
    parser.add_argument("--lifetime",
                        type=int,
                        required=True,
                        help="Time (in month) before certificate expired")
    parser.add_argument("--host",
                        required=True,
                        type=str,
                        help="Hostname of the server")
    parser.add_argument("--port",
                        required=True,
                        type=int,
                        help="Port of the server")
    parser.add_argument("--app-dir",
                        required=True,
                        type=Path,
                        help="Path the microservice application")
    parser.add_argument(
        "--data-dir",
        required=True,
        type=Path,
        help="Path with data encrypted for a specific MRENCLAVE")
    parser.add_argument("--debug",
                        action="store_true",
                        help="Debug mode without SGX")

    return parser.parse_args()


def run():
    """Entrypoint of the CLI."""
    args: argparse.Namespace = parse_args()
    os.makedirs(args.data_dir, exist_ok=True)

    subject: x509.Name = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "FR"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Ile-de-France"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Paris"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Cosmian Tech"),
        x509.NameAttribute(NameOID.COMMON_NAME, "cosmian.com"),
    ])

    cert: SGXCertificate = (SGXCertificate(
        dns_name=args.host,
        subject=subject,
        root_path=Path(args.data_dir),
    ) if not args.debug else SelfSignedCertificate(
        dns_name=args.host, subject=subject, root_path=Path(args.data_dir)))

    if args.encrypted_code:
        serve_sgx_unseal(hostname="0.0.0.0", port=args.port, certificate=cert)
        import_set_key(globs.SEALED_KEY)

    config = Config.from_mapping({
        "bind": f"0.0.0.0:{args.port}",
        "keyfile": cert.key_path,
        "certfile": cert.cert_path,
        "alpn_protocols": ["h2"],
        "workers": 1
    })

    sys.path.append(f"{args.app_dir.resolve()}")
    module, app = args.application.split(":")
    app = getattr(importlib.import_module(module), app)

    asyncio.run(serve(app, config))

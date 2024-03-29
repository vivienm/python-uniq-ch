from typing import Any, Dict

from setuptools_rust import RustExtension

rust_extensions = [
    RustExtension(
        "uniq_ch_rust",
        "src/uniq_ch_rust/Cargo.toml",
    ),
]


def build(setup_kwargs: Dict[str, Any]) -> None:
    setup_kwargs.update(rust_extensions=rust_extensions)
    setup_kwargs.update(rust_extensions=rust_extensions)

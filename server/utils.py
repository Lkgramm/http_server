import os
import mimetypes


def get_file_path(requested_path: str, document_root: str) -> str:
    if requested_path == "/":
        requested_path = "/index.html"
    return os.path.join(document_root, requested_path.lstrip("/"))


def file_exists(file_path: str) -> bool:
    return os.path.exists(file_path) and os.path.isfile(file_path)


def guess_mime_type(file_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or "application/octet-stream"

import os
from typing import Dict, Tuple

import mimetypes

FileTypeVideo = "video"
FileTypeImage = "image"
FileTypeZip = "zip"
FileTypeDoc = "doc"
FileTypeAttachment = "attachment"

UPLOAD_FILE_TYPE: Dict[str, str] = {
    "jpg": FileTypeImage,
    "jpeg": FileTypeImage,
    "png": FileTypeImage,
    "gif": FileTypeImage,
    "npy": FileTypeImage,
    "mp4": FileTypeVideo,
    "avi": FileTypeVideo,
    "mpg": FileTypeVideo,
    "mpeg": FileTypeVideo,
    "3gp": FileTypeVideo,
    "mov": FileTypeVideo,
    "m4v": FileTypeVideo,
    "dat": FileTypeVideo,
    "mkv": FileTypeVideo,
    "flv": FileTypeVideo,
    "vob": FileTypeVideo,
    "dav": FileTypeVideo,
    "ts": FileTypeVideo,
    "md": FileTypeVideo,
    "h264": FileTypeVideo,
    "h265": FileTypeVideo,
    "zip": FileTypeZip,
    "gz": FileTypeZip,
    "tar": FileTypeZip,
    "rar": FileTypeZip,
    "bz2": FileTypeZip,
    "csv": FileTypeDoc,
    "json": FileTypeDoc,
    "pdf": FileTypeDoc,
    "txt": FileTypeDoc,
    "xml": FileTypeDoc,
}


def get_file_type(file_path: str) -> Tuple[str, str]:
    file_type = mimetypes.guess_type(file_path)[0]
    if not file_type:
        file_type = "application/octet-stream"

    name = os.path.basename(file_type)
    if name in UPLOAD_FILE_TYPE:
        upload_file_type = UPLOAD_FILE_TYPE[name]
    else:
        upload_file_type = FileTypeAttachment

    return file_type, upload_file_type

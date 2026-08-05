"""OSS 对象命名规则。"""


def build_object_key(file_id: str, file_size: int) -> str:
    """按不可变内容身份生成 OSS key。"""
    normalized_id = file_id.lower()
    return f"{normalized_id[:4]}/{normalized_id[4:]}-{file_size}"

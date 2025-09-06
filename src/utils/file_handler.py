def read_file_utf8(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_file_utf8(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
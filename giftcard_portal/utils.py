def display(name: str) -> str:
    return name if len(name) <= 30 else f"{name[:27]}..."

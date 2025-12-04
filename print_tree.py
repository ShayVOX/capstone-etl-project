import os

SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".idea",
    ".vscode",
    ".mypy_cache",
    ".pytest_cache",
}

def print_tree(start_path=".", indent=""):
    for item in sorted(os.listdir(start_path)):
        full_path = os.path.join(start_path, item)

        if os.path.isdir(full_path) and item in SKIP_DIRS:
            continue

        print(f"{indent}{item}")

        if os.path.isdir(full_path):
            print_tree(full_path, indent + "  ")

if __name__ == "__main__":
    print("\nPROJECT TREE:\n")
    print_tree(".")

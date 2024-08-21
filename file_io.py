from typing import List

in_file_path = ''
out_file_path = ''


def create_out_file() -> None:
    with open(out_file_path, 'w'):
        pass


def read_all_from_in() -> str:
    with open(in_file_path, 'r') as f:
        return f.read()


def read_lines_from_input() -> List[str]:
    with open(in_file_path, 'r') as f:
        lines = f.read().strip().split('\n')

    new_lines = []
    for line in lines:
        line = line.strip()
        if line:
            new_lines.append(line)

    return new_lines


def append_to_out(text: str) -> None:
    with open(out_file_path, 'a') as f:
        f.write(text)
        f.write('\n')

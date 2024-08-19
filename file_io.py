in_file_path = ''
out_file_path = ''


def create_out_file():
    with open(out_file_path, 'w') as f:
        pass


def read_all_from_in():
    with open(in_file_path, 'r') as f:
        return f.read()

def read_lines_from_in():
    with open(in_file_path, 'r') as f:
        lines = f.read().strip().split('\n')
    
    new_lines = []
    for line in lines:
        if line:
            new_lines.append(line)
    
    return new_lines

def append_to_out(text: str):
    with open(out_file_path, 'a') as f:
        f.write(text)
        f.write('\n')

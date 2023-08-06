from uuid import uuid4

from .config import Config
from .get_tsxs import get_tsxs


def mark(dir='.'):
    for file_name in get_tsxs(dir):
        print(file_name)
        with open(file_name) as file:
            file_body = file.read()

        for tag in Config.TAGS:
            idx = 0
            while (idx := file_body.find('<' + tag, idx + 1)) != -1:
                uuid = uuid4()
                next_word = file_body[idx + 1 + len(tag):idx + 1 + len(tag) + 5]
                next_symbol = file_body[idx + 1 + len(tag):idx + 1 + len(tag) + 1]
                if next_word != f' {Config.ATTR}' and (next_symbol == ' ' or next_symbol == '\n'):
                    file_body = file_body[:idx + 1 + len(tag)] + f' {Config.ATTR}="{uuid}" ' + file_body[idx + 1 + len(tag):]

        # Write the file out again
        with open(file_name, 'w') as file:
            file.write(file_body)

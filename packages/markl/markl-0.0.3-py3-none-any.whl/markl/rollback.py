from .config import Config
from .get_tsxs import get_tsxs
from uuid import uuid4

def rollback(dir='.'):
    for file_name in get_tsxs(dir):
        print(file_name)
        with open(file_name) as file:
            file_body = file.read()

        for tag in Config.TAGS:
            idx = 0
            while (idx := file_body.find('<' + tag + f' {Config.ATTR}=', idx + 1)) != -1:
                mark_start = idx + 1 + len(tag)
                mark_end = idx + 1 + len(tag) + len(Config.ATTR) \
                           + len('="') + len(str(uuid4())) + len('" ') + 1
                file_body = file_body[:mark_start] + file_body[mark_end:]

        with open(file_name, 'w') as file:
            file.write(file_body)

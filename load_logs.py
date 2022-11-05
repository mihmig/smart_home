# Парсинг логов сервиса zigbe2mqtt (только срабатывания датчиков)
# https://docs.python.org/3/howto/regex.html
import glob
import re

p = re.compile(
    "^.+(?P<timestamp>[\d \-\:]{19,19}).+'zigbee2mqtt/(?P<device_id>0x([\da-f]+))', payload '(?P<payload>.+)'\n",
    re.IGNORECASE)


def process_log_file(log_file_name: str):
    lines_readed = 0
    lines_parsed = 0
    log_file = open(log_file_name, mode="r", encoding="utf-8")
    while True:
        line = log_file.readline()
        if not line:
            break
        lines_readed += 1
        if line == '\n' or line == ' \n' or 'tamper' not in line or 'payload' not in line:
            continue
        res = p.match(line)
        if not (res is None):
            print(res.group('device_id'), res.group('payload'))
            lines_parsed += 1
    print(f'Parsed lines {lines_parsed} from {lines_readed}')


INPUT_PATH = "./data/log/*/*.txt"
log_files = glob.glob(INPUT_PATH)
part = 0
for i, file in enumerate(log_files):
    print(f'Process file: {file} ({i} from {len(log_files)})')
    process_log_file(file)

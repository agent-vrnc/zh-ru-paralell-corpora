import re
import csv

# файлы со ссылками
RU_FILE = 'ru_links_interview.txt'
ZH_FILE = 'zh_links_interview.txt'

OUTPUT_FILE = 'matched_links_interview.csv'


def load_links(filename):
    """Читает ссылки и удаляет дубли"""
    with open(filename, 'r', encoding='utf-8') as f:
        return sorted(set(
            line.strip()
            for line in f
            if line.strip()
        ))


def extract_date(url):
    """
    Извлекает дату вида 20260430 из URL
    """
    match = re.search(r't(\d{8})_', url)

    if match:
        return match.group(1)

    return None


# загружаем ссылки
ru_links = load_links(RU_FILE)
zh_links = load_links(ZH_FILE)

# словари: дата -> ссылка
ru_dict = {}
zh_dict = {}

for link in ru_links:

    date = extract_date(link)

    if date:
        ru_dict[date] = link


for link in zh_links:

    date = extract_date(link)

    if date:
        zh_dict[date] = link


# все даты
all_dates = sorted(set(ru_dict.keys()) | set(zh_dict.keys()))

# записываем CSV
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as f:

    writer = csv.writer(f)

    writer.writerow(['date', 'ru_link', 'zh_link'])

    for date in all_dates:

        writer.writerow([
            date,
            ru_dict.get(date, ''),
            zh_dict.get(date, '')
        ])

print(f'Готово: {OUTPUT_FILE}')
print(f'RU ссылок: {len(ru_links)}')
print(f'ZH ссылок: {len(zh_links)}')
print(f'Совпадений по дате: {len(all_dates)}')
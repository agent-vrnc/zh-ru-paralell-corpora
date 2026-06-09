from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import urljoin
import time

options = webdriver.ChromeOptions()

# ускоряет работу
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# главное:
options.page_load_strategy = 'eager'

driver = webdriver.Chrome(options=options)

sites = {
    'ru': 'https://vladivostok.china-consulate.gov.cn/rus/zlgdt_2/',
    'zh': 'https://vladivostok.china-consulate.gov.cn/chn/zlgdt/'
}

MAX_PAGES = 10

for lang, base_url in sites.items():

    links = set()

    for page in range(1, MAX_PAGES + 1):

        if page == 1:
            url = base_url
        else:
            url = urljoin(base_url, f'index_{page}.htm')

        print(f'\nОткрываем: {url}')

        try:

            # timeout страницы
            driver.set_page_load_timeout(15)

            driver.get(url)

            # ждём появления ссылок
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.title_list a')
                )
            )

        except TimeoutException:

            print('Timeout страницы')
            continue

        except Exception as e:

            print('Ошибка:', e)
            continue

        articles = driver.find_elements(
            By.CSS_SELECTOR,
            '.title_list a'
        )

        page_links = 0

        for a in articles:

            href = a.get_attribute('href')

            if href and href.endswith('.htm'):

                links.add(href)
                page_links += 1

                print(href)

        if page_links == 0:

            print(f'{lang}: ссылок нет')
            break

        print(f'{lang}: страница {page}, ссылок: {page_links}')

        time.sleep(1)

    # сохраняем
    with open(
        f'{lang}_links_interview_vld.txt',
        'w',
        encoding='utf-8'
    ) as f:

        for link in sorted(links):
            f.write(link + '\n')

    print(f'\n{lang}: сохранено {len(links)} ссылок')

driver.quit()
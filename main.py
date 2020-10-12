import base64
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_pdf_from_html(path, chromedriver='/opt/chromedriver/chromedriver'):
    # запускаем Chrome
    webdriver_options = Options()
    webdriver_options.add_argument('--headless')
    webdriver_options.add_argument('--disable-gpu')
    webdriver_options.add_argument('--remote-debugging-address=0.0.0.0')
    # webdriver_options.add_argument('--run-all-compositor-stages-before-draw')
    # webdriver_options.add_argument('--virtual-time-budget=1000')
    webdriver_options.add_argument('--remote-debugging-port=9222')

    # For Docker https://stackoverflow.com/questions/53902507/unknown-error-session-deleted-because-of-page-crash-from-unknown-error-cannot
    webdriver_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(chromedriver, options=webdriver_options)

    # открываем заданный url
    # driver.set_page_load_timeout(30)
    # driver.get(path)

    driver.execute_cdp_cmd("Page.navigate", cmd_args={'url': path})
    # import pdb
    # pdb.set_trace()

    calculated_print_options = {
        # 'landscape': False,
        # 'headerTemplate': '''
        #     <span class=url>11</span>
        #     <span class=pageNumber>11</span>
        # ''',
        # 'footerTemplate': '''
        #     <span class="title">11</span>
        #     <span class="pageNumber">11</span>
        # ''',
        # 'paperWidth': '1000px',
        # 'marginTop': 0,
        # 'marginBottom': 0,
        # 'marginLeft': 0,
        # 'marginRight': 0,
        'pageRanges': '1',
        'displayHeaderFooter': True,
        'printBackground': True,
        'preferCSSPageSize': True,
    }

    result = driver.execute_cdp_cmd("Page.printToPDF", calculated_print_options)
    driver.quit()
    return base64.b64decode(result['data'])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: converter.py <html_page_sourse> <filename_to_save>")
        exit()

    result = get_pdf_from_html(sys.argv[1])
    with open(sys.argv[2], 'wb') as file:
        file.write(result)

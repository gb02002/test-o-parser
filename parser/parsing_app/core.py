import re
from selenium.common import WebDriverException, NoSuchElementException
from parsing_app import db_population

from parser.settings import PARSING_PATH
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


def setUp():
    """Setting up driver with headers"""
    options = webdriver.ChromeOptions()

    try:
        driver = uc.Chrome(options=options)
        driver.get(PARSING_PATH)
        return driver
    except WebDriverException as e:
        print("Произошла ошибка при инициализации драйвера:", e)
        return None
    except Exception as e:
        # Обработка других неожиданных ошибок
        print("Произошла неожиданная ошибка:", e)
        return None


def establish_connection(driver):
    """Waiting to load full page"""
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="layoutPage"]/div[1]/div[3]/div/div[1]/div[1]/div[2]/div[1]/span')))
    WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element(
        (By.XPATH, '//*[@id="layoutPage"]/div[1]/div[3]/div/div[1]/div[1]/div[2]/div[1]/span'), "Proffi"))


def main_logic(products_counts=10):
    """Main script"""
    try:
        print(products_counts)
        driver = setUp()
        establish_connection(driver=driver)

        needed_links = [i.get_attribute('href') for i in driver.find_elements(By.XPATH, "//div[@class='iy6 iy7 "
                                                                                        "tile-root']/div/div/a")[
                                                         :products_counts]]
        success = scraping(driver=driver, links=needed_links)
        if success:
            return "SUCCESS"
        else:
            return "ERROR"
    except Exception as e:
        print("Произошла ошибка:", e)
        return "ERROR"
    finally:
        try:
            if driver is not None:
                driver.quit()
        except Exception:
            return "ERROR"


def scraping(driver, links: list) -> bool:
    """Gets links, parses data from them and saves data"""

    max_errors = 2
    error_count = 0
    success = True

    for link in links:
        try:
            driver.get(link)
            product_data = parse_info(driver)
            save_to_db(product_data)
        except Exception as e:
            print(f"Ошибка при обработке ссылки {link}: {e}")
            error_count += 1
            if error_count >= max_errors:
                print("Превышено максимальное количество ошибок. Возвращаем FAIL.")
                success = False
                break

    return success


def parse_info(driver) -> dict | None:
    """Parses product_data and returns it"""
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="section-description"]/div[2]/div/div/div'))
    )

    try:
        name = driver.find_element(By.XPATH,
                                   '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[1]/div[1]/div[2]/div/div[1]/h1').text
        price = driver.find_element(By.XPATH,
                                        '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div[1]/div[2]/div/div['
                                        '1]/div/div/div[1]/div[2]/div/div[1]/span[2]').text[:-2]
        price = extract_discount_from_element(price)
        image_url = ""
        try:
            image_url = driver.find_element(By.XPATH,
                                            '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[1]/div[1]/div['
                                            '1]/div/div/div/div/div/div[2]/div[1]/div/img').get_attribute('src')
        except NoSuchElementException:
            try:
                image_url = driver.find_element(By.XPATH,
                                                '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[1]/div[1]/div['
                                                '1]/div/div/div/div/div/div[2]/div[1]/div/div[1]').get_attribute('src')
            except NoSuchElementException:
                try:
                    image_url = driver.find_element(By.XPATH,
                                                    '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[1]/div[1]/div['
                                                    '1]/div/div/div/div/div/div/div[1]/div').get_attribute('src')
                except NoSuchElementException:
                    pass
        finally:
            if not image_url:
                image_url = ""

        discount = driver.find_element(By.XPATH, '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div[1]/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[1]/span[1]').text[:-2]
        discount = extract_discount_from_element(discount)
        description = driver.find_element(By.XPATH, '//*[@id="section-description"]/div[2]/div/div/div').text

    except NoSuchElementException:
        return None

    product_data = {
        "name": name,
        "price": price,
        "description": description,
        "image_url": image_url,
        "discount": discount
    }

    return product_data


def save_to_db(product_data: dict | None):
    if product_data:
        db_population.populate_db(product_data)


def extract_discount_from_element(str):
    # Очистка строки от пробелов и неразрывных пробелов
    cleaned_str = str.replace('\u2009', '').replace('\u202F', '').replace(' ', '')

    # Проверка, состоит ли очищенная строка только из цифр
    if cleaned_str.isdigit():
        return int(cleaned_str)

    # Если строка не состоит только из цифр, ищем числовое значение перед символом '₽'
    match = re.search(r'(\d[\d\s]*)\s*', cleaned_str)
    if match:
        # Удаляем все пробелы из числа
        clean_str = match.group(1).replace('\u2009', '').replace('\u202F', '').replace(' ', '')
        return int(clean_str)

    return 0


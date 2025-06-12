from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait

from celery import shared_task


@shared_task
def get_jobes():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Firefox(options=options)
    driver.get("https://jobinja.ir/jobs")

    wait = WebDriverWait(driver, 10)

    try:
        category_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.c-jobSearchTop__block:nth-child(3)")
            )
        )
        category_button.click()
        category_option = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[contains(text(), 'برنامه‌نویسی')]")
            )
        )
        category_option.click()

        search_elem = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )

        old_text = driver.find_element(
            By.CLASS_NAME, "c-jobSearchState__numberOfResults"
        ).text
        search_elem.click()
        wait.until(
            lambda d: d.find_element(
                By.CLASS_NAME, "c-jobSearchState__numberOfResults"
            ).text
            != old_text
        )

        jobs = wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//li[contains(@class, 'o-listView__item') and contains(@class, 'c-jobListView__item')]",
                )
            )
        )
        for job in jobs:
            html = job.get_attribute("innerHTML")
            print(html)
            print("-----------------------------------------------------")

    finally:
        driver.quit()

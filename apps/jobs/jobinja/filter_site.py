from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812


def filter_jobs(driver, wait):
    driver.get("https://jobinja.ir/jobs")
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "div.c-jobSearchTop__block:nth-child(3)")
        )
    ).click()
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'برنامه‌نویسی')]"))
    ).click()

    search_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    old_text = driver.find_element(
        By.CLASS_NAME, "c-jobSearchState__numberOfResults"
    ).text
    search_btn.click()
    wait.until(
        lambda d: d.find_element(
            By.CLASS_NAME, "c-jobSearchState__numberOfResults"
        ).text
        != old_text
    )

    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".c-jobSearchState__sortSelect"))
    ).click()
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".c-jobSearchState__sortSelect > option:nth-child(2)")
        )
    ).click()
    sleep(3)

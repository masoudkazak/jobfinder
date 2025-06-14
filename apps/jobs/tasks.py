from time import sleep

from bs4 import BeautifulSoup
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait
from utils.text_clean import clean_text

from celery import shared_task


def login(driver, wait, email, password):
    driver.get("https://jobinja.ir/login/user")
    wait.until(EC.presence_of_element_located((By.NAME, "identifier"))).send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "input.c-btn").click()
    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".c-nav2AccountManager__toggleLabel")
            )
        )
        print("✅ ورود موفق بود")
        return True
    except Exception as e:
        print(f"❌ ورود ناموفق بود: {e}")
        return False


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


def get_today_job_links(driver, wait):
    jobs = wait.until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                "//li[contains(@class, 'o-listView__item') and contains(@class, 'c-jobListView__item')]",
            )
        )
    )

    links = []
    for job in jobs:
        try:
            html = job.get_attribute("innerHTML")
            soup = BeautifulSoup(html, "html.parser")
            url = soup.find("a", class_="c-jobListView__titleLink")["href"]
            passed_days = soup.find("span", class_="c-jobListView__passedDays")
            if passed_days and "امروز" in passed_days.text:
                links.append(url)
            else:
                break
        except Exception as e:
            print(f"❌ خطا در لینک: {e}")
    return links


def parse_info_box(soup, class_name):
    result = {}
    box = soup.find("ul", class_=class_name)
    if not box:
        return result
    for item in box.find_all("li", class_="c-infoBox__item"):
        title_tag = item.find("h4", class_="c-infoBox__itemTitle")
        if not title_tag:
            continue
        title_text = clean_text(title_tag.text)
        values = [
            clean_text(span.text) for span in item.find_all("span", class_="black")
        ]
        result[title_text] = values
    return result


def extract_job_details(driver, wait, url):
    try:
        driver.get(url)
        job_elem = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".c-jobView"))
        )
        soup = BeautifulSoup(job_elem.get_attribute("innerHTML"), "html.parser")

        title = soup.select_one("div.c-jobView__titleText h1").get_text(strip=True)
        first_info = parse_info_box(soup, "c-jobView__firstInfoBox")
        second_info = parse_info_box(soup, "c-infoBox u-mB0")
        body = "".join(
            clean_text(div.text) for div in soup.find_all("div", class_="o-box__text")
        )

        print(f"{title}\n{first_info}\n{second_info}\n{body}")
        print("------------------------------------------------------")
    except Exception as e:
        print(f"❌ خطا در جزئیات {url}: {e}")


@shared_task
def jobinja_scraper_task():
    email = config("JOBINJA_EMAIL")
    password = config("JOBINJA_PASSWORD")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        if not login(driver, wait, email, password):
            return

        filter_jobs(driver, wait)
        job_links = get_today_job_links(driver, wait)

        for link in job_links:
            extract_job_details(driver, wait, link)

    finally:
        driver.quit()

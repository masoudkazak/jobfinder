from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812


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

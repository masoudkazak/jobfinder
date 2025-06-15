from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from apps.jobs.jobinja.extract_data import extract_job_details
from apps.jobs.jobinja.filter_site import filter_jobs
from apps.jobs.jobinja.login import login
from apps.jobs.jobinja.urls_jobs import get_today_job_links
from celery import shared_task

from .models import JobPosting


@shared_task
def jobinja_scraper_task():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 10)
    data = list()
    try:
        if not login(driver, wait):
            return

        filter_jobs(driver, wait)
        job_links = get_today_job_links(driver, wait)
        data = [
            JobPosting(**extract_job_details(driver, wait, link)) for link in job_links
        ]

    finally:
        driver.quit()
    JobPosting.objects.bulk_create(data, ignore_conflicts=True)

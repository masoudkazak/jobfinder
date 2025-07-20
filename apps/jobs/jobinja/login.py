import logging

from decouple import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812

logger = logging.getLogger(__name__)


def login(driver, wait):
    email = config("JOBINJA_EMAIL")
    password = config("JOBINJA_PASSWORD")
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
        logger.info("✅ ورود موفق بود")
        return True
    except Exception as e:
        logger.error(f"❌ ورود ناموفق بود: {e}")
        return False

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from utils.text_clean import clean_text

from apps.core.models import Province
from apps.jobs.jobinja.job_posting_converter import (
    job_type_mapping,
    persian_english_number,
    seniority_level_mapping,
)


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


def extract_salary(salary_field):
    if not salary_field or salary_field[0] == "توافقی":
        return "negotiable", None
    elif salary_field[0] == "حقوق پایه (وزارت کار)":
        return "fixed", "حقوق پایه (وزارت کار)"
    return "fixed", persian_english_number(salary_field[0])


def extract_military(value):
    pass


def extract_province(province):
    return Province.objects.filter(name=province).first()


def extract_job_details(driver, wait, url):
    try:
        driver.get(url)

        comapny_elem = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".c-companyHeader__info"))
        )
        soup = BeautifulSoup(comapny_elem.get_attribute("innerHTML"), "html.parser")
        company = soup.find("h2", class_="c-companyHeader__name")
        full_company = company.get_text(strip=True)
        company_list = [
            part.strip() for part in full_company.split("|") if part.strip()
        ]

        job_elem = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".c-jobView"))
        )
        soup = BeautifulSoup(job_elem.get_attribute("innerHTML"), "html.parser")

        title = clean_text(
            soup.select_one("div.c-jobView__titleText h1").get_text(strip=True)
        )
        first_info = parse_info_box(soup, "c-jobView__firstInfoBox")
        second_info = parse_info_box(soup, "c-infoBox u-mB0")

        job_types = first_info.get("نوع همکاری", [])
        is_remote = "دورکاری" in job_types
        if is_remote:
            job_types.remove("دورکاری")
        salary_type, salary = extract_salary(first_info.get("حقوق", []))
        base_salary = True if salary == "حقوق پایه (وزارت کار)" else False
        province = extract_province(
            first_info.get("موقعیت مکانی", [""])[0].split("،")[0].strip()
        )
        raw_military_status = second_info.get("وضعیت نظام وظیفه", [])
        military_status = []
        if isinstance(raw_military_status, list):
            military_status = [str(item) for item in raw_military_status if item]

        data = {
            "title": title,
            "company_persian": company_list[0] if len(company_list) > 0 else None,
            "company_english": company_list[1] if len(company_list) > 1 else None,
            "province": province,
            "is_remote": is_remote,
            "description": "".join(
                clean_text(div.text)
                for div in soup.find_all("div", class_="o-box__text")
            ),
            "url": url,
            "job_type": job_type_mapping[job_types[0]],
            "seniority_level": [
                seniority_level_mapping[key]
                for key in seniority_level_mapping
                if key in title
            ],
            "salary_type": salary_type,
            "base_salary": base_salary,
            "salary": salary if not salary else None,
            "source": "Jobinja",
            "skills": second_info.get("مهارت های مورد نیاز", []),
            "military_status": military_status,
        }
        return data

    except Exception as e:
        print(f"❌ خطا در جزئیات {url}: {e}")

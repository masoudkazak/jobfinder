job_type_mapping = {
    "تمام وقت": "full_time",
    "پاره وقت": "part_time",
    "قراردادی": "contract",
    "کارآموزی": "internship",
}

seniority_level_mapping = {
    "کارآموز": "intern",
    "Senior": "senior",
    "Junior": "junior",
    "Mid-Level": "mid",
    "Team Lead": "lead",
}


def persian_english_number(number: str):
    persian_to_english = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
    english_number = number.split()[1].translate(persian_to_english)
    english_number = int(english_number.replace(",", ""))
    return english_number

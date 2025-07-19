def format_profile(filters: dict) -> str:  # noqa: C901
    lines = ["🔎فیلترهای جستجوی شما:\n"]

    if filters.get("title"):
        lines.append(f"📌 عنوان شغلی: {filters['title']}")

    if filters.get("job_types"):
        job_types = ", ".join(
            map(
                lambda x: {
                    "full_time": "تمام‌وقت",
                    "part_time": "پاره‌وقت",
                    "contract": "پروژه‌ای",
                    "internship": "کارآموزی",
                }.get(x, x),
                filters["job_types"],
            )
        )
        lines.append(f"🧩 نوع همکاری: {job_types}")

    if filters.get("seniorities"):
        levels = ", ".join(
            map(
                lambda x: {"junior": "جونیور", "mid": "میدل", "senior": "سینیور"}.get(
                    x, x
                ),
                filters["seniorities"],
            )
        )
        lines.append(f"📈 سطح ارشدیت: {levels}")

    if filters.get("province"):
        provinces = ", ".join(filters["province"])
        lines.append(f"🗺️ استان‌ها: {provinces}")

    if filters.get("remote_only") is True:
        lines.append("🏠 امکان دورکاری: دارد")
    elif filters.get("remote_only") is False:
        lines.append("🏢 امکان دورکاری: ندارد")

    if filters.get("salary_type"):
        types = {"negotiable": "توافقی", "fixed": "ثابت"}
        lines.append(
            f"💰 نوع حقوق: {types.get(filters['salary_type'], filters['salary_type'])}"
        )

    if filters.get("min_salary") is not None:
        lines.append(f"📉 حداقل حقوق: {filters['min_salary']:,} تومان")

    if filters.get("max_salary") is not None:
        lines.append(f"📈 حداکثر حقوق: {filters['max_salary']:,} تومان")

    if filters.get("skills"):
        skills = ", ".join(filters["skills"])
        lines.append(f"🛠️ مهارت‌ها: {skills}")

    return "\n".join(lines)


def format_job(job: dict) -> str:
    if not isinstance(job, dict):
        return "❌ خطا: ورودی باید یک دیکشنری باشد."

    title = job.get("title", "نامشخص")
    company = job.get("company_persian") or job.get("company_english") or "نامشخص"
    job_type = {
        "full_time": "تمام‌وقت",
        "part_time": "پاره‌وقت",
        "contract": "پروژه‌ای",
        "internship": "کارآموزی",
    }.get(job.get("job_type"), "نامشخص")

    seniority = (
        ", ".join(
            {"junior": "جونیور", "mid": "میدل", "senior": "سینیور"}.get(level, level)
            for level in job.get("seniority_level", [])
        )
        or "نامشخص"
    )

    province = job.get("province", "نامشخص")

    salary_type = {"negotiable": "توافقی", "fixed": "ثابت"}.get(
        job.get("salary_type"), "نامشخص"
    )
    base_salary = job.get("base_salary", False)
    salary_amount = f"{job.get('salary'):,} تومان" if job.get("salary") else ""
    if salary_type == "توافقی" and not base_salary:
        salary_display = f"{salary_type}".strip()
    elif salary_type == "توافقی" and base_salary:
        salary_display = "حقوق پایه وزارت کار"
    else:
        salary_display = f"{salary_amount}".strip()

    skills = ", ".join(job.get("skills", [])) if job.get("skills") else "ندارد"
    is_remote = "بله ✅" if job.get("is_remote") else "خیر ❌"

    description = job.get("description", "")
    description_summary = description[:200].strip() + (
        "..." if len(description) > 200 else ""
    )

    url = job.get("url", "ندارد")
    source = job.get("source", "نامشخص")
    military_status = (
        ", ".join(job.get("military_status", []))
        if job.get("military_status")
        else "مهم نیست"
    )

    return f"""📋 عنوان شغلی: {title}
🏢 شرکت: {company}
🧩 نوع همکاری: {job_type}
📈 سطح ارشدیت: {seniority}
🗺️ استان: {province}
💰 حقوق: {salary_display}
🛠️ مهارت‌ها: {skills}
🏠 دورکاری: {is_remote}
🪖 وضعیت نظام‌وظیفه: {military_status}
📡 منبع انتشار: {source}
📝 توضیحات: {description_summary}
🔗 لینک: <a href="{url}">مشاهده</a>
"""

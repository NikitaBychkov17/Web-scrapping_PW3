import requests
import bs4
import json
import re

if __name__ == "__main__":
    url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
    fake_ua = {
        "user-agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; Touch)"
    }
    res = requests.get(url=url, headers=fake_ua)
    soup = bs4.BeautifulSoup(res.text, "lxml")

    result = []
    for item in soup.find_all("div", class_="vacancy-serp-item__layout"):
        title_item = item.find("span", {"data-qa": "serp-item__title-text"})
        title = title_item.text if title_item else ""
        print(f"Title: {title}")  # Отладка

        salary_item = item.find("span", class_="magritte-text_style-primary___AQ7MW_3-0-20")
        salary = salary_item.text.replace("\u202f", "") if salary_item else ""
        print(f"Salary: {salary}")  # Отладка

        company_item = item.find("span", {"data-qa": "vacancy-serp__vacancy-employer-text"})
        company = company_item.text.replace("\xa0", " ") if company_item else ""
        print(f"Company: {company}")  # Отладка

        city_item = item.find("span", {"data-qa": "vacancy-serp__vacancy-address"})
        city = re.sub(r"\sи.+", "", city_item.text) if city_item else ""
        print(f"City: {city}")  # Отладка

        if title and ("django" in title.lower() or "flask" in title.lower()):
            result.append(
                {
                    "link": item.find("a", class_="serp-item__title")["href"],
                    "salary": salary,
                    "company": company,
                    "city": city,
                }
            )

    print(f"Total results: {len(result)}")  # Отладка перед записью

    with open("result.json", "w", encoding="utf8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)


import random
from bs4 import BeautifulSoup
import requests
import time, json, csv
from time import sleep

url = 'https://hh.kz/search/vacancy?area=160&search_field=name&search_field=company_name&search_field=description&text=python&from=suggest_post&hhtmFrom=vacancy_search_list'
headers = {
    'Accept': "*/*",
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
}
# req = requests.get(url, headers=headers)
# src = req.text
#
# with open('data.csv', 'w') as f:
#     f.write(src)

# with open('data.csv') as f:
#     src = f.read()
#
# soup = BeautifulSoup(src, 'lxml')
# all_vacancies_link = soup.find_all('a', {"class": "bloko-link", "data-qa": "vacancy-serp__vacancy-title"})
#
# all_vacancies_dict = {}
# for i in all_vacancies_link:
#     i_text = i.text
#     i_href = i.get('href')
#
#     all_vacancies_dict[i_text] = i_href
#
# with open('all_vacancies_dict.json', 'w') as f:
#     json.dump(all_vacancies_dict, f, indent=4, ensure_ascii=False )

with open('blank/all_vacancies_dict.json') as f:
    all_vacancies = json.load(f)

iteration_count = int(len(all_vacancies)) - 1
count = 0
for vacancy_name, vacancy_href in all_vacancies.items():
    rep = [",", " ", "-", "'"]
    for item in rep:
        if count == 0:
            rep = [",", ' ', '-']
            for i in rep:
                vacancy_name = vacancy_name.replace(i, '_')
            req = requests.get(url=vacancy_href, headers=headers)
            src = req.text

            with open(f'blank/{count}_{vacancy_name}.html', 'w') as f:
                f.write(src)

            with open(f'blank/{count}_{vacancy_name}.html') as f:
                src = f.read()

            soup = BeautifulSoup(src, 'lxml')
            vacancy_descript = soup.find(class_='g-user-content').find_all("strong")

            skill1 = vacancy_descript[0].text
            skill2 = vacancy_descript[1].text
            skill3 = vacancy_descript[2].text


            with open(f"{count}_{vacancy_name}.csv", "w", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        skill1,
                        skill2,
                        skill3,

                    )
                )
                # собираем данные продуктов
                vacancy_data = soup.find(class_="g-user-content").find_all("ul")

                vacancy_info = []
                for item in vacancy_data:
                    vacancy_lis = item.find_all("li")

                    info1 = vacancy_lis[0].text
                    info2 = vacancy_lis[1].text
                    info3 = vacancy_lis[2].text

                    vacancy_info.append(
                        {
                            "info1": info1,
                            "info2": info2,
                            "info3": info3,
                        }
                    )
                with open(f"{count}_{vacancy_name}.csv", "a", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        (
                            info1,
                            info2,
                            info3,
                        )
                    )
                with open(f"{count}_{vacancy_name}.json", "a", encoding="utf-8") as file:
                    json.dump(vacancy_info, file, indent=4, ensure_ascii=False)

                count += 1
                print(f"# Итерация {count}. {vacancy_name} записан...")
                iteration_count = iteration_count - 1

                if iteration_count == 0:
                    print("Работа завершена")
                    break

                print(f"Осталось итераций: {iteration_count}")
                time.sleep(random.randrange(2, 4))



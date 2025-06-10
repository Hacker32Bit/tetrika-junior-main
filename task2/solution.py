from urllib.parse import quote, urljoin
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict
from typing import Dict
import csv


def wiki_parse(base_url: str, start: str = "А", end: str = "Я") -> Dict[str, int]:
    print("Working...")

    res = defaultdict(int)
    current_url = f"{base_url}&from={start}"
    current_url = quote(current_url, safe=":/?&=%")

    alphabet = [chr(c) for c in range(ord(start), ord(end) + 1)]

    is_end = False

    while True:
        html_doc = urlopen(current_url).read()
        soup = BeautifulSoup(html_doc, "html.parser")

        # Count items under each letter
        for element in soup.select("#mw-pages .mw-category-columns > div > ul > li"):
            first_char = element.text[0]
            if first_char in alphabet:
                res[first_char] += 1

        # Get visible letters on current page
        letters = [h3.get_text(strip=True) for h3 in soup.select("#mw-pages .mw-category-columns > div > h3")]

        # Check for end condition
        if end in letters:
            is_end = True
        if is_end and end not in letters:
            break

        next_link = soup.find("a", string="Следующая страница")
        if not next_link:
            break

        current_url = urljoin("https://ru.wikipedia.org", next_link["href"])

    return dict(res)


def save_csv(data: Dict[str, int], filename: str, delimiter: str = ","):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=delimiter)
        for letter, count in sorted(data.items()):
            writer.writerow([letter, count])


def main():
    url = "https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту"
    result = wiki_parse(url, start="А", end="Я")
    save_csv(result, "result.csv")
    print("DONE!")


if __name__ == "__main__":
    main()

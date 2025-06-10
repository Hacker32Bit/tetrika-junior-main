import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from solution import wiki_parse, save_csv
import csv
import os


@pytest.fixture
def sample_html_page():
    return """
    <div id="mw-pages">
        <div class="mw-category-columns">
            <div>
                <h3>А</h3>
                <ul>
                    <li>Акула</li>
                    <li>Аист</li>
                </ul>
            </div>
            <div>
                <h3>Б</h3>
                <ul>
                    <li>Бобр</li>
                </ul>
            </div>
        </div>
        <a href="/w/index.php?title=Категория:Животные_по_алфавиту&pagefrom=Б">Следующая страница</a>
    </div>
    """


@pytest.fixture
def final_html_page():
    return """
    <div id="mw-pages">
        <div class="mw-category-columns">
            <div>
                <h3>В</h3>
                <ul>
                    <li>Волк</li>
                </ul>
            </div>
        </div>
    </div>
    """


@patch("solution.urlopen")
def test_wiki_parse(mock_urlopen, sample_html_page, final_html_page):
    # Configure mock to return different HTML on each call
    mock_response_1 = MagicMock()
    mock_response_1.read.return_value = sample_html_page.encode("utf-8")

    mock_response_2 = MagicMock()
    mock_response_2.read.return_value = final_html_page.encode("utf-8")

    mock_urlopen.side_effect = [mock_response_1, mock_response_2]

    base_url = "https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту"
    result = wiki_parse(base_url, start="А", end="В")

    assert isinstance(result, dict)
    assert result["А"] == 2
    assert result["Б"] == 1
    assert result["В"] == 1


def test_save_csv(tmp_path):
    data = {"А": 2, "Б": 1}
    file_path = tmp_path / "output.csv"
    save_csv(data, file_path)

    with open(file_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert rows == [["А", "2"], ["Б", "1"]]

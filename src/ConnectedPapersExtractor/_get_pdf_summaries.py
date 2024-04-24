from itertools import count
from pathlib import Path
from typing import Union

import arxiv
from enhanced_webdriver import EnhancedWebdriver
from selenium.webdriver.chrome.options import Options
from undetected_chromedriver import ChromeOptions

from . import ArticleFilter
from .PdfSummary import PdfSummary


def _get_pdf_summaries(
    connected_papers_link: str,
    article_filter: ArticleFilter,
    dir_path: Union[str, Path] = Path("./"),
) -> list[PdfSummary]:
    options = ChromeOptions()
    options.headless = True
    driver = EnhancedWebdriver.create(undetected=True, options=options)
    driver.get(connected_papers_link)
    summaries = list()
    for index in count(1):
        if not driver.click(
            f'//*[@id="desktop-app"]/div[2]/div[4]/div[1]/div/div[2]/div/div[2]/div[{index}]'
        ):
            break
        link = (
            driver.get_attribute(
                '//*[@id="desktop-app"]/div[2]/div[4]/div[3]/div/div[2]/div[5]/a[1]',
                "href",
            )
            .split("/")[-1]
            .rpartition(".")[0]
        )
        if not link:
            continue
        try:
            paper = next(arxiv.Client().results(arxiv.Search(id_list=[link])))
        except StopIteration:
            continue
        summaries.append(
            PdfSummary(
                download_args=(paper, str(dir_path),),
                year=int(
                    driver.get_text_of_element(
                        '//*[@id="desktop-app"]/div[2]/div[4]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]'
                    )
                ),
                citations=int(
                    driver.get_text_of_element(
                        '//*[@id="desktop-app"]/div[2]/div[4]/div[3]/div/div[2]/div[4]/div[1]'
                    ).split()[0]
                ),
            )
        )
    summaries = article_filter.filter(summaries)

    return summaries

import os
from itertools import count
from pathlib import Path
from typing import Union

from download import download
from enhanced_webdriver import EnhancedWebdriver
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
    downloads = list()
    for index in count(1):
        if not driver.click(
            f'//*[@id="desktop-app"]/div[2]/div[4]/div[1]/div/div[2]/div/div[2]/div[{index}]'
        ):
            break
        link = driver.get_attribute(
            '//*[@id="desktop-app"]/div[2]/div[4]/div[3]/div/div[2]/div[5]/a[1]',
            "href",
        )
        if driver.get_text_of_element('//*[@id="desktop-app"]/div[2]/div[4]/div[3]/div/div[2]/div[5]/a[1]/span') != "PDF":
            continue
        file_path = dir_path.joinpath(link.rpartition('/')[-1]).with_suffix('.pdf')
        summary = PdfSummary(
                file_path=file_path,
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
        summaries.append(summary)
        downloads.append((link, str(file_path),))
    driver.quit()
    for link, file_path in downloads:
        download(link, file_path)
    summaries = list(filter(PdfSummary.is_valid, summaries))
    summaries = article_filter.filter(summaries)
    for _, file_path in downloads:
        if not any(map(set(str(summary.file_path) for summary in summaries).__contains__, file_path)):
            os.remove(file_path)
    return summaries

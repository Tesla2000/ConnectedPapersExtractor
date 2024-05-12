from itertools import count
from pathlib import Path
from typing import Union

from enhanced_webdriver import EnhancedWebdriver
from undetected_chromedriver import ChromeOptions

from src.connectedpapersextractor import PdfSummaries, PdfSummary
from src.connectedpapersextractor.utils.download_summaries import _download_summaries


def download_summaries_from_connected_papers(
    connected_papers_link: str,
    dir_path: Union[str, Path] = Path("/"),
) -> PdfSummaries:
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
        link = driver.get_attribute(
            '//*[@id="desktop-app"]/div[2]/div[4]/div[3]/div/div[2]/div[5]/a[1]',
            "href",
        )
        if (
            driver.get_text_of_element(
                '//*[@id="desktop-app"]/div[2]/div[4]/div[3]/div/div[2]/div[5]/a[1]/span'
            )
            != "PDF"
        ):
            continue
        title = driver.get_text_of_element(
            '//*[@id="desktop-app"]/div[2]/div[4]/div[3]/div/div[2]/div[1]/div/a'
        )
        file_path = dir_path.joinpath(link.rpartition("/")[-1]).with_suffix(".pdf")
        summary = PdfSummary(
            file_path=file_path,
            download_link=link,
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
            title=title,
        )
        summaries.append(summary)
    driver.quit()
    _download_summaries(summaries, dir_path)
    return summaries

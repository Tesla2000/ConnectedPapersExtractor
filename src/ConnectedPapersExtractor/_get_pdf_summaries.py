import json
from dataclasses import asdict
from itertools import count
from pathlib import Path
from typing import Union

from download import download
from enhanced_webdriver import EnhancedWebdriver
from undetected_chromedriver import ChromeOptions

from . import PdfSummaries, PdfSummary
from .Config import Config


def _get_pdf_summaries(
    connected_papers_link: str,
    dir_path: Union[str, Path] = Path("./"),
) -> PdfSummaries:
    options = ChromeOptions()
    # options.headless = True
    driver = EnhancedWebdriver.create(undetected=True, options=options)
    driver.get(connected_papers_link)
    summaries = list()
    downloads = list()
    for index in count(1):
        if not driver.is_element(
            f'//*[@id="desktop-app"]/div[2]/div[4]/div[1]/div/div[2]/div/div[2]/div[{index}]'
        ):
            break
        driver.click(
            f'//*[@id="desktop-app"]/div[2]/div[4]/div[1]/div/div[2]/div/div[2]/div[{index}]'
        )
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
        title = driver.get_text_of_element('//*[@id="desktop-app"]/div[2]/div[4]/div[3]/div/div[2]/div[1]/div/a')
        file_path = dir_path.joinpath(link.rpartition("/")[-1]).with_suffix(".pdf")
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
            title=title,
        )
        summaries.append(summary)
        downloads.append(
            (
                link,
                str(file_path),
            )
        )
    driver.quit()
    for link, file_path in downloads:
        download(link, file_path)
    summaries = list(filter(PdfSummary.is_valid, summaries))
    dir_path.joinpath(Config.metadate_file_name).write_text(
        json.dumps(
            dict(
                (str(summary_dict.pop("file_path")), summary_dict)
                for summary_dict in map(asdict, summaries)
            ),
            indent=2,
        )
    )
    return summaries

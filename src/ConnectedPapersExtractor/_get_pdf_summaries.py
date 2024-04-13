from itertools import count
from pathlib import Path
from typing import Union

from enhanced_webdriver import EnhancedWebdriver
import arxiv

from .PdfSummary import PdfSummary


def _get_pdf_summaries(
    connectedpapers_link: str,
    dirpath: Union[str, Path] = Path("./"),
    filename: Union[str, Path] = "",
) -> list[PdfSummary]:
    driver = EnhancedWebdriver.create()
    driver.get(connectedpapers_link)
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
        try:
            paper = next(arxiv.Client().results(arxiv.Search(id_list=[link])))
        except StopIteration:
            continue
        out_path = paper.download_pdf(dirpath=str(dirpath), filename=str(filename))
        summaries.append(
            PdfSummary(
                Path(out_path),
                int(
                    driver.get_text_of_element(
                        '//*[@id="desktop-app"]/div[2]/div[4]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]'
                    )
                ),
                int(
                    driver.get_text_of_element(
                        '//*[@id="desktop-app"]/div[2]/div[4]/div[3]/div/div[2]/div[4]/div[1]'
                    ).split()[0]
                ),
            )
        )
    return summaries

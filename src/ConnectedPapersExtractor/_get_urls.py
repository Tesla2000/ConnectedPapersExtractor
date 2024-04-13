from itertools import count, takewhile
from typing import Generator

from enhanced_webdriver import EnhancedWebdriver


def _get_urls(connectedpapers_link: str) -> Generator[str, None, None]:
    driver = EnhancedWebdriver.create()
    driver.get(connectedpapers_link)
    for _ in takewhile(
        lambda index: driver.click(
            f'//*[@id="desktop-app"]/div[2]/div[4]/div[1]/div/div[2]/div/div[2]/div[{index}]'
        ),
        count(1),
    ):
        pass
    return filter(
        lambda link: link.startswith("https://arxiv.org/pdf/"),
        (
            driver.get_attribute(
                '//*[@id="desktop-app"]/div[2]/div[4]/div[3]/div/div[2]/div[5]/a[1]',
                "href",
            )
            for _ in takewhile(
                lambda index: driver.click(
                    f'//*[@id="desktop-app"]/div[2]/div[4]/div[1]/div/div[2]/div/div[2]/div[{index}]'
                ),
                count(1),
            )
        ),
    )

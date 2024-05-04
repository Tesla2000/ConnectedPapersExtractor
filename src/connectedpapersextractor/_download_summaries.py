import json
from contextlib import suppress
from os import PathLike
from pathlib import Path

from dataclasses import asdict
from download import download

from . import PdfSummaries
from .Config import Config


def _download_summaries(summaries: PdfSummaries, out_dir: PathLike[str]) -> PdfSummaries:
    for summary in summaries:
        link, file_path = summary.download_link, str(summary.file_path)
        with suppress(RuntimeError):
            download(link, file_path)
    summaries = list(
        set(summary for summary in summaries if summary.is_valid()))
    Path(out_dir).joinpath(Config.metadate_file_name).write_text(
        json.dumps(
            dict(
                (str(summary_dict.pop("file_path")), summary_dict)
                for summary_dict in map(asdict, summaries)
            ),
            indent=2,
        )
    )
    return summaries

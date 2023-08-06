import sys

from rich.console import Console

from norma2.config.config import get_config
from norma2.config.config_class import OutputFormat
from norma2.main import main
from norma2.utils import open_file


def entrypoint():
    config = get_config(Console(record=True))

    ex = main(config)

    out = None
    outfilext = None
    outfile = ".norma2.report"
    if config.format == OutputFormat("HTML"):
        outfilext = ".html"
        config.console.save_html(f"{outfile}{outfilext}")
        out = True
    elif config.format == OutputFormat("MARKDOWN"):
        outfilext = ".md"
        config.console.save_text(f"{outfile}{outfilext}")
        out = True
    elif config.format == OutputFormat("SVG"):
        outfilext = ".svg"
        config.console.save_svg(f"{outfile}{outfilext}")
        out = True
    if out:
        open_file(f"{outfile}{outfilext}")

    sys.exit(ex)

from urllib.parse import urlparse

import gdshortener
import typer

app = typer.Typer()
_isgd = gdshortener.ISGDShortener()
_vgd = gdshortener.VGDShortener()

"""
_vgd:VDGShortner = gdshortener.VDGDShortener()  # object from gdshortner
vgd:bool = False # bool for cli to use is.gd or v.gd
"""


@app.command()
def create(
    url,
    custom_url=typer.Option(None, help="Customize your url(s)"),
    log_stat: bool = typer.Option(False, help="Track your url(s)"),
    verify_ssl: bool = typer.Option(True, help="enable/disable ssl for your url(s)"),
    vgd: bool = typer.Option(False, help="use v.gd domain for your url(s)"),
):
    """create a shortened url using is.gd or v.gd"""

    # is.gd
    if not vgd:
        (short_url, stats_url) = _isgd.shorten(url, custom_url, log_stat, verify_ssl)
        if stats_url == None:
            typer.echo(f"\nurl: {short_url}")
        else:
            typer.echo(f"\nurl:   {short_url}\nstats: {stats_url}")
    # v.gd
    else:
        (short_url, stats_url) = _vgd.shorten(url, custom_url, log_stat, verify_ssl)
        if stats_url == None:
            typer.echo(f"\nurl: {short_url}")
        else:
            typer.echo(f"\nurl:   {short_url}\nstats: {stats_url}")


@app.command()
def stats(url: str):
    # Getter of parameter of url
    def getStatsCode(get_url: str):

        url_code = get_url.replace("\\", "/").split("/")[-1]
        base_stats_code = f"stats.php?url={url_code}"
        return base_stats_code

    # for is.gd url
    if urlparse(url).netloc == "is.gd":
        final_url = f"https://is.gd/{getStatsCode(url)}"
        typer.echo(f"Opening {final_url} on your default browser...")
        typer.launch(final_url)
    # for v.gd url
    elif urlparse(url).netloc == "v.gd":
        final_url = f"https://is.gd/{getStatsCode(url)}"
        typer.echo(f"Opening {final_url} on your default browser...")
        typer.launch(final_url)


if __name__ == "__main__":
    app()

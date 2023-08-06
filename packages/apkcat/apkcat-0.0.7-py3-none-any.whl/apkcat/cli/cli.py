import click

from apkcat import __version__
from apkcat.core import main


@click.version_option(version=__version__)
@click.command(no_args_is_help=True)
@click.option(
    "-f",
    "--target_file",
    is_flag=False,
    help="APK or DEX file",
)
@click.option(
    "-p",
    "--permission",
    is_flag=True,
    help="List all permission",
)
@click.option(
    "-a",
    "--activity",
    is_flag=True,
    help="List all activities",
)
@click.option(
    "-q",
    "--query",
    is_flag=False,
    help="Sample hash file",
)
def entry_point(target_file, permission, activity, query):
    """APKCAT"""

    main(target_file, permission, activity, query)


if __name__ == "__main__":
    entry_point()

from pathlib import Path
from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich.style import Style
import typer, json, os, sys
from source.excel import Excel

# Get project's home directory,
BASEDIR = Path(__file__).parents[1]
# All data directory
DATADIR = BASEDIR / "data"
# Insert the BASEDIR to system path
sys.path.insert(0, os.fspath(BASEDIR))


app = typer.Typer()
console = Console()

error_style = Style(color="red")
success_style = Style(color="green")


def getJsonData(excel_file_name):
    e = Excel(excel_name=excel_file_name)
    return json.loads(e.json)


def show_exception(e: Exception):
    console.print(e, style="red")


def show_error(e):
    console.print(e, style="red")


def show_warning(msg: str):
    console.print(msg, style="yellow")


def print_errors(r):
    if r.status_code == 401:
        print(r.json().get("detail"))
    elif r.status_code == 422:
        console.print("Validation erro:", style=error_style)
        print(r.json()["detail"])
    else:
        console.print(r.status_code, style=error_style)
        print(r.json()["detail"])

from dataclasses import dataclass
from rich.console import Console
from rich.table import Table


def split_wisely(line: str, sep: str, num: int):
    parts = line.split(sep)
    return parts[0:num]


@dataclass
class Table_:

    def show(self, content: str, title: str, columns: tuple, skiprow=1):

        table = Table(title=title)
        column_num = len(columns)
        for column in columns:
            table.add_column(column, justify="left", style="cyan", no_wrap=True)
        lines = content.splitlines()
        if not lines:
            return
        for item in lines[skiprow:]:
            parts = split_wisely(item, ":", column_num)
            table.add_row(*parts, style="green")

        console = Console()
        console.print(table)

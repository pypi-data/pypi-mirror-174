from __future__ import annotations

import sys
from argparse import ArgumentParser
from collections import defaultdict
from datetime import datetime
from functools import cached_property
from html import escape
from importlib import resources
from pathlib import Path
from typing import Iterable, Sequence
from warnings import warn

import tomli
from jinja2 import Environment, PackageLoader, select_autoescape
from rich.ansi import AnsiDecoder
from rich.console import (
    Console,
    ConsoleOptions,
    ConsoleRenderable,
    RenderableType,
    RenderResult,
)
from rich.segment import Segment
from rich.style import Style

__all__ = ["Span", "Row", "Grid"]

THUMB_W = 80
THUMB_H = 19


COLOR_CLASSES = [
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "bright-black",
    "bright-red",
    "bright-green",
    "bright-yellow",
    "bright-blue",
    "bright-magenta",
    "bright-cyan",
    "bright-white",
]

decoder = AnsiDecoder()
mock_console = Console(
    color_system="truecolor",
    force_terminal=True,
    width=float("inf"),  # type: ignore - sue me McGugan
    tab_size=8,
)


class Span(Sequence, ConsoleRenderable):
    def __init__(self, segment: Segment):
        if segment.control is not None:
            raise NotImplementedError()
        self._segment = segment

    @property
    def text(self) -> str:
        return self._segment.text

    @property
    def style(self) -> Style | None:
        return self._segment.style

    @cached_property
    def markup(self) -> str:
        safe_text = escape(self.text)

        if self.style is None:
            return safe_text

        classes = []
        inlines = []

        color = self.style.color
        bgcolor = self.style.bgcolor
        if self.style.reverse:
            color, bgcolor = bgcolor, color
        color_class = True
        color_hex = None
        if not color:
            if not self.style.reverse:
                classes.append("fgcolor")
            else:
                classes.append("bgcolor")
        else:
            assert color.number is not None  # for mypy
            if color.is_system_defined:
                classes.append(COLOR_CLASSES[color.number])
            else:
                color_class = False
                color_hex = color.get_truecolor().hex
                inlines.append(f"text-color: {color_hex}")
                inlines.append(f"text-decoration-color: {color_hex}")
                inlines.append(f"border-color: {color_hex}")

        if self.style.bold:
            if color_class:
                classes.append("-bold")
            else:
                raise NotImplementedError()
        if self.style.dim:
            raise NotImplementedError()
        if self.style.italic:
            inlines.append("font-style: italic")
        if self.style.underline:
            inlines.append("font-style: underline")
        if self.style.strike:
            inlines.append("font-style: line-through")
        if self.style.overline:
            inlines.append("font-style: overline")
        if not bgcolor:
            if self.style.reverse:
                classes.append("bg-fgcolor")
        else:
            if bgcolor.is_system_defined:
                assert bgcolor.number is not None  # for mypy
                classes.append(f"bg-{COLOR_CLASSES[bgcolor.number]}")
            else:
                inlines.append(f"background-color: {bgcolor.get_truecolor().hex}")

        span = "<span"
        if len(classes) > 0:
            f_classes = " ".join(classes)
            span += f' class="{f_classes}"'
        if len(inlines) > 0:
            f_styles = "; ".join(inlines)
            span += f' style="{f_styles}"'
        span += ">"

        return f"{span}{safe_text}</span>"

    def __getitem__(self, slc: slice) -> Span:
        return Span(Segment(self.text[slc], self.style))

    def __len__(self):
        return len(self.text)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderableType:
        yield self._segment

    def __hash__(self):
        return hash(self.text) ^ hash(self.style)

    def __repr__(self):
        return f"Span({self.text})"

    def __str__(self):
        return self.text


class Row(Sequence, ConsoleRenderable):
    def __init__(self, spans: Iterable[Span]):
        self.spans = tuple(spans)

    @property
    def text(self) -> str:
        return "".join(span.text for span in self.spans)

    @cached_property
    def markup(self) -> str:
        return "".join(span.markup for span in self.spans)

    def __getitem__(self, key: int | slice) -> Row:
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
        else:
            raise NotImplementedError()
        if step != 1:
            raise NotImplementedError()

        spans = []
        i = 0
        for span in self.spans:
            if i > stop:
                break
            end = i + len(span)
            if end > start:
                a = None if i >= start else start - i
                z = None if end <= stop else stop - start - i
                spans.append(span[a:z])
            i = end

        return Row(spans)

    def __len__(self) -> int:
        return sum(len(span) for span in self.spans)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield from self.spans

    def __hash__(self):
        return hash(self.spans)

    def __repr__(self):
        return f"Row({self.text})"

    def __str__(self):
        return self.text


class Grid(ConsoleRenderable):
    def __init__(self, rows: Iterable[Row]):
        self.rows = tuple(rows)

    @classmethod
    def from_str(cls, string: str) -> Grid:
        rows = []
        texts = list(decoder.decode(string))
        if len(texts) == 0:
            raise ValueError(f"{string=} contains no renderable text")
        for text in texts:
            segments = text.render(mock_console)
            row = Row(Span(s) for s in segments)
            rows.append(row)
        return cls(rows)

    @cached_property
    def h(self) -> int:
        return len(self.rows)

    @cached_property
    def w(self) -> int:
        return max(len(row) for row in self.rows)

    def __getitem__(self, ix: int | slice | tuple[int | slice, int | slice]) -> Grid:
        if not isinstance(ix, tuple):
            return Grid(tuple(self.rows[ix]))
        else:
            return Grid(tuple(row[ix[1]] for row in self.rows[ix[0]]))

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield from self.rows

    @cached_property
    def markup(self) -> str:
        return "\n".join(row.markup for row in self.rows)

    def __hash__(self):
        return hash(self.rows)

    def __repr__(self):
        result = f"Grid({self.rows[0].text}"
        for row in self.rows[1:]:
            result += f"\n     {row.text}"
        result += ")"
        return result

    def __str__(self):
        return "\n".join(row.text for row in self.rows)


class Art:
    def __init__(
        self,
        grid: Grid,
        /,
        name: str,
        *,
        hidden=False,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        **kw,
    ):
        self.grid = grid
        self.name = name
        self.hidden = hidden
        self.created_at = created_at
        self.updated_at = updated_at
        for k, v in kw.items():
            setattr(self, k, v)


def main(argv: list[str] = sys.argv):
    console = Console()

    parser = ArgumentParser()
    parser.add_argument("artdir")
    parser.add_argument("-g", "--glob", default="**/*.txt")
    parser.add_argument("-o", "--outdir", default="site")
    args = parser.parse_args(argv[1:])

    root = Path(args.artdir)

    manifest_path = root / "manifest.toml"
    with open(manifest_path) as f:
        raw_manifest = tomli.loads(f.read())
        if any(
            any(isinstance(v, dict) for v in d.values())
            for d in raw_manifest.values()
            if isinstance(d, dict)
        ):
            raise NotImplementedError(f"nested dicts\n{raw_manifest}")
        if any(
            "grid" in d.keys() for d in raw_manifest.values() if isinstance(d, dict)
        ):
            raise ValueError("grid is a reserved keyword")
        manifest = defaultdict(dict, raw_manifest)

    # TODO: check valid default values
    #       convert default dates to datetimes
    #       warn on discrepancies between custom value types
    #       Art dataclass factory based on custom values

    arts = []
    for path in root.glob(args.glob):
        with open(path) as f:
            raw = f.read()
            if len(raw) == 0:
                warn(f"{path} contains no text, skipping")
                continue
            try:
                grid = Grid.from_str(raw)
            except ValueError:
                warn(f"{path} contains no text, skipping")
                continue
        kw = manifest[path.name]
        if "name" not in kw.keys():
            kw["name"] = path.name
        arts.append(Art(grid, **kw))
    arts = sorted(arts, key=lambda a: a.updated_at or a.created_at, reverse=True)

    env = Environment(loader=PackageLoader("asciidump"), autoescape=select_autoescape())
    index = env.get_template("index.html")
    outdir = Path(args.outdir)
    outdir.mkdir(exist_ok=True)
    with open(outdir / "index.html", "w") as index_f:
        index_f.write(index.render(arts=arts))
    with open(outdir / "style.css", "w") as style_f:
        style_f.write(resources.read_text("asciidump", "style.css"))

    console.print("done")

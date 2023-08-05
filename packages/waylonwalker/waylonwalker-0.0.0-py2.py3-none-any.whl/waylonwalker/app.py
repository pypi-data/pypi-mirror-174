import webbrowser

from textual.css.query import NoMatches
from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Container
from textual.message import Message

LINKS = [
    ("home", "https://waylonwalker.com/"),
    ("blog", "https://waylonwalker.com/archive/"),
    ("YouTube", "https://youtube.com/waylonwalker"),
    ("Twitch", "https://www.twitch.tv/waylonwalker"),
    ("Twitter", "https://twitter.com/_waylonwalker"),
    ("Dev.to", "https://dev.to/waylonwalker"),
    ("LinkedIn", "https://www.linkedin.com/in/waylonwalker/"),
]


class Link(Static):
    def __init__(self, title, url):
        super().__init__(title)
        self.title = title
        self.url = url

    class ClearActive(Message):
        ...

    def on_click(self):
        webbrowser.open(self.url)

    def on_enter(self):
        self.add_class("active")

    async def on_leave(self):
        await self.emit(self.ClearActive(self))


class WaylonWalker(App):
    CSS = """
    Static {
        background: $primary-background;
        margin: 1;
        padding: 1;
    }
    Static.active {
        background: $accent;
    }
    """

    def action_next(self):
        self.select(1)

    def action_previous(self):
        self.select(-1)

    def select(self, n):
        links = self.query("Link")
        try:
            active = self.query_one(".active")
        except NoMatches:
            links[0].add_class("active")
            return
        active_index = links.nodes.index(active)
        next_index = active_index + n
        if next_index >= len(links):
            next_index = 0
        elif next_index < 0:
            next_index = len(links) - 1

        active.remove_class("active")
        links[next_index].add_class("active")

    def on_link_clear_active(self):
        for node in self.query(".active").nodes:
            node.remove_class("active")

    async def on_load(self, event: events.Load) -> None:
        self.bind("ctrl+c", "quit", show=False)
        self.bind("g", "submit", show=False)
        self.bind("q", "quit")
        self.bind("j", "next")
        self.bind("down", "next")
        self.bind("k", "previous")
        self.bind("up", "previous")
        self.bind("enter", "open")

    async def action_open(self) -> None:
        webbrowser.open(self.query_one(".active").url)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(*[Link(*link) for link in LINKS])
        yield Footer()


if __name__ == "__main__":
    from textual.features import parse_features
    import os
    import sys

    dev = (
        "--dev" in sys.argv
    )  # this works, but putting it behind argparse, click, or typer would be much better

    features = set(parse_features(os.environ.get("TEXTUAL", "")))
    if dev:
        features.add("debug")
        features.add("devtools")

    os.environ["TEXTUAL"] = ",".join(sorted(features))

    WaylonWalker.run(title="Waylon Walker")

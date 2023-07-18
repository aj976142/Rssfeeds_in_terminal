import urwid
import feedparser
import textwrap

class RSSReader:
    def __init__(self, feed_url):
        self.feed_url = feed_url
        self.entries = []
        self.feed_title = ""
        self.feed_description = ""

        self.fetch_feed()

        # Create the widgets
        title_widget = urwid.Text(self.feed_title)
        description_widget = urwid.Text(self.feed_description)
        entries_widget = urwid.ListBox(urwid.SimpleListWalker([]))
        self.update_entries_widget(entries_widget)

        # Combine the widgets into a layout
        self.layout = urwid.Pile([
            title_widget,
            urwid.Divider(),
            description_widget,
            urwid.Divider(),
            ('weight', 1, entries_widget),
        ])

        self.main_loop = urwid.MainLoop(self.layout, unhandled_input=self.handle_input)
        self.main_loop.run()

    def fetch_feed(self):
        feed = feedparser.parse(self.feed_url)
        self.entries = feed.entries
        self.feed_title = feed.feed.title
        self.feed_description = feed.feed.description

    def update_entries_widget(self, entries_widget):
        entries = []
        for entry in self.entries:
            title = entry.title
            summary = entry.summary

            widget = urwid.Pile([
                urwid.Text(('bold', title)),
                urwid.Text(textwrap.fill(summary, width=80))
            ])
            entries.append(urwid.AttrMap(widget, None, focus_map='reversed'))

        entries_widget.body = entries

    def handle_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

def main():
    feed_url = input("Enter the RSS feed URL: ")
    RSSReader(feed_url)

if __name__ == "__main__":
    main()

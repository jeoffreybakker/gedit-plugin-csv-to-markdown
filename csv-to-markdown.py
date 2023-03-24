#!/usr/bin/python
# -*- coding: utf-8 -*-

from gi.repository import GObject, Gedit, Gtk, Gio
import csv

class CsvToMarkdownAppActivatable(GObject.Object, Gedit.AppActivatable):
    app = GObject.property(type=Gedit.App)
    __gtype_name__ = 'CsvToMarkdownAppActivatable'
    
    def __init__(self):
        GObject.Object.__init__(self)
    
    def do_activate(self):
        self.app.set_accels_for_action("win.CsvToMarkdown", ["<Primary>M"])
    
        self.menu_ext = self.extend_menu('edit-section')
        self.menu_item = Gio.MenuItem.new(_("Csv to markdown"), 'win.CsvToMarkdown')
        self.menu_ext.append_menu_item(self.menu_item)
    
    def do_deactivate(self):
        self.app.set_accels_for_action("win.CsvToMarkdown", [])
        self.menu_item = None
        self.menu_ext = None

class CsvToMarkdownWindowActivatable(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "CsvToMarkdownWindowActivatable"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        action = Gio.SimpleAction(name="CsvToMarkdown")
        action.connect("activate", self.convert_csv_to_markdown)
        self.window.add_action(action)

    def do_deactivate(self):
        pass

    def do_update_state(self):
        pass

    def convert_csv_to_markdown(self, action, data):
        view = self.window.get_active_view()
        doc = view.get_buffer()

        start_iter = doc.get_start_iter()
        end_iter = doc.get_end_iter()

        # Get the CSV data from the buffer
        csv_data = doc.get_text(start_iter, end_iter, False)

        # Convert the CSV to Markdown
        markdown = ""
        rows = csv.reader(csv_data.splitlines())
        headers = next(rows)
        markdown += "|" + "|".join(headers) + "|\n"
        markdown += "|" + "|".join([":-:" for i in range(len(headers))]) + "|\n"
        for row in rows:
            markdown += "|" + "|".join(row) + "|\n"

        # Replace the buffer contents with the Markdown
        doc.begin_user_action()
        doc.set_text(markdown)
        doc.end_user_action()

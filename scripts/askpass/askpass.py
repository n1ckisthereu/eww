#!/usr/bin/python

import gi
import os
import sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class AskPassWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Ask Pass")
        self.set_modal(True)
        self.set_position(Gtk.WindowPosition.CENTER)

        # Connect the 'destroy' event to quit the application
        self.connect("destroy", Gtk.main_quit)

        # Set window to not resizable
        self.set_resizable(False)

        # Set window to not movable
        self.set_decorated(False)
        self.set_keep_above(True)

        # Add a label and a button to the window
        label = Gtk.Label(label="Please enter your password:")
        entry = Gtk.Entry()
        entry.set_visibility(False)  # Hide entered text
        entry.connect("activate", self.on_submit_clicked)  # Connect Enter key press event
        submit_button = Gtk.Button(label="Submit")
        submit_button.connect("clicked", self.on_submit_clicked)
        cancel_button = Gtk.Button(label="Cancel")
        cancel_button.connect("clicked", Gtk.main_quit)

        # Set up the layout
        grid = Gtk.Grid(column_homogeneous=True)
        grid.attach(label, 0, 0, 1, 1)
        grid.attach_next_to(entry, label, Gtk.PositionType.BOTTOM, 2, 1)
        grid.attach(submit_button, 0, 2, 1, 1)
        grid.attach(cancel_button, 1, 2, 1, 1)
        self.add(grid)

        label.set_margin_bottom(5)
        label.set_margin_top(5)
        label.set_margin_start(5)

        entry.set_margin_bottom(5)
        entry.set_margin_top(5)
        entry.set_margin_start(5)
        entry.set_margin_end(5)

        submit_button.set_margin_bottom(5)
        submit_button.set_margin_top(5)
        submit_button.set_margin_start(5)
        submit_button.set_margin_end(5)

        cancel_button.set_margin_bottom(5)
        cancel_button.set_margin_top(5)
        cancel_button.set_margin_start(5)
        cancel_button.set_margin_end(5)

        # Load CSS
        self.load_css()



    def load_css(self):
        style_provider = Gtk.CssProvider()

        # Load CSS from file using a relative path
        css_path = os.path.join(os.path.dirname(__file__), 'style.css')
        style_provider.load_from_path(css_path)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


    def on_submit_clicked(self, widget):
        password = self.get_password()
        sys.stdout.write(password)
        # You can add your logic here for password verification

        # Close the window
        self.destroy()

    def get_password(self):
        for child in self.get_children():
            if isinstance(child, Gtk.Grid):
                for grid_child in child.get_children():
                    if isinstance(grid_child, Gtk.Entry):
                        return grid_child.get_text()
        return None


if __name__ == "__main__":
    win = AskPassWindow()
    win.show_all()
    Gtk.main()

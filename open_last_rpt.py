import os
import glob
import sublime, sublime_plugin

rpt_files = []
ST3 = int(sublime.version()) >= 3000

def move_to_eof(view):
    if view.file_name() in rpt_files:
        rpt_files.remove(view.file_name())
        view.run_command("move_to", {"to": "eof"})

class OpenLastRptCommand(sublime_plugin.WindowCommand):
    def run(self):
        # Get last RPT file
        base_folder = os.path.join(os.getenv("LOCALAPPDATA"), "Arma 3")
        newest_rpt_file = max(glob.iglob(os.path.join(base_folder, "*.rpt")), key=os.path.getctime)
        # Save file into list for EventListener
        rpt_files.append(newest_rpt_file)
        # Open file
        self.window.open_file(newest_rpt_file)

class EventListener(sublime_plugin.EventListener):
    # Called when a file is finished loading
    def on_load_async(self, view):
        move_to_eof(view)

    # ST2 Compatibility (has no on_load_async)
    def on_load(self, view):
        if not ST3:
            move_to_eof(view)

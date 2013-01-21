import sublime, sublime_plugin

class ShowNextErrorCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    err_regex = "(\n(error|warning:)|uninitialized|[^l]remerge|Invalid data for)(?! (the .{4,15} product with which|your system is scheduled|will be expiring soon, and|this upcoming expiration.|information on your warning period.))"
    # Get end of last current selection.
    curr_pos = 0
    for region in self.view.sel():
        curr_pos = region.end()

    # Find the next error
    next_error = self.view.find(err_regex, curr_pos, sublime.IGNORECASE)
    if next_error:
      # Clear out any previous selections.
      self.view.sel().clear()
      self.view.sel().add(next_error)
      self.view.show(next_error)
      sublime.status_message("Found error at " + str(next_error))
    else:
      sublime.status_message("No more errors!")

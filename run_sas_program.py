# prototyping custom build command.
import sublime, sublime_plugin, subprocess, os, re
class RunSasProgramCommand(sublime_plugin.WindowCommand):
  def check_log(log_path, err_regx):
    log = open(log_filename)
    log_contents = log.read()
    log.close()
    num_errs = len(re.findall(err_regx, log_contents))
    return "\nLog file: " + log_path + "\n" + "Found " + num_errs + " errors/warnings."

  def run(self):
    self.window.active_view().run_command('save')
    prg_filename = self.window.active_view().file_name()
    extension = os.path.splitext(prg_filename)[-1].lower()
    if extension == '.sas':
      log_filename = prg_filename[:-3] + 'log'
      lst_filename = prg_filename[:-3] + 'lst'
      lrn_filename = lst_filename + '.last.run'
      if os.path.exists(lrn_filename):
        os.remove(lrn_filename)
      s = sublime.load_settings('sas.sublime-settings')
      sas_path = s.get('sas-path', "C:\\Program Files\\SAS\\SASFoundation\\9.2\\sas.exe")
      sas_args = s.get('sas-args', ['-nologo', '-noovp'])
      err_regx = s.get('err-regx', "(^(error|warning:)|uninitialized|[^l]remerge|Invalid data for)(?! (the .{4,15} product with which|your system is scheduled|will be expiring soon, and|this upcoming expiration.|information on your warning period.))")
      s.set('sas-path', sas_path)
      s.set('sas-args', sas_args)
      s.set('err-regx', err_regx)
      sublime.save_settings('sas.sublime-settings')
      err_regx = re.compile(err_regx, re.MULTILINE + re.IGNORECASE)
      if os.path.exists(sas_path):
        call_args = [sas_path, '-sysin', prg_filename, '-log', log_filename, '-print', lst_filename] + sas_args
        # print subprocess.list2cmdline(call_args)
        subprocess.call(call_args)
        sublime.status_message("Finished running " + prg_filename)
        if os.path.exists(lst_filename):
          self.window.open_file(lst_filename)
        if os.path.exists(log_filename):
          res = check_log(log_filename, err_regx)
          sublime.message_dialog("Finished!" + res)
          self.window.open_file(log_filename)
          self.window.active_view().run_command('show_next_error')
        else:
          sublime.message_dialog("Problem!  Did not find the expected log file (" + log_filename + ").")
        # print sas_path + " exists?: " + str(os.path.exists(sas_path))
        # sublime.message_dialog("Pretend I ran " + sas_path)
        # self.window.open_file(r'C:\Users\Roy\AppData\Roaming\Sublime Text 3\Packages\SAS\notes.txt')
      else:
        sublime.message_dialog("Problem--could not find sas.exe at " + sas_path + ".  Please update the sas-path setting in sas.sublime-settings in the User package folder.")
    else:
      sublime.message_dialog('Sorry--this only works with .sas files.')


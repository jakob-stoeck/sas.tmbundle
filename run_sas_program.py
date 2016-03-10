# prototyping custom build command.
import sublime, sublime_plugin, subprocess, os, re
class RunSasProgramCommand(sublime_plugin.WindowCommand):
  def check_log(self, log_path, err_regx):
    if os.path.exists(log_path):
      log = open(log_path)
      log_contents = log.read()
      log.close()
      num_errs = len(re.findall(err_regx, log_contents))
      self.window.open_file(log_path)
      self.window.active_view().run_command('show_next_error')
      return "\nLog file: " + log_path + "\n" + "Found " + str(num_errs) + " errors/warnings."
    else:
      return "PROBLEM!--could not find log file " + log_path + "!"

  def run_calc(self):
    # sublime.message_dialog("boobies!")
    subprocess.call('calc.exe')

  def find_logs(self, main_logfile):
    # Searches the main log for evidence of other, PROC PRINTTO-spawned logs and returns an array of file paths
    # representing all the logs for the job.
    ret = [main_logfile]
    l = open(main_logfile)
    log = l.read()
    l.close()
    ropts = re.IGNORECASE
    # If I was a better regex guy I would combine these two & use a proper backreference--some other time.
    diverted_regex_double = re.compile("proc\s+printto\s+log\s*=\s*\"([^\"]*)\"", ropts)
    diverted_regex_single = re.compile("proc\s+printto\s+log\s*=\s*'([^']*)'", ropts)

    other_logs = []
    other_logs += diverted_regex_single.findall(log)
    other_logs += diverted_regex_double.findall(log)

    # Search for macro vars in these putative log file paths
    for logpath in other_logs:
      corrected_path = ""
      path_components = re.split(r'[/.\\]', logpath)
      for index, component in enumerate(path_components):
        # print(index, component)
        if len(component) > 1:
          if component[0] == '&':
            strrgx = "[^*]%let\s+" + str.strip(component[1:]) + "\s*=([^;]*)"
            print(strrgx)
            macrolet_regex = re.compile(strrgx, ropts)
            macro_value = re.findall(macrolet_regex, log)
            if len(macro_value) == 1:
              component = str.strip(macro_value[0])
            else:
              print("Problem--could not find a value for macro var '&" + str.strip(component[1:]) + "'!")
        if index in range(0, len(path_components) - 2):
          corrected_path += component + "/"
        elif index == len(path_components) - 1:
          corrected_path += '.' + component
        else:
          corrected_path += component
      print(corrected_path)
      ret.append(corrected_path)
    return ret

  def shell_out_to_sas(self, call_args, prg_filename, lst_filename, log_filename, err_regx, sas_path):
    subprocess.call(call_args)
    sublime.status_message("Finished running " + prg_filename)
    if os.path.exists(lst_filename):
      self.window.open_file(lst_filename)
    if os.path.exists(log_filename):
      res = "Finished!\n"
      for l in self.find_logs(log_filename):
        res += self.check_log(l, err_regx)
      sublime.message_dialog(res)
    else:
      sublime.message_dialog("Problem!  Did not find the expected log file (" + log_filename + ").")
    # print sas_path + " exists?: " + str(os.path.exists(sas_path))
    # sublime.message_dialog("Pretend I ran " + sas_path)
    # self.window.open_file(r'C:\Users\Roy\AppData\Roaming\Sublime Text 3\Packages\SAS\notes.txt')



  def run(self):
    self.window.active_view().run_command('save')
    prg_filename = self.window.active_view().file_name()
    extension = os.path.splitext(prg_filename)[-1].lower()
    if extension == '.sas':
      log_filename = prg_filename[:-3] + 'log'
      lst_filename = prg_filename[:-3] + 'lst'
      lrn_filename = lst_filename + '.last.run'
      wrkdir, prog = os.path.split(prg_filename)
      if os.path.exists(lrn_filename):
        os.remove(lrn_filename)
      s = sublime.load_settings('SAS_Package.sublime-settings')
      sas_path = s.get('sas-path', "C:\\Program Files\\SAS\\SASFoundation\\9.2\\sas.exe")
      sas_args = s.get('sas-args', ['-nologo', '-noovp'])
      err_regx = s.get('err-regx', "(^(error|warning:)|uninitialized|[^l]remerge|Invalid data for)(?! (the .{4,15} product with which|your system is scheduled|will be expiring soon, and|this upcoming expiration.|information on your warning period.))")
      s.set('sas-path', sas_path)
      s.set('sas-args', sas_args)
      s.set('err-regx', err_regx)
      sublime.save_settings('SAS_Package.sublime-settings')
      err_regx = re.compile(err_regx, re.MULTILINE + re.IGNORECASE)
      if os.path.exists(sas_path):
        call_args = [sas_path, '-sysin', prg_filename, '-log', log_filename, '-print', lst_filename, '-SASINITIALFOLDER', wrkdir] + sas_args
        # print subprocess.list2cmdline(call_args)
        # sublime.set_timeout_async(self.run_calc, 0)
        sublime.set_timeout_async(lambda: self.shell_out_to_sas(call_args, prg_filename, lst_filename, log_filename, err_regx, sas_path), 0)
      else:
        sublime.message_dialog("Problem--could not find sas.exe at " + sas_path + ".  Please update the sas-path setting in SAS_Package.sublime-settings in the User package folder.")
    else:
      sublime.message_dialog('Sorry--this only works with .sas files.')


# prototyping custom build command.
import sublime, sublime_plugin, subprocess, os, re
import threading

class RunSasProgramCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.active_view().run_command('save')
    self.window.active_view().show_popup('Submitting to SAS.')
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
      # Direct path to exe. Is there a better way to do this?
      sas_path = s.get('sas-path', "c:\\Program Files\\SASHome\\SASFoundation\\9.4\\sas.exe")
      sas_args = s.get('sas-args', ['-nologo', '-noovp'])
      err_regx = s.get('err-regx', "(^(error|warning:)|uninitialized|[^l]remerge|Invalid data for)(?! (the .{4,15} product with which|your system is scheduled|will be expiring soon, and|this upcoming expiration.|information on your warning period.))")
      sas_config_path = s.get('sas-config-path', '')
      s.set('sas-path', sas_path)
      s.set('sas-args', sas_args)
      s.set('err-regx', err_regx)
      s.set('sas-config-path', sas_config_path)
      sublime.save_settings('SAS_Package.sublime-settings')
      err_regx = re.compile(err_regx, re.MULTILINE + re.IGNORECASE)
      if sas_config_path == '':
        config_spec = []
      else:
        if os.path.exists(sas_config_path):
          # Not really sure why I have to manually quote-delimit this, but it appears I do.
          config_spec = ["-config '", sas_config_path, "'"]
        else:
          sublime.message_dialog('Could not find config file "' + sas_config_path + '"--ignoring.')
          config_spec = []
      if os.path.exists(sas_path):
        call_args = [sas_path, config_spec, '-sysin', prg_filename, '-log', log_filename, '-print', lst_filename, '-SASINITIALFOLDER', wrkdir] + sas_args
        # sublime.message_dialog(subprocess.list2cmdline(call_args))
        threads = []
        thread = RunSasThreaded(self, call_args, prg_filename, lst_filename, log_filename, err_regx, sas_path)
        threads.append(thread)
        thread.start()
        self.handle_threads(threads)
      else:
        sublime.message_dialog("Problem--could not find sas.exe at " + sas_path + ".  Please update the sas-path setting in SAS_Package.sublime-settings in the User package folder.")
    else:
      sublime.message_dialog('Sorry--this only works with .sas files.')

  # Loop through list of threads and look for those
  # no longer running
  def handle_threads(self, threads):
    next_threads = []
    for thread in threads:
      if thread.is_alive():
        next_threads.append(thread)
        continue
      if thread.result == False:
        continue
    threads = next_threads

class RunSasThreaded(threading.Thread):
  def __init__(self, window_reference, call_args, prg_filename, lst_filename, log_filename, err_regx, sas_path):
    self.call_args = call_args
    self.window_reference = window_reference
    self.prg_filename = prg_filename
    self.lst_filename = lst_filename
    self.log_filename = log_filename
    self.err_regx = err_regx
    self.sas_path = sas_path
    self.result = None
    threading.Thread.__init__(self)

  def run(self):
    subprocess.call(self.call_args)
    sublime.status_message("Finished running " + self.prg_filename)
    if os.path.exists(self.lst_filename):
      self.window_reference.window.open_file(self.lst_filename)
    if os.path.exists(self.log_filename):
      res = "Finished!\n"
      for l in self.find_logs(self.log_filename):
        res += self.check_log(l, self.err_regx)
      sublime.message_dialog(res)
    else:
      sublime.message_dialog("Problem!  Did not find the expected log file (" + self.log_filename + ").")
    # print sas_path + " exists?: " + str(os.path.exists(sas_path))
    # sublime.message_dialog("Pretend I ran " + sas_path)

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

  def check_log(self, log_path, err_regx):
    if os.path.exists(log_path):
      log = open(log_path)
      log_contents = log.read()
      log.close()
      num_errs = len(re.findall(err_regx, log_contents))
      self.window_reference.window.open_file(log_path)
      self.window_reference.window.active_view().run_command('show_next_error')
      return "\nLog file: " + log_path + "\n" + "Found " + str(num_errs) + " errors/warnings."
    else:
      return "PROBLEM!--could not find log file " + log_path + "!"

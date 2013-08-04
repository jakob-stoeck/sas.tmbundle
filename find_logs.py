'''
  Can we detect that the log has been redirected with proc printto?
    If yes--can we work out exactly where the redirected log went?
      Even if it's done with a macro var (as is the norm)

  we want to capture (single-or-double-quote)(whatever is here that is *not* a single-or-double-quote)(same-kind-of-quote-that opened the string)
'''

import re

# Now we look for macro variables.  The typical CESR pattern seems to be diverting the log to ../local_only/myfile.log
# But let's see if we can do something more general.
def find_logs(main_logfile):
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
      # print "This component is: '" + str.strip(component) + "'"
      if len(component) > 1:
        if component[0] == '&':
          # print "This is a macro var reference."
          strrgx = "[^*]%let\s+" + str.strip(component[1:]) + "\s*=([^;]*)"
          # print "Regex will be: " + strrgx
          macrolet_regex = re.compile(strrgx, ropts)
          macro_value = re.findall(macrolet_regex, log)
          if len(macro_value) == 1:
            # print "Macro value is: " + macro_value[0]
            # corrected_path += str.strip(macro_value[0]) + "/"
            component = str.strip(macro_value[0]) 
          else:
            print "Problem--could not find a value for macro var '&" + str.strip(component[1:]) + "'!"
      # print index, component
      if index in range(1, len(path_components) - 2):
        corrected_path += component + "/"
      elif index == len(path_components) - 1:
        corrected_path += '.' + component
      else:
        corrected_path += component

    # print "Corrected path is: " + corrected_path
    ret.append(corrected_path)
  return ret

logs = find_logs('C:\Users\Roy\AppData\Roaming\Sublime Text 3\Packages\sas\chase_the.log')
print logs

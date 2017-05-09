#SAS Programming Package for Sublime Text 3

A modest package for doing SAS programming.

##Features
Syntax definitions (highlighting) for SAS Programs and .log files.
A build system that
  1. Batch-submits the currently-showing program to your local install of SAS.
  2. Waits for said program to finish.
  3. Opens the resulting .log file and checks it for errors or warnings (via a user-configurable regular expression).
A macro (bound to ctrl-e) for jumping from error/warning to error/warning in your log.

Snippets!
  1. 'sql' starts up a proc sql - quit block.
  2. 'mac' creates the shell of a macro.
  3. 'mloop' creates a shell macro that loops through all the vars in a dataset (saving you from having to remember where to put the double-ampersands).
  4. 'frq' starts up a FREQ call.
  5. 'srt' starts up a SORT call.
  5. 'tp' starts up a TRANSPOSE call.
  7. Many more!

Indentation rules.
Completions.

##Installation
Installation is via the wonderful [Package Control](http://wbond.net/sublime_packages/package_control).  Choose 'Package Control: Install Package' off the command palette and then find 'SAS Programming' on the resulting list.

Once that's done, create a trivial sas program (e.g., proc print data = sashelp.class ;), save it to a file (e.g., deleteme.sas) and hit ctrl-b to 'build' (aka batch-submit) your program.  One of two things will happen:
1. The package will find your copy of sas.exe in the location it expects, and the program will be batch-submitted (probably 20% of installs).
2. The package will *not* find sas.exe where it's expected and it will prompt you to tell it where your sas.exe is.

If you get outcome 2 there, use the menus to navigate to Preferences -> Package Settings -> SAS -> Settings-User.  That will open up the preferences file.  Find and edit the value listed for the "sas-path" at the bottom.  Enter the full path to your local copy of sas.exe.  Windows users, note that backslash characters need to be escaped (doubled up) to be properly read.


##To-Do
1. Polish build system.
  1. Play a sound at the finish of a job to call attention?
  3. Distinguish the taskbar icon from ST3's on the dialog that informs users that a build is complete?
  2. (Possible?) Bring (relevant instance of) ST3 to the fore upon dismissing finish dialog.
  4. Tap into built-in ['results view'](https://github.com/wbond/package_control_channel/pull/5571) stuff for error/warning navigations.



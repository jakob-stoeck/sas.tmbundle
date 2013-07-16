SAS Package for Sublime Text
============================

A modest package for doing SAS programming. [Read all about it here.](http://implementing-vdw.blogspot.com/2012/10/new-sublime-text-package-available-for.html)

Installation is via git only right now.  In your packages folder:

  `git clone git@github.com:rpardee/sas.tmbundle.git SAS`

Or failing that, [download the package as a zip from github](https://github.com/rpardee/sas.tmbundle/zipball/master) and then unzip it into %PACKAGES%/SAS.

In light testing it appeared to work with Sublime Text 3.

To-Do
-----
1. Polish build system.
2. Make installable via [Package Control](http://wbond.net/sublime_packages/package_control)
3. Polish syntax definition.  In particular:
  1. Enable multiple 'dsetname (optional options)' sequences after the 'data' statement.
  2. Color PROC SQL & any trailing options as other procs are colored.
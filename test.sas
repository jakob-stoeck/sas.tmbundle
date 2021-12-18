/*********************************************
* Roy Pardee
* Group Health Research Institute
* (206) 287-2078
* pardee.r@ghc.org
*
* C:\Documents and Settings/pardre1/Application Data/Sublime Text 2/Packages/SAS/test.sas
*
* purpose
*********************************************/

 %* %include "\\home\pardre1\SAS\Scripts\remoteactivate.sas" ;

options
  linesize  = 150
  msglevel  = i
  formchar  = '|-++++++++++=|-/|<>*'
  dsoptions = note2err
  nocenter
  noovp
  nosqlremerge

;
options orientation = landscape ;

libname s "\\home.ghc.org\home$\%sysget(USERNAME)\workingdata" ;

libname s "\\home.ghc.org\home$\%sysget(USERNAME)\workingdata" ;


* ods graphics / height
 = 6in width = 10in ;

%let td_goo = user              = "&username@LDAP"
              password          = "&password"
              server            = "&td_prod"
              schema            = "pardre1"
              connection        = global
              mode              = teradata
;

libname blah teradata &td_goo multi_datasrc_opt = in_clause ;

%macro something(arg12, arge9) ;
  * yo mama ;
%mend something ;


data b perm.ass dss dss2 ;
  x = 4 * y ;



%macro boobies(xarg1, xarg2) ;
  data something ;
    set &xarg2 ;
  run ;
%mend boobies ;


data bobbi (obs = 100) ;
  set bld.ah bling bloob ;
  x = lowcase(y) ;
  do x = 1 to 20 ;

  end ;
run ;

data    bobbity ;
data    boo ;
;


data s.gnu ;
  set b.old
  ;
* message ;
* foobar; * foobar;
x1 = a * b ;
x2    =    8*n ;
x = 1.2 ** 2-1;
x = 1.2 *** 2-1;
x = 1.2 * 2-1;
x = 1.2^(2-1);
z  = "&date."d;

/* foobar */

x = a    *
    b ;
run ;

* %let out_folder = //home/pardre1/ ;
%let out_folder = /C/Documents and Settings/pardre1/Application Data/Sublime Text 2/Packages/SAS/ ;
%let out_folder = C:\Documents and Settings/pardre1/Application Data/Sublime Text 2/Packages/SAS/test.sas ;

ods html path = "&out_folder" (URL=NONE)
         body   = "test.html"
         (title = "test output")
          ;

* ods rtf file = "&out_folder.test.rtf"d device = sasemf ;



run ;

** this is also a comment ;
ods _all_ close ; * trailing comment ;
proc sql outobs = 20 nowarn ;
  * this is a comment ;
  create table blah as
  select *
  from some.other_table
  ;
quit ;

%macro somthing ;
  data gnu (obs=100 alter='alterPass2');
    set old ;
  run ;

%mend something ;

data one ;
  set two ;
  if x = 3 then do ;
    slsl ;
  end ;
run ;

data bob ;
  set sashelp.class ;
  if height = 4 then do ;
    weight = 40 ;
  end ;
  if weight = 400 then do ;
    category = 'fatty' ;
  end ;
  else do;
    something ;
  end ;
run ;

data gnu;
  set old;
run;



data gnu ;
  set old ;
  if x = 1 then do ;
    y = 4 ;
  end ;
  if z = 4 then do ;
    z = 4 ;
  end ;
run ;

  if y = 2 then do ;
    bhal ;
  end ;

run ;

data three ;
  set four ;
  if x = 12 then do ;
end ;

proc something ;
  if x = 2 then do ;
end ;

%macro x ;
  data bob ;
    set mary ;
    if x = 2 then do ;
  end ;
  run ;
%mend ;

%let mon=JAN;
data foo;
set x;
where mydate between "01JAN2014"d and "01&mon.2014"d;

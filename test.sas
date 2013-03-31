/*********************************************
* Roy Pardee
* Group Health Research Institute
* (206) 287-2078
* pardee.r@ghc.org
*
* /C/Documents and Settings/pardre1/Application Data/Sublime Text 2/Packages/sas/test.sas
*
* Scratchpad for testing out this package.
*********************************************/

%include "\\home\pardre1\SAS\Scripts\remoteactivate.sas" ;

options
  linesize  = 150
  msglevel  = i
  formchar  = '|-++++++++++=|-/|<>*'
  dsoptions = note2err
  nocenter
  noovp
  nosqlremerge
;

proc blah ;
  sxx ;
run ;

%macro bob(args) ;
  hey here! ;
%mend bob ;
data gnu ;
  set old ;
run ;

PROC BLAH ;
  SLSLS ;
quit ;

proc sql ;
  create table gnu as
  select  *
  from    x as x
  order by  mrn
  ;
quit ;

data something ;
z = 4 ;
  output ;
run ;

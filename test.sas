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




%macro somthing ;
  data gnu ;
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

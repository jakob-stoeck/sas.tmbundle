data fakedata;
  do i = 5 to 100000000;
  	rnd = int(ranuni(0)*4 - 2);
    res = logbeta(i, i-rnd);
    output;
  end;
run;

title "Output of Test1.sas";
proc print data=fakedata(obs=10);
run;

data something_else ;
  set fakedata ;
  x = rand(uniform, 0, 1) ;
run ;

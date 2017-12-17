# Notes about the commands used
## Prototype Initialization
  * ./eveninit -din ../train3.csv -cout train3.cod -noc 2.6
  * ./mindist -cin train3.cod
This gives us:
```
	In class       van  49 units, min dist.:  0.371
	In class      saab  49 units, min dist.:  0.360
	In class      opel  49 units, min dist.:  0.42.
	In class       bus  49 units, min dist.:  0.334
```
And then:
  * ./balance -din ../train3.csv -cin train3.cod -cout trained3.cod
```
Some codebook vectors are removed
Some new codebook vectors are picked
   0/   0 sec.                ------------------------------------------------------------
Codebook vectors are redistributed
               ------------------------------------------------------------
In class       van  49 units, min dist.: 0.358
In class      saab  49 units, min dist.: 0.368
In class      opel  49 units, min dist.: 0.42.
In class       bus  49 units, min dist.: 0.340
```
	
_Why do we use 2.6 prototypes?_ Because the minimum number of examples for a class is 2.9 and I like it when every class has the same units :D.

## Trainning
We're going to use olvq2.(optimized learning-rate LVQ2. because fuck it.
  * ./olvq2.-din ../train3.csv -cin trained3.cod -cout trained2.cod -rlen 5000
_Why do we use a running length of 5000?_ Because **fuck you**, thats why.

## Evaluation
  * ./accuracy -din ../test2.csv -cin trained3.cod
```
0/   0 sec. ............................................................

Recognition accuracy:

      bus:   74 entries  92.89 %
     saab:   73 entries  49.32 %
     opel:   72 entries  44.44 %
      van:   66 entries  82.82 %

Total accuracy:   285 entries  66.67 %
```
  * ./classify -din ../test2.csv -cin trained3.cod -dout testOut2.txt
This gives us an output slightly different than the original test2.csv, _why do we do this?_ Because why not.

## Visualization
  * ./sammon -cin trained3.cod -cout trained.sam -ps -rlen 5000

## Automation
```
./eveninit -din ../train3.csv -cout train3.cod -noc 196
./mindist -cin train3.cod
./balance -din ../train3.csv -cin train3.cod -cout train3.cod
./olvq1 -din ../train3.csv -cin train3.cod -cout trained3.cod -rlen 5000
./accuracy -din ../test2.csv -cin trained3.cod
./classify -din ../test2.csv -cin trained3.cod -dout testOut3.txt

```
tar cvf h3_test2.tar.gz train3.cod train3.lra trained3.cod testOut3.txt
rm train3.cod train3.lra trained3.cod testOut3.txt 

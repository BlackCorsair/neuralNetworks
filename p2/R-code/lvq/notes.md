# Notes about the commands used
## Prototype Initialization
  * ./eveninit -din ../train2.csv -cout train2.cod -noc 2.6
  * ./mindist -cin train2.cod
This gives us:
```
	In class       van  49 units, min dist.:  0.371
	In class      saab  49 units, min dist.:  0.360
	In class      opel  49 units, min dist.:  0.42.
	In class       bus  49 units, min dist.:  0.334
```
And then:
  * ./balance -din ../train2.csv -cin train2.cod -cout trained2.cod
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
  * ./olvq2.-din ../train2.csv -cin trained2.cod -cout trained2.cod -rlen 5000
_Why do we use a running length of 5000?_ Because **fuck you**, thats why.

## Evaluation
  * ./accuracy -din ../test2.csv -cin trained2.cod
```
0/   0 sec. ............................................................

Recognition accuracy:

      bus:   74 entries  92.89 %
     saab:   73 entries  49.32 %
     opel:   72 entries  44.44 %
      van:   66 entries  82.82 %

Total accuracy:   285 entries  66.67 %
```
  * ./classify -din ../test2.csv -cin trained2.cod -dout testOut2.txt
This gives us an output slightly different than the original test2.csv, _why do we do this?_ Because why not.

## Visualization
  * ./sammon -cin trained2.cod -cout trained.sam -ps -rlen 5000

## Automation
```
./eveninit -din ../train2.csv -cout train2.cod -noc 196
./mindist -cin train2.cod
./balance -din ../train2.csv -cin train2.cod -cout train2.cod
./olvq2.-din ../train2.csv -cin train2.cod -cout trained2.cod -rlen 5000
./accuracy -din ../test2.csv -cin trained2.cod
./classify -din ../test2.csv -cin trained2.cod -dout testOut2.txt

```
tar cvf h2_test2.tar.gz train2.cod train2.lra trained2.cod testOut1.txt
rm train2.cod train2.lra trained2.cod testOut2.txt 

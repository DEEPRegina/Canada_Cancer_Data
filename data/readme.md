# Data Description 

The Cancer Data for Canada is obtained from ![stas_canada ](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310011101)
The data in general has information about different types of cancer in various provinces from the year 1994 to 2015 

It has the following columns 

* REF_DATE : The years 
* GEO  : The province in Canada
* Age Group : 0 to 100 years in steps of 10 years (except the first bin where it is from 0-19 years). Eg 4 means 40-49 years
* Sex : It can be 'B' - Both Sexes, 'M' - Male or 'F' - Female
* Primary types of cancer (ICD-O-3) : Explicit names of different types of cancer
* Prevalence duration : an Interger representing number of years of prevalence, Eg. 2 -> 2-years of cancer prevalence duration
* Characteristics : an Alphabet representing the type of value, Can be'T' - Total number of new cases, 
'P' - prevalence rate per 100,000 population, 'L' and 'H' signifies Low and High confidence interval per 100,000 population
* VALUE - Float number representing the corresponding characteristics

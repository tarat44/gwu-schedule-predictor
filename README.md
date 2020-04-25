Input: 
Provide the python script with the parameters:
       
    --subject <subject>: subject of the course you are interested in taking
    --coursenum <coursenum>: number of course you are interested in taking
    --semester <semester>: semester you are interested in taking the course (ex: fall)
Output:

All of the previous instances of that course offered in the last two years and the percent likelihood of the course being offered in the next given semester

ex:
```
   python predict_course_availability.py --subject=phys --coursenum=1234 --semester=spring
   Finding terms with course information available
   Obtaining and indexing information for fall 2019
   Obtaining and indexing information for summer 2019
   Obtaining and indexing information for spring 2019
   Obtaining and indexing information for fall 2018
   Obtaining and indexing information for summer 2018
   Obtaining and indexing information for spring 2018
   
   
   Previous instances of phys1234:
   
   12345:
   Semester: fall 2019	professor: Smith, J	status: WAITLIST
   
   45678:
   Semester: spring 2018	professor: Smith, J	status: OPEN

   91011:
   Semester: summer 2018	professor: None	status: CANCELLED
   
   Likelihood of course being offered next spring: 70 %
```

Disclaimer: The percent likelihood is just a fun number to get an idea of whether the class might be offered. It does not have any probabilitistic or statistical merit.

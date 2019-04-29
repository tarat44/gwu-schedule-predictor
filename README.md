Input: 
Provide the python script with the parameters:
       
    --subject <subject>: subject of the course you are interested in taking
    --coursenum <coursenum>: number of course you are interested in taking
    --semester <semester>: semester you are interested in taking the course (ex: fall)
Output:

All of the previous instances of that course offered in the last two years
Percent likelihood of the course being offered in the next given semester

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
   [('fall 2019', 'Smith, J', 'OPEN'), ('fall 2018', 'None', 'CANCELLED'), ('summer 2018', 'Smith, J', 'OPEN')]
   80 %
```

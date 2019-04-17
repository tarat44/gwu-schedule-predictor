Input: 
Provide the python script with the parameters:
       
    --subject <subject>: subject of the course you are interested in taking
    --coursenum <coursenum>: number of course you are interested in taking
Output:

All of the previous instances of that course offered in the last two years

ex:
```
   python get_course_instances.py --subject=phys --coursenum=1234
   Finding terms with course information available
   Obtaining and indexing information for fall 2019
   Obtaining and indexing information for summer 2019
   Obtaining and indexing information for spring 2019
   Obtaining and indexing information for fall 2018
   Obtaining and indexing information for summer 2018
   Obtaining and indexing information for spring 2018
   [('fall 2019', 'Smith, J', 'OPEN'), ('fall 2018', 'None', 'CANCELLED'), ('summer 2018', 'Smith, J', 'OPEN')]
```

Future Development: Algorithm to determine the likelihood of the course being offered in a given semester

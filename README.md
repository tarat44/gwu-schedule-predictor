# **GWU Schedule Predictor**

*The purpose of this tool is to allow students at George Washington University to get a better idea of whether a course will be provided in an upcoming semester that the student wishes to take it. Given the subject, course number, and desired semester the script will gather all previous instances of the course for the past semesters that are publicly available on the GW website, and output these instances and a guess about whether or not the course will be provided in the future semester based on a fixed algorithm that uses the previous data.*



## **Running the Script**

1. Create a python virtual environment
2. Run `pip install -r requirements.txt`
3. Call `predict_course_availability.py` with python using the following input parameters listed below

### Input: 
Provide the python script with the parameters:
       
    --subject <subject>: subject of the course you are interested in taking
    --coursenum <coursenum>: number of course you are interested in taking
    --semester <semester>: semester you are interested in taking the course (ex: fall, spring, summer)
### Output:

All of the previous instances of that course offered in the last two years and a guess of whether the course will be offered in the next given semester

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
   
   Likely to be offered next spring: Yes
```

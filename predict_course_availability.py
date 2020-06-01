import argparse

from get_course_instances import CollectCourseData
from predict import Predictor

def parse_args():
    """Obtain subject and course number arguments from user and parse data"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject', type=str, dest='subject',
                        help='The abbreviated subject of the course, ex: csci, bisc, chem')
    parser.add_argument('--coursenum', type=str, dest='coursenum',
                        help='Number of the course, ex: 1011, 1112')
    parser.add_argument('--semester', type=str, dest='semester',
                        help='Semester you would like to take the course, ex: fall, spring')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    subject = args.subject.upper()
    course_dict, terms = CollectCourseData().collect_course_data(subject)
    coursenum = args.coursenum
    try:
        course = course_dict[coursenum]
        instances = course.instances
        crns = instances.keys()
        print(f"\n\nPrevious instances of {subject}{coursenum}:\n")
        for crn in crns:
            print(f"{crn}:\nSemester: {instances[crn][0]}\tprofessor: {instances[crn][1]}\tstatus: {instances[crn][2]}\n")
        semester = args.semester
        predictor = Predictor(course_dict[coursenum], terms, semester)
        result = predictor.predict()
        print(f"Likely to be offered next {semester}: {result}")
    except KeyError:
        print(f"The course {subject} {coursenum} has not been offered in the last two years")

if __name__=="__main__":
        main()

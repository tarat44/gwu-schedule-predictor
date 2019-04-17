import lxml.html
import requests
import argparse


course_dict = {}
class Course:

    def __init__(self, title, semester, professor, status): 
        """Instantiate class with information related to
           first uncovered course offering"""
        self.semesters = [semester]
        self.professors = [professor]
        self.title = title
        self.statuses = [status]
        self.instances = [(semester, professor, status)]

    def add_instance_of_course(self, semester, professor, status):
        """add an offering with related info in the form of a tuple
           to list of previous offering"""
        self.semesters.append(semester)
        self.professors.append(professor)
        self.statuses.append(status)
        self.instances.append((semester, professor, status))


def call_url_and_get_html_object(url):
    resp = requests.get(url)
    return lxml.html.fromstring(resp.text)


def get_semester_course_data(url, semester):
    """inputs, url (str) to call, semester (str) that url find data for"""
    print(f"Obtaining and indexing information for {semester}")
    html = call_url_and_get_html_object(url)
    tables = html.findall(".//table[@class='courseListing']")

    # Parse html to get course offering data
    for table in tables:
        fields = table.findall(".//td")
        spans = table.findall(".//span")
        course_number =  str(spans[1].text.strip())
        title = str(fields[4].text).strip()
        professor = str(fields[6].text).strip()
        status = str(fields[0].text)

        # Add course offering data to dictionary of course classes
        if course_number not in course_dict.keys():
        # If course doesn't already exist in dictionary keys, instantiate class of it
            course_dict[course_number] = Course(
                title=title, semester=semester,
                professor=professor, status=status)
        else:
            course_dict[course_number].add_instance_of_course(
                semester, professor, status)

def parse_args():
    """Obtain subject and course number arguments from user and parse data"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject', type=str, dest='subject',
                        help='The abbreviated subject of the course, ex: csci, bisc, chem')
    parser.add_argument('--coursenum', type=str, dest='coursenum',
                        help='Number of the course, ex: 1011, 1112')
    args = parser.parse_args()
    return args


def get_urls_from_term_strings(terms, subject):
    """Inputs are a list of term html objects and a subject (string),
       Returns a list of tuples containing the url (string) to obtain courses 
       in a given subject for each term and the term (string)"""
    urls = []
    for term in terms:
        term = str(term.text).lower().strip()
        term_split = term.split(" ")
        if term_split[0] == "fall":
            term_num = "03"
        elif term_split[0] == "summer":
            term_num= "02"
        elif term_split[0] == "spring":
            term_num = "01"
        else:
            raise Exception("Isssue parsing urls")
        urls.append((f"https://my.gwu.edu/mod/pws/print.cfm?campId=1&termId={term_split[1]}{term_num}&subjId={subject}", term))
    return urls


def get_data_urls_and_terms(subject):
    """Return list of urls to obtain data from available previous semesers"""
    print("Finding terms with course information available")
    html = call_url_and_get_html_object("https://my.gwu.edu/mod/pws/") # Call home page url
    terms = html.findall(".//div[@class='tableHeaderFont'].//b") # Obtain list of available terms
    return get_urls_from_term_strings(terms, subject)

def main():
    args = parse_args()
    subject = args.subject.upper()
    urls = get_data_urls_and_terms(subject)
    for url, semester in urls:
        get_semester_course_data(url, semester)
    coursenum = args.coursenum
    try:
        print(course_dict[coursenum].instances)
    except KeyError:
        print(f"The course {subject} {coursenum} has not been offered in the last two years")

if __name__=="__main__":
        main()

import lxml.html
import requests

from utils import translate_term_to_numerical

class Course:

    def __init__(self, title, semester, professor, crn, status): 
        """Instantiate class with information related to
           first uncovered course offering"""
        self.semesters = [semester]
        self.professors = [professor]
        self.title = title
        self.statuses = [status]
        self.instances = {crn: (semester, professor, status)}

    def add_instance_of_course(self, semester, professor, crn, status):
        """add an offering with related info in the form of a tuple
           to list of previous offering"""
        self.semesters.append(semester)
        self.professors.append(professor)
        self.statuses.append(status)
        self.instances[crn] = (semester, professor, status)


class CollectCourseData:

    def __init__(self):
        self.course_dict = {}
        self.terms = []

    def call_url_and_get_html_object(self, url):
        resp = requests.get(url)
        return lxml.html.fromstring(resp.text)

    def get_semester_course_data(self, url, semester):
        """inputs, url (str) to call, semester (str) that url find data for"""
        print(f"Obtaining and indexing information for {semester}")
        html = self.call_url_and_get_html_object(url)
        tables = html.findall(".//table[@class='courseListing']")

        # Parse html to get course offering data
        for table in tables:
            fields = table.findall(".//td")
            spans = table.findall(".//span")
            course_number =  str(spans[1].text.strip())
            title = str(fields[4].text).strip()
            professor = str(fields[6].text).strip()
            status = str(fields[0].text)
            crn = str(fields[1].text)

            # Add course offering data to dictionary of course classes
            if course_number not in self.course_dict.keys():
            # If course doesn't already exist in dictionary keys, instantiate class of it
                self.course_dict[course_number] = Course(
                    title=title, semester=semester,
                    professor=professor, crn=crn, status=status)
            else:
                self.course_dict[course_number].add_instance_of_course(
                    semester, professor, crn, status)

    def get_url_from_term_string(self, num_term, subject):
        """Inputs are a term number (int) and a subject (string),
           Returns a list of tuples containing the url (string) to obtain courses
           in a given subject for each term and the term (string)"""
        return f"https://my.gwu.edu/mod/pws/print.cfm?campId=1&termId={num_term}&subjId={subject}"

    def get_data_urls_and_terms(self, subject):
        """Return list of urls to obtain data from available previous semesers"""
        print("Finding terms with course information available")
        html = self.call_url_and_get_html_object("https://my.gwu.edu/mod/pws/") # Call home page url
        term_elements = html.findall(".//div[@class='tableHeaderFont'].//b") # Obtain list of available terms
        terms = [term.text.lower().strip() for term in term_elements]
        term_urls = []
        
        for term in terms:
            num_term = translate_term_to_numerical(term)
            self.terms.append(int(num_term))
            term_urls.append((self.get_url_from_term_string(num_term, subject), term))
        return term_urls

    def collect_course_data(self, subject):
        urls = self.get_data_urls_and_terms(subject)
        for url, semester in urls:
            self.get_semester_course_data(url, semester)
        return self.course_dict, self.terms

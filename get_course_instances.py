import lxml.html
import requests


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


class CollectCourseData:

    def __init__(self):
        self.course_dict = {}

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

            # Add course offering data to dictionary of course classes
            if course_number not in self.course_dict.keys():
            # If course doesn't already exist in dictionary keys, instantiate class of it
                self.course_dict[course_number] = Course(
                    title=title, semester=semester,
                    professor=professor, status=status)
            else:
                self.course_dict[course_number].add_instance_of_course(
                    semester, professor, status)

    def get_urls_from_term_strings(self, terms, subject):
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

    def get_data_urls_and_terms(self, subject):
        """Return list of urls to obtain data from available previous semesers"""
        print("Finding terms with course information available")
        html = self.call_url_and_get_html_object("https://my.gwu.edu/mod/pws/") # Call home page url
        terms = html.findall(".//div[@class='tableHeaderFont'].//b") # Obtain list of available terms
        return self.get_urls_from_term_strings(terms, subject)

    def collect_course_data(self, subject):
        urls = self.get_data_urls_and_terms(subject)
        for url, semester in urls:
            self.get_semester_course_data(url, semester)
        return self.course_dict

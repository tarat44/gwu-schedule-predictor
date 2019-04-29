from utils import translate_term_to_numerical

class Predictor:

    def __init__(self, course, terms, semester):
        self.score = 0
        self.course = course
        self.terms = terms
        self.semester = semester
        terms.sort()
        self.latest_terms = terms[-3:]

    def predict(self):
        self.factor_in_enrollment()
        self.factor_in_multiple_professors()
        self.factor_in_semester_offered()
        self.create_percentage_from_score()

    def factor_in_enrollment(self):
        recent = True
        for crn in self.course.instances.keys():
            if self.course.instances[crn][2].lower() == "open":
                weight = 2
            elif self.course.instances[crn][2].lower() == "cancelled":
                weight = -.5
            elif self.course.instances[crn][2].lower() == "closed" or self.course.instances[crn][2].lower() == "waitlist":
                weight = 3
            if self.within_last_year(self.course.instances[crn]):
                weight = weight * 2
            self.score = self.score + weight

    def within_last_year(self, instance):
        if int(translate_term_to_numerical(instance[0])) in self.latest_terms:
                return True

    def factor_in_multiple_professors(self):
        professors = [professor for professor in self.course.professors if professor.lower() != "none"]
        number_professors = len(set(professors))
        if number_professors > 1:
            self.score = self.score + number_professors

    def factor_in_semester_offered(self):
        if self.semester.lower() not in str(self.course.semesters):
            seasons = [semester.lower().split(" ")[0] for semester in self.course.semesters]
            if len(set(seasons)) < len(seasons):
                self.score = self.score - 20
            else:
                self.score = self.score - 4

    def create_percentage_from_score(self):
        self.score = self.score * 10
        if self.score >= 95:
            self.score = 95
        if self.score <= 0:
            self.score = 5

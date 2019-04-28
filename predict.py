from utils import translate_term_to_numerical

class Predictor:

    def __init__(self, course, terms, semester):
        self.score = 0
        self.course = course
        self.terms = terms
        self.semester = semester
        self.latest_term = max(terms)

    def predict(self):
        self.factor_in_enrollment()
        self.factor_in_multiple_professors()
        self.factor_in_semester_offered()
        self.create_percentage_from_score()

    def factor_in_enrollment(self):
        for crn in self.course.instances.keys():
            if self.course.instances[crn][2].lower() == "open":
                weight = 3
            elif self.course.instances[crn][2].lower() == "cancelled":
                weight = -4
            elif self.course.instances[crn][2].lower() == "closed" or self.course.instances[crn][2].lower() == "waitlist":
                weight = 4
            if self.within_last_year(self.course.instances[crn]):
                weight = weight * 2
            self.score = self.score + weight

    def is_seasonal_course(self):
        seasons = [semester.split(" ")[0] for semester in self.course.semesters]
        if len(set(seasons)) == 1:
            return self.course.semesters[0]

    def within_last_year(self, instance):
        if int(translate_term_to_numerical(instance[0])[-2]) == self.latest_term:
                return True

    def factor_in_multiple_professors(self):
        prev_profs = [self.course.instances[list(self.course.instances.keys())[0]][1]]
        for crn in self.course.instances.keys():
            if self.course.instances[crn][1] not in prev_profs and self.course.instances[crn][1].lower() != "none":
                self.score = self.score + 2
            prev_profs.append(self.course.instances[crn][1])

    def factor_in_semester_offered(self):
        if self.is_seasonal_course() and self.is_seasonal_course().split(" ")[0].lower() != self.semester.lower():
            self.score = self.score - 20

    def create_percentage_from_score(self):
        self.score = self.score * 30
        if self.score >= 100:
            self.score = 99
        if self.score <= 0:
            self.score = 1

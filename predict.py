from utils import translate_term_to_numerical

class Predictor:

    def __init__(self, course, terms):
        self.score = 0
        self.course = course
        self.terms = terms

    def predict(self):
        self.factor_in_enrollment()
        self.factor_in_latest_term_available()
        self.factor_in_multiple_professors()
        self.create_percentage_from_score()

    def factor_in_enrollment(self):
        for crn in self.course.instances.keys():
            if self.course.instances[crn][2].lower() == "open":
                self.score = self.score + 4
            elif self.course.instances[crn][2].lower() == "cancelled":
                self.score = self.score - 6
            elif self.course.instances[crn][2].lower() == "closed" or self.course.instances[crn][2].lower() == "waitlist":
                self.score = self.score + 5

    def factor_in_latest_term_available(self):
        latest_term = max(self.terms)
        for crn in self.course.instances.keys():
            if translate_term_to_numerical(self.course.instances[crn][0]) == latest_term:
                self.score = self.score + 7
                return

    def factor_in_multiple_professors(self):
        prev_profs = [self.course.instances[list(self.course.instances.keys())[0]][1]]
        for crn in self.course.instances.keys():
            if self.course.instances[crn][1] not in prev_profs and self.course.instances[crn][1].lower() != "none":
                self.score = self.score + 2
            prev_profs.append(self.course.instances[crn][1])

    def create_percentage_from_score(self):
        self.score = self.score * 4
        if self.score > 100:
            self.score = 99

import pytest

from predict import Predictor
from get_course_instances import Course


@pytest.mark.parametrize("status, semester, score", [
    ("OPEN", "fall 2018", 2.5), ("CLOSED", "fall 2018", 3), ("CANCELLED", "fall 2018", -.5),
    ("OPEN", "fall 2019", 5), ("CLOSED", "fall 2019", 6), ("CANCELLED", "fall 2019", -1)])
def test_factor_in_enrollment(status, semester, score):
    course_dict = {}
    course_dict["1234"] = Course(title="title", semester=semester, professor="proferssor", crn="123456", status=status)
    predictor = Predictor(course_dict["1234"], [201903, 201902, 201901, 201803], "fall")
    predictor.factor_in_enrollment()
    assert predictor.score == score


@pytest.mark.parametrize("semester, result", [("fall 2018", None), ("fall 2019", True)])
def test_within_last_year(semester, result):
    course_dict = {}
    course_dict["1234"] = Course(title="title", semester=semester, professor="professor", crn="123456", status="OPEN")
    predictor = Predictor(course_dict["1234"], [201903, 201902, 201901, 201803], "fall")
    assert predictor.within_last_year(course_dict["1234"].instances["123456"]) == result


def test_factor_in_multiple_professors():
    course_dict = {}
    course_dict["1234"] = Course(title="title", semester="spring 2019", professor="professor", crn="123456", status="OPEN")
    course_dict["1234"].add_instance_of_course("spring 2019", "professor2", "56789", "OPEN")
    predictor = Predictor(course_dict["1234"], [201903, 201902, 201901, 201803], "fall")
    predictor.factor_in_multiple_professors()
    assert predictor.score == 2


def test_factor_in_semester_offered_one_semester():
    course_dict = {}
    course_dict["1234"] = Course(title="title", semester="spring 2019", professor="professor", crn="123456", status="OPEN")
    course_dict["1234"].add_instance_of_course("spring 2019", "professor", "56789", "OPEN")
    predictor = Predictor(course_dict["1234"], [201903, 201902, 201901, 201803], "fall")
    predictor.factor_in_semester_offered()
    assert predictor.score == -20

def test_factor_in_semester_offered_two_semesters():
    course_dict = {}
    course_dict["1234"] = Course(title="title", semester="spring 2019", professor="professor", crn="123456", status="OPEN")
    course_dict["1234"].add_instance_of_course("fall 2019", "professor", "56789", "OPEN")
    predictor = Predictor(course_dict["1234"], [201903, 201902, 201901, 201803], "summer")
    predictor.factor_in_semester_offered()
    assert predictor.score == -4


def test_likely_to_be_offered():
    course_dict = {}
    course_dict["1234"] = Course(title="title", semester="spring 2019", professor="professor", crn="123456", status="OPEN")
    predictor = Predictor(course_dict["1234"], [201903, 201902, 201901, 201803], "summer")
    predictor.score = 3
    assert not predictor.likely_to_be_offered()

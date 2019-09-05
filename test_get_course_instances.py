from get_course_instances import CollectCourseData, Course
  
def test_add_instance_of_course():
    course = Course("Intro Bio", "Fall 2019", "Johnson", "1234", "OPEN")
    course.add_instance_of_course("Spring 2020", "Smith", "5678", "CLOSED")

    assert course.semesters == ["Fall 2019", "Spring 2020"]
    assert course.statuses == ["OPEN", "CLOSED"]
    assert course.professors == ["Johnson", "Smith"]
    assert course.instances["1234"] == ("Fall 2019", "Johnson", "OPEN")
    assert course.instances["5678"] == ("Spring 2020", "Smith", "CLOSED")

def test_get_url_from_term_strings():
    assert CollectCourseData().get_url_from_term_string(
        "201802", "BISC") == "https://my.gwu.edu/mod/pws/print.cfm?campId=1&termId=201802&subjId=BISC"

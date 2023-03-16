import datetime
import os.path
import random
from readCourses import offered_list1, offered_list2, offered_list3


# from part2 import get_course_schedule


class Course:
    def __init__(self, code, section, course_type, instructor, schedule):
        self.code = code
        self.section = section
        self.instructor = instructor
        self.schedule = schedule
        self.course_type = course_type

    def get_code(self):
        return self.code

    def get_section(self):
        return self.section

    def get_instructor(self):
        return self.instructor

    def getScheduling(self):
        return self.schedule

    def setScheduling(self, new_schedule):
        self.schedule = new_schedule

    def __str__(self):
        return f"{self.code}-{self.course_type}-{self.section}-{self.instructor}-{self.schedule}"


class Schedule:
    def __init__(self, year, semester, courses: list[Course]):
        self.year = year
        self.semester = semester
        self.courses = courses

    def get_year(self):
        return self.year

    def get_semester(self):
        return self.semester

    def get_courses(self):
        return self.courses

    def __str__(self):
        string = f"Year: {self.year}\tSemester: {self.semester}\n"
        for course in self.courses:
            string += course.getInfo() + "\n"
        return string


class Plan:
    def __init__(self, year, semester, code, pre):
        self.year = year
        self.semester = semester
        self.code = code
        self.pre = pre

    def __str__(self):
        string = f"{self.year}\t{self.semester}:\t{self.code} {self.pre}"
        return string

    def get_code(self):
        return self.code


store_plan: list[Plan] = []


def readStudyPlan(file_path):
    """
        Reads a study plan from a txt file and returns a dictionary containing the course data.
        Parameters:
        file_path (str): The path to the txt file.
        Returns:
        dict: A dictionary containing the course data, organized by year and semester.
        Each course is represented as a dictionary with the following keys:
        - course: The name of the course.
        - prerequisites: A list of the prerequisites for the course.
    """
    data = {}
    with open(file_path, "r") as file:
        # skip the first line (column names)
        next(file)
        for line in file:
            element = line.strip().split(",")
            year = int(element[0])
            semester = int(element[1])
            course = element[2]
            prerequisites = element[3:] if len(element) > 3 else []

            # check if year exists in the data dictionary
            if not year in data:
                data[year] = {}
            # check if semester exists in the data dictionary
            if not semester in data[year]:
                data[year][semester] = []

            data[year][semester].append(
                {'course': course, 'prerequisites': prerequisites})
            plan = Plan(year, semester, course, prerequisites)
            store_plan.append(plan)
    return data


def read_student_records(file):
    """
        Reads a file containing student records and returns a dictionary of the data.
        Parameters:
        file (str): The path to the file containing student records.
        Returns:
        dict: A dictionary containing the student records, organized by year and semester.
        The dictionary has the following structure:
        {
            year: {
                semester: {
                    course_code: grade,
                    course_code: grade,
                    ...
                },
                semester: {
                    course_code: grade,
                    course_code: grade,
                    ...
                },
                ...
            }, ...
        }
        """
    try:
        records = {}
        with open(file, "r") as f:
            lines = f.readlines()[1:]
            for line in lines:
                element = line.strip().split(",")
                year = int(element[0])
                semester = int(element[1])
                # check if year exists in the records dictionary
                if not year in records:
                    records[year] = {}
                # check if semester exists in the records dictionary
                if not semester in records[year]:
                    records[year][semester] = {}

                for course in element[2:]:
                    course_code, grade = course.split(":")
                    records[year][semester][course_code] = int(grade)
        return records
    except FileNotFoundError:
        print("File Not Found!")


def get_passed_courses(student_records):
    """
        Returns a dictionary of passed courses from the input student records.

        Parameters:
        student_records (dict): A dictionary containing student records, organized by year and semester.

        Returns:
        dict: A dictionary of passed courses, organized by year and semester.

        The returned dictionary has the following structure:
        {
            year: {
                semester: [course_code, course_code, ...],
                semester: [course_code, course_code, ...],
                ...
            },
            year: {
                semester: [course_code, course_code, ...],
                semester: [course_code, course_code, ...],
                ...
            },
            ...
        }
        """
    passed_courses = {}
    for year, semesters in student_records.items():
        for semester, courses in semesters.items():
            # check if year exists in the passed_courses dictionary
            if year not in passed_courses:
                passed_courses[year] = {}
            # check if semester exists in the passed_courses dictionary
            if semester not in passed_courses[year]:
                passed_courses[year][semester] = []
            for course, grade in courses.items():
                if grade >= 60:
                    passed_courses[year][semester].append(course)
    return passed_courses


# display output

def displayStudyPlan(data):
    """
    Prints the study plan data in a tabular format showing the year, semester and courses.
    Args:
        data (dict): A dictionary containing study plan data with year, semester, and course information.
    Returns:
        None
    """
    head_y = "Year"
    head_s = "Semester"
    head_c = "Courses"
    print("%-5s%-10s%-5s" % (head_y, head_s, head_c))
    print("---- ------- ---------")
    for year in data.keys():
        for semester in data[year].keys():
            courses_list = []
            for value in data[year][semester]:
                code = value['course']
                courses_list.append(code)
            courses_list = ", ".join(courses_list)
            print(f"{year} {semester} {courses_list},")


def display_with_passed(study_plan, passed_courses):
    """
    Display the study plan along with the passed courses highlighted in green.

    Args:
        study_plan (dict): A dictionary containing the study plan data with years and semesters as keys.
        passed_courses (dict): A dictionary containing the passed courses data with years and semesters as keys.

    Returns:
        None. The function only prints the data to the console.

    """
    head_y = "Year"
    head_s = "Semester"
    head_c = "Courses"
    print("%-5s%-10s%-5s\n" % (head_y, head_s, head_c))
    for year in study_plan:
        for semester, values_list in study_plan[year].items():
            courses = []
            for value in values_list:
                course_code = value['course']
                # check if course is present in the passed_courses dictionary
                flag = 0
                for key in passed_courses.keys():
                    for sem, passed_list in passed_courses[key].items():
                        if course_code in passed_list:
                            flag = 1
                            break
                if flag:
                    courses.append("\033[32m" + course_code + "\033[0m")
                else:
                    courses.append(course_code)
            courses = ", ".join(courses)
            print(f"{year} {semester} {courses},\n")


def display_with_current(study_plan, passed_courses, current_passed):
    """
    Display the study plan along with the courses that have been passed Highlighted in Green and are currently being taken Highlighted in Red.

    Args:
        study_plan (dict): A dictionary containing the student's study plan.
        passed_courses (dict): A dictionary containing the courses that the student has passed.
        current_passed (list): A list containing the course codes of the courses that the student is currently taking.

    Returns:
        None
    """
    head_y = "Year"
    head_s = "Semester"
    head_c = "Courses"
    print("%-5s%-10s%-5s\n" % (head_y, head_s, head_c))
    for year in study_plan:
        for semester, values_list in study_plan[year].items():
            courses = []
            for value in values_list:
                course_code = value['course']
                # check if course is present in the passed_courses dictionary
                passed_flag = 0
                current_flag = 0
                for key in passed_courses.keys():
                    for sem, passed_list in passed_courses[key].items():
                        if course_code in passed_list:
                            passed_flag = 1
                            break
                if course_code in current_passed:
                    current_flag = 1
                if passed_flag:
                    courses.append("\033[32m" + course_code + "\033[0m")
                elif current_flag:
                    courses.append("\033[31m" + course_code + "\033[0m")
                else:
                    courses.append(course_code)
            courses = ", ".join(courses)
            print(f"{year} {semester} {courses},\n")


def read_electives(filename):
    """
    Reads a TXT file containing elective courses and their prerequisites and returns a dictionary of electives and their prerequisites.

    Args:
        filename (str): The name of the CSV file to read.

    Returns:
        A dictionary containing elective course codes as keys and lists of prerequisite course codes as values. Returns an empty dictionary if the file cannot be found.
    """
    try:
        electives = {}
        with open(filename, "r") as file:
            next(file)
            for line in file:
                elements = line.strip().split(",")
                group = elements[0]
                code = elements[1]
                pre = elements[2:] if len(elements) >= 2 else []
                electives[code] = pre

        return electives
    except FileNotFoundError:
        print("File Not Found")


def get_user_preferences():
    """
       Asks the user to input their preferences for minimum free days and maximum credits per week for each semester,
       and returns a dictionary with the user's preferences.

       Returns:
       - userPrefs (dict): a dictionary containing the user's preferences for each semester.
         Each key is a string representing the semester ("first", "second", "summer"), and each value is a dictionary with
         two keys: "min_free_days" (int) and "max_credits" (int).
    """
    semesters = ["first", "second", "summer"]
    userPrefs = {}
    for semester in semesters:
        min_free_days = int(
            input("What is the minimum number of free days you want per week, for the {} semester?".format(semester)))
        max_credits = int(
            input("What is the maximum number of credits you want to register, for the {} semester?".format(semester)))
        if semester == 'summer':
            max_credits = min(max_credits, 9)
        else:
            max_credits = min(max_credits, 18)
        userPrefs[semester] = {
            "min_free_days": min_free_days, "max_credits": max_credits}
    return userPrefs


def getPre(study_plan: dict):
    """
    Returns a dictionary of course prerequisites, based on a given study plan.

    Args:
        study_plan (dict): A dictionary representing the study plan. The keys of this
            dictionary are the years, and the values are dictionaries of semesters
            and their corresponding courses.

    Returns:
        dict: A dictionary of course prerequisites. The keys of this dictionary are the
            course codes, and the values are lists of prerequisites for the corresponding
            course. If a course has no prerequisites, the value associated with the course
            key is an empty list.

    """
    pres = {}
    for year in study_plan.keys():
        for semester, values_list in study_plan[year].items():
            for value in values_list:
                if value['prerequisites'] is not None:
                    pres[value['course']] = value['prerequisites']
                else:
                    pres[value['course']] = []
    return pres


def get_hours(code: str):
    """
    This function takes a course code as a parameter and returns the number of hours the course requires.
     If the length of the course code is less than 6 characters, the function returns 0.
    """
    if len(code) >= 6:
        return int(code[5])
    else:
        return 0


def check_semesters(passed_courses: dict):
    """
        Calculates the total planned credit hours and total passed credit hours for a student's academic plan.

        Args:
            passed_courses (dict): A dictionary representing the courses a student has passed, with the years and semesters as keys and the passed courses as values.

        Returns:
            A tuple containing two integers - the total planned credit hours and the total passed credit hours.
    """
    plan_hours = 0
    for course in store_plan:
        credit_hours = get_hours(course.get_code())
        plan_hours += credit_hours
    passed_hours = 0
    for year in passed_courses.keys():
        for semester, passed in passed_courses[year].items():
            for course in passed:
                passed_hours += get_hours(course)

    return plan_hours, passed_hours


def calculate_pre():
    """
        Counts the number of courses that have each prerequisite course in a given academic plan.

        Returns:
            A dictionary containing the count of how many courses have each prerequisite course.
    """
    number_of_pre = {}
    for course in store_plan:
        for pre in course.pre:
            if pre not in number_of_pre.keys():
                number_of_pre[pre] = 1
            else:
                number_of_pre[pre] += 1
    return number_of_pre


def calculate_pre_electives(electives: dict):
    electives_pre_numbers = {}
    for group in electives.keys():
        for course, pre in electives[group].items():
            for pre_course in pre:
                if pre_course not in electives_pre_numbers.keys():
                    electives_pre_numbers[pre_course] = 1
                else:
                    electives_pre_numbers[pre_course] += 1
    return electives_pre_numbers


def check_overlapping(day1, time1, day2, time2):
    """
        Checks if two courses have overlapping class times.

        Args:
            day1 (str): The day of the week for the first course.
            time1 (str): The time of day for the first course, in the format 'HH:MM - HH:MM'.
            day2 (str): The day of the week for the second course.
            time2 (str): The time of day for the second course, in the format 'HH:MM - HH:MM'.

        Returns:
            A boolean value indicating whether the two courses have overlapping class times.
    """
    # Check if both courses have class on the same day
    if day1 == day2:
        # Get the start and end times for both courses
        start_time1, end_time1 = time1.split(' - ')
        start_time2, end_time2 = time2.split(' - ')
        # Convert the start and end times to datetime objects
        start_time1 = datetime.datetime.strptime(start_time1, '%H:%M')
        end_time1 = datetime.datetime.strptime(end_time1, '%H:%M')
        start_time2 = datetime.datetime.strptime(start_time2, '%H:%M')
        end_time2 = datetime.datetime.strptime(end_time2, '%H:%M')
        # Check if the time intervals for both courses intersect
        if start_time1 < end_time2 and start_time2 < end_time1:
            return True
        else:
            return False
    else:
        return False


def getElective(code: str, electives: dict, passed_courses):
    for course, values in electives.items():
        if code == course:
            for value in values:
                pass


def get_specific_pre(study_plan: dict, code: str):
    pre_req = []
    for year in study_plan.keys():
        for semester, values in study_plan[year].items():
            for value in values:
                if value['course'] == code:
                    pre_req = value['prerequisites']
    return pre_req


def generateTime(registered_courses_list: [Course], new_course, max_attempts=100):
    days = ["M", "T", "W", "R", "F"]  # list of days
    start_hour = 8  # earliest possible start hour
    end_hour = 17  # latest possible end hour

    # Create a list of all the time slots that are already taken
    taken_slots = []
    for course in registered_courses_list:
        for day, time_range in course.getScheduling.items():
            start_time, end_time = time_range.split(" - ")
            start_time = int(start_time[:2])
            end_time = int(end_time[:2])
            for hour in range(start_time, end_time):
                taken_slots.append((day, hour))

    # Randomly generate a day and hour until we find an available slot
    for i in range(max_attempts):
        day = random.choice(days)
        hour = random.randint(start_hour, end_hour - len(new_course.schedule) + 1)

        # Check if the chosen slot is available
        available = True
        for i in range(len(new_course.schedule)):
            current_day = days[days.index(day) + i]
            current_hour = hour + i
            if (current_day, current_hour) in taken_slots:
                available = False
                break

        # If the slot is available, return the new course with the scheduled time
        if available:
            schedule = {}
            for i in range(len(new_course.schedule)):
                current_day = days[days.index(day) + i]
                current_hour = hour + i
                schedule[current_day] = f"{current_hour:02}:00 - {current_hour + 1:02}:00"
            new_course.schedule = schedule
            return new_course

    # If no free time slot is found within the maximum number of attempts, raise an exception
    return new_course


def create_schedules(study_plan: dict, passed_courses: dict, user_preferences: dict, electives: dict,
                     num_of_semesters: int, current_semester, current_year, pre_priority: dict):
    get_passed_codes = []
    schedulers_list: list[Schedule] = []
    sorted_dict = dict(sorted(electives.items(), key=lambda x: x[1], reverse=True))
    for year in passed_courses.keys():
        for semester, values in passed_courses[year].items():
            for value in values:
                get_passed_codes.append(value)
                if value in sorted_dict.keys():
                    del sorted_dict[value]

    for i in range(num_of_semesters):
        first_requested = None
        if len(sorted_dict) > 0:
            first_requested = next(iter(sorted_dict))
        key = ""
        if current_semester == 1:
            key = "first"
        elif current_semester == 2:
            key = "second"
        elif current_semester == 3:
            key = "summer"
        max_hours = user_preferences[key]['max_credits']
        current_semester_codes = []
        current_courses: list[Course] = []
        reserved_hours = 0
        needed_pre = []
        for year in study_plan.keys():
            for semester, values in study_plan[year].items():
                for value in values:
                    possible_scheduling = []
                    course_code = value['course']
                    pre_req = value['prerequisites']
                    if course_code not in get_passed_codes:
                        flag = 1
                        for any_pre in pre_req:
                            if any_pre not in get_passed_codes:
                                needed_pre.append(any_pre)
                                # course_code = any_pre
                                flag = 0
                        pre_flag = 1
                        if len(needed_pre) > 0:
                            temp_possible = []
                            for needed in needed_pre:
                                sign = 1
                                pre_for_needed = get_specific_pre(study_plan, needed)
                                if len(pre_for_needed) > 0:
                                    for one in pre_for_needed:
                                        if one not in get_passed_codes:
                                            sign = 0
                                if not sign:
                                    pre_flag = 0
                                    break
                                if current_semester == 1:
                                    for item in offered_list1:
                                        if needed == item.getCode():
                                            temp_possible.append(item)
                                elif current_semester == 2:
                                    for item in offered_list2:
                                        if needed == item.getCode():
                                            temp_possible.append(item)
                                elif current_semester == 3:
                                    for item in offered_list3:
                                        if needed == item.getCode():
                                            temp_possible.append(item)
                                break_flag = 0
                                for possible in temp_possible:
                                    if reserved_hours > max_hours or (
                                            reserved_hours + get_hours(needed)) > max_hours:
                                        break_flag = 1
                                        pre_flag = 0
                                        break
                                    low_priority = []
                                    if len(possible.getSchedule()) == 0:
                                        continue
                                    if len(current_courses) == 0:
                                        current_course = Course(possible.getCode(), possible.getSection(),
                                                                possible.getCourseType(), possible.getInstructor(),
                                                                possible.getSchedule())
                                        current_courses.append(current_course)
                                        get_passed_codes.append(needed)
                                        reserved_hours += get_hours(needed)
                                        break_flag = 1
                                        current_semester_codes.append(needed)
                                        if needed in sorted_dict.keys():
                                            del sorted_dict[needed]
                                        break
                                    # compare with the existed courses
                                    else:
                                        insert_flag = 1
                                        # check if there is an overlapping in current schedule:
                                        for inner_day, inner_time in possible.getSchedule().items():
                                            for course in current_courses:
                                                if len(course.getScheduling()) == 0:
                                                    break
                                                for course_day, course_time in course.getScheduling().items():
                                                    check = check_overlapping(inner_day, inner_time, course_day,
                                                                              course_time)
                                                    if check:
                                                        insert_flag = 0
                                                        pre_flag = 0
                                                        break
                                        if insert_flag:
                                            current_course = Course(possible.getCode(), possible.getSection(),
                                                                    possible.getCourseType(), possible.getInstructor(),
                                                                    possible.getSchedule())
                                            current_courses.append(current_course)
                                            get_passed_codes.append(needed)
                                            reserved_hours += get_hours(needed)
                                            current_semester_codes.append(needed)
                                            break_flag = 1
                                            pre_flag = 1
                                            if course_code in sorted_dict.keys():
                                                del sorted_dict[needed]
                                            break
                                if break_flag:
                                    break
                        # add the course to the schedule
                        if pre_flag:
                            if current_semester == 1:
                                for item in offered_list1:
                                    if course_code == item.getCode():
                                        possible_scheduling.append(item)

                            elif current_semester == 2:
                                for item in offered_list2:
                                    if course_code == item.getCode():
                                        possible_scheduling.append(item)
                            elif current_semester == 3:
                                for item in offered_list3:
                                    if course_code == item.getCode():
                                        possible_scheduling.append(item)
                    # choose one section !
                    break_flag = 0
                    for possible in possible_scheduling:
                        if reserved_hours > max_hours or (reserved_hours + get_hours(course_code)) > max_hours:
                            break_flag = 1
                            break
                        if len(possible.getSchedule()) == 0:
                            continue
                        if len(current_courses) == 0:
                            current_course = Course(possible.getCode(), possible.getSection(),
                                                    possible.getCourseType(), possible.getInstructor(),
                                                    possible.getSchedule())
                            current_courses.append(current_course)
                            get_passed_codes.append(course_code)
                            reserved_hours += get_hours(course_code)
                            break_flag = 1
                            current_semester_codes.append(course_code)
                            if course_code in sorted_dict.keys():
                                del sorted_dict[course_code]
                            break
                        # compare with the existed courses
                        else:
                            insert_flag = 1
                            # check if there is an overlapping in current schedule:
                            for inner_day, inner_time in possible.getSchedule().items():
                                for course in current_courses:
                                    if len(course.getScheduling()) == 0:
                                        continue
                                    for course_day, course_time in course.getScheduling().items():
                                        check = check_overlapping(inner_day, inner_time, course_day, course_time)
                                        if check:
                                            insert_flag = 0
                                            break
                            if insert_flag:
                                current_course = Course(possible.getCode(), possible.getSection(),
                                                        possible.getCourseType(), possible.getInstructor(),
                                                        possible.getSchedule())
                                current_courses.append(current_course)
                                get_passed_codes.append(course_code)
                                reserved_hours += get_hours(course_code)
                                current_semester_codes.append(course_code)
                                break_flag = 1
                                if course_code in sorted_dict.keys():
                                    del sorted_dict[course_code]
                                break
                    if break_flag:
                        break

        display_with_current(study_plan, passed_courses, get_passed_codes)

        for item in current_semester_codes:
            if current_year not in passed_courses:
                passed_courses[current_year] = {}
            # check if semester exists in the passed_courses dictionary
            if current_semester not in passed_courses[current_year]:
                passed_courses[current_year][current_semester] = []
            passed_courses[current_year][current_semester].append(item)

        current_schedule = Schedule(current_year, current_semester, current_courses)
        schedulers_list.append(current_schedule)
        if current_semester == 1 or current_semester == 2:
            current_semester += 1
        elif current_semester == 3:
            current_semester = 1
            current_year += 1
    return schedulers_list


def print_schedules(schedule: Schedule, file_name=None):
    days = ['M', 'T', 'W', 'R', 'S']

    # initialize a nested dictionary to hold the schedule for each day
    week_schedule = {day: {} for day in days}

    # loop through the schedule data and populate the week_schedule dictionary
    courses_list: list[Course] = []
    if len(schedule.get_courses()) > 0:
        courses_list = schedule.get_courses()
    for course in courses_list:
        for day, time in course.schedule.items():
            if day in days:
                # create a string representation of the class
                class_str = f"{course.get_code()}-{course.get_instructor()}-{course.get_section()}"
                # add the class to the schedule for the given day
                week_schedule[day][time] = class_str

    # print the weekly schedule
    if file_name is not None:
        try:
            with open(file_name, "a") as file:
                file.write(f"Weekly Schedule for Year {schedule.get_year()} - Semester {schedule.get_semester()}:\n")
                file.write("-----------------\n")
                for day, classes in week_schedule.items():
                    file.write(day + ":\n")
                    if not classes:
                        file.write("No Classes Scheduled\n")
                    else:
                        for time, class_name in sorted(classes.items()):
                            file.write(f"  {time}: {class_name}\n")
        except FileNotFoundError:
            print(f"The File {file_name} cant be open")
    else:
        print(f"Weekly Schedule for Year {schedule.get_year()} - Semester {schedule.get_semester()}:")
        print("-----------------")
        for day, classes in week_schedule.items():
            print(day + ":")
            if not classes:
                print("  No classes scheduled\n")
            else:
                for time, class_name in sorted(classes.items()):
                    print(f"  {time}: {class_name}")
            print()


# Option 1
study_plan = readStudyPlan("CEStudyPlan.txt")
# get prerequisites
pres = getPre(study_plan)
# 2
continue_flag = 1
while continue_flag:
    displayStudyPlan(study_plan)
    print("=" * 50)
    filename = input("Please enter the name and the location of the student records file: ")
    while not os.path.isfile(filename):  # check if the file exists or not
        print("File Not Found, Try Again")
        filename = input("Please enter the name of the student records file: ")
    student_records = read_student_records(filename)  # read student records
    passed_courses = get_passed_courses(student_records)
    # get number of remaining hours to be passed :
    plan_hours, passed_hours = check_semesters(passed_courses)
    remaining_hours = plan_hours - passed_hours
    print(f"Major Credit Hours {plan_hours}, Passed Hours {passed_hours}")
    # ===================================================================================
    current_semester = 0
    current_year = 1
    if os.path.getsize(filename) == 0:
        current_year = 1
        current_semester = 1
    else:
        # extract that is the current year and semester based on student records input
        for year in passed_courses.keys():
            semesters_list = list(passed_courses[year].keys())
            current_semester = len(semesters_list)
            current_year = year

        if current_semester == 1 or current_semester == 2:
            current_semester += 1
        elif current_semester == 0:
            current_semester = 1
        elif current_semester == 3:
            current_semester = 1
            current_year += 1

    print(f"Current Year : {current_year}, Current Semester : {current_semester}")
    print("=" * 50)
    # 3
    display_with_passed(study_plan, passed_courses)  # display the study plan with passed courses green colored
    priority_pres = calculate_pre()
    Electives = read_electives("Electives.txt")  # Read Elective Courses
    print(f"Electives :\n{Electives}")
    print("=" * 50)
    # 4
    user_preferences = get_user_preferences()
    print("USER PREFERENCES: ")
    print(user_preferences)
    print("=" * 50)
    # 5
    num_of_semesters = int(
        input("Please enter the number of semesters that the script should do the schedule planning for."))

    result = create_schedules(study_plan, passed_courses, user_preferences, Electives,
                              num_of_semesters, current_semester, current_year, priority_pres)
    # Show The Result (Print the Schedules)
    for schedule in result:
        print_schedules(schedule)

    answer = input("Do You Want To Save These Schedules To a Text File (Y/N)")
    if answer == "y" or answer == "Y":
        file_to_saved = "SuggestedCourses.txt"
        with open(file_to_saved, "w") as file:
            file.write("")
        for sche in result:
            print_schedules(sche, file_to_saved)
        continue_flag = 0
        print(f"Schedules Saved To The File {file_to_saved}\nBye!")
    else:
        answer = input("Do You Want To Exist Or Continue (e/E to exit, anything else to continue)")
        if answer == "e" or answer == "E":
            continue_flag = 0
        else:
            continue_flag = 1

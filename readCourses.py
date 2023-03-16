import json
import datetime

with open("CourseBrowser1.json", "r") as file:
    CoursesSemester1 = json.load(file)
with open("CourseBrowser2.json", "r") as file:
    CoursesSemester2 = json.load(file)
with open("CourseBrowser3.json", "r") as file:
    CoursesSemester3 = json.load(file)


class OfferedCourses:
    def __init__(self, code, section, course_type, instructor, schedule):
        self.code = code
        self.section = section
        self.course_type = course_type
        self.instructor = instructor
        self.schedule = schedule
        self.new_code = f"{code}-{course_type}"

    def __str__(self):
        return f"{self.code}-{self.course_type}-{self.section} : {self.instructor}\t {self.schedule}"

    def getCode(self):
        return self.code

    def getSection(self):
        return self.section

    def getCourseType(self):
        return self.course_type

    def getInstructor(self):
        return self.instructor

    def getSchedule(self):
        return self.schedule

    def getDetailedScheduling(self, timing):
        day, time = timing.items()
        # Split the value into start and end time using the '-' separator
        start_time, end_time = time.split(' - ')
        # Convert the start and end time strings to datetime objects
        start_time = datetime.datetime.strptime(start_time, '%H:%M')
        end_time = datetime.datetime.strptime(end_time, '%H:%M')
        # Calculate the time interval between the start and end time
        time_interval = end_time - start_time
        # Print the details of the schedule and the time interval
        return day, time


# Create a new dictionary with split keys
offered_list1: list[OfferedCourses] = []
for key, value in CoursesSemester1.items():
    # Split the key into course code, type, and section number
    code, course_type, section = key.split('-')
    schedule = {}
    instructor = None
    for inner_key in value.keys():
        if inner_key == 'Instructor':
            instructor = value[inner_key]
        elif inner_key is not None:
            schedule[inner_key] = value[inner_key]

    # Add the value to the new dictionary with the new key
    course = OfferedCourses(code, section, course_type, instructor, schedule)
    offered_list1.append(course)

offered_list2: list[OfferedCourses] = []
for key, value in CoursesSemester2.items():
    # Split the key into course code, type, and section number
    code, course_type, section = key.split('-')
    schedule = {}
    instructor = None
    for inner_key in value.keys():
        if inner_key == 'Instructor':
            instructor = value[inner_key]
        elif inner_key is not None:
            schedule[inner_key] = value[inner_key]

    # Add the value to the new dictionary with the new key
    course = OfferedCourses(code, section, course_type, instructor, schedule)
    offered_list2.append(course)

offered_list3: list[OfferedCourses] = []
for key, value in CoursesSemester3.items():
    # Split the key into course code, type, and section number
    code, course_type, section = key.split('-')
    schedule = {}
    instructor = None
    for inner_key in value.keys():
        if inner_key == 'Instructor':
            instructor = value[inner_key]
        elif inner_key is not None:
            schedule[inner_key] = value[inner_key]

    # Add the value to the new dictionary with the new key
    course = OfferedCourses(code, section, course_type, instructor, schedule)
    offered_list3.append(course)


# # Course schedules
# course1 = {'M': '09:00 - 09:50', 'W': '10:00 - 11:15', 'F': '13:30 - 14:20'}
# course2 = {'M': '09:55 - 10:50', 'W': '11:00 - 12:15', 'F': '14:30 - 15:20'}
#
# # Loop through the days of the week
# for day in course1.keys():
#     # Check if both courses have class on the same day
#     if day in course2.keys():
#         # Get the start and end times for both courses
#         start_time1, end_time1 = course1[day].split(' - ')
#         start_time2, end_time2 = course2[day].split(' - ')
#         # Convert the start and end times to datetime objects
#         start_time1 = datetime.datetime.strptime(start_time1, '%H:%M')
#         end_time1 = datetime.datetime.strptime(end_time1, '%H:%M')
#         start_time2 = datetime.datetime.strptime(start_time2, '%H:%M')
#         end_time2 = datetime.datetime.strptime(end_time2, '%H:%M')
#         # Check if the time intervals for both courses intersect
#         if start_time1 < end_time2 and start_time2 < end_time1:
#             print(f"Overlap found on {day} between course 1 and course 2.")

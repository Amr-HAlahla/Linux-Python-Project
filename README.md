# Study Schedule Planner

The Study Schedule Planner is a Python script designed to help students plan their course schedules based on their study plan, passed courses, user preferences, and available electives. This tool automates the process of generating semester-wise schedules to assist students in efficiently planning their academic curriculum.

## Features

- **Study Plan Management**: Allows users to input and manage their study plan, including prerequisites and elective courses.
- **Passed Courses Tracking**: Tracks courses already passed by the student to avoid scheduling them again.
- **User Preferences**: Allows users to set preferences such as maximum credit hours per semester.
- **Elective Courses Support**: Incorporates elective courses into the scheduling process.
- **Automatic Schedule Generation**: Generates semester-wise schedules based on the study plan, passed courses, and user preferences.
- **Output to Text File**: Optionally saves generated schedules to a text file for easy reference.

## Usage

1. **Input Data**:
   - Provide the study plan, including prerequisites and elective courses.
   - Input student records to track passed courses and determine the current year and semester.
   - Input course data from CourseBrowser JSON files.

2. **Set User Preferences**:
   - Specify preferences such as maximum credit hours per semester.

3. **Generate Schedules**:
   - Run the script to generate semester-wise schedules based on the input data and user preferences.

4. **View Schedules**:
   - Review the generated schedules, which include details of courses scheduled for each day and time.

5. **Save Schedules** (Optional):
   - Optionally save the generated schedules to a text file for future reference.

## Dependencies

- Python 3.x
- External libraries: None

## File Structure
study-schedule-planner/
│
├── main.py # Main script for data processing and generating study schedules
├── readCourse.py # Script for reading course data from JSON files
├── CourseBrowser1.json# Input file containing course data for Semester 1
├── CourseBrowser2.json# Input file containing course data for Semester 2
├── CourseBrowser3.json# Input file containing course data for Semester 3
├── study_plan.txt # Input file containing the study plan
├── student_records.txt# Input file containing student records
├── electives.txt # Input file containing elective courses
└── README.md # Documentation and usage instructions


## How to Run

1. Clone the repository to your local machine.
2. Install Python 3.x if not already installed.
3. Navigate to the project directory in the terminal.
4. Run `python main.py` to execute the study schedule planner.
5. Follow the on-screen instructions to input data, set preferences, and generate schedules.

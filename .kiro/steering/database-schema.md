# Education Workshop Database Schema

Database: `education_workshop_db`
All data is scoped to the **College of Engineering** (school_id = 2) and its five departments.

## Tables

### student
Student records including admissions and academic performance.
Columns: student_id (PK), first_name, last_name, gender ('M'/'F'), birth_date, email_address, admitted ('1'/'0'), enrolled ('1'/'0'), parent_alum ('1'=alumni), parent_highest_ed (FK→ed_level.ed_level_id), first_gen_hed_student ('1'=first gen), high_school_gpa, was_hs_athlete_ind, home_state_name, admit_type ('Regular'/'Early Action'/'Early Decision'), private_hs_indicator, multiple_majors_indicator, secondary_class_percentile, department_id (FK→department), admit_semester_id (FK→semester), first_year_gpa, cumulative_gpa, enroll_status ('enrolled'/'admitted'/'declined'), planned_grad_semester_id (FK→semester, 0 if not enrolled)

### course
Course catalogue.
Columns: course_id (PK), course_name, course_level ('100','200','300'), course_code (e.g. 'COMP-0100','AERO-0200'), school_id (FK→school), department_id (FK→department)

### course_registration
Which students registered for which courses.
Columns: date_registered, date_dropped ('0001-01-01' if not dropped), student_id (FK→student), course_id (FK→course), status ('completed'), semester_id (FK→semester), update_ts

### course_outcome
Student grades per course.
Columns: student_id (FK→student), course_id (FK→course), semester_id (FK→semester), score (numeric), letter_grade ('A+','A','A-','B+','B','B-','C','C+','D','F')

### course_schedule
When and where courses are offered.
Columns: course_id (FK→course), semester_id (FK→semester), staff_id (FK→faculty), lecture_days, lecture_start_hour, lecture_duration, lab_days, lab_start_hour, lab_duration

### degree_plan
Planned course sequences per student.
Columns: student_id (FK→student), course_id (FK→course), course_seq_no, status ('completed'/'pending'), is_major_ind ('1'=major req/'0'=elective), semester_seq_no

### department
Columns: department_id (PK), department_name ('Aeronautics','Computer Science','Data Science','Engineering','Environment and Natural Resources'), department_code ('AERO','COMP','DATA','ENGI','ENVI'), school_id (FK→school, always 2)

### school
Columns: school_id (PK, only 2), school_name ('College of Engineering'), relative_website_url, university_id (FK→university)

### faculty
Columns: faculty_id (PK), first_name, last_name, gender, department_id (FK→department), tenure_years, is_tenured, title ('professor'/'associate professor'/'assistant instructor'/'instructor'), dept_chair

### semester
Columns: semester_id (PK, 29–43), start_date, end_date, term_name ('Fall'/'Spring'), semester_year, school_year_name (e.g. '2014-2015'). Spans Fall 2014 to Fall 2021.

### ed_level
Parent education level lookup.
Columns: ed_level_id (PK, 0–9), ed_level_code (e.g. 'HS Grad','Bachelors'), ed_level_desc

### university
Columns: university_id (PK), university_name, website_url

## Key Relationships
- student.department_id → department.department_id
- student.admit_semester_id / planned_grad_semester_id → semester.semester_id
- student.parent_highest_ed → ed_level.ed_level_id
- course.department_id → department.department_id
- course_registration.student_id → student.student_id
- course_registration.course_id → course.course_id
- course_registration.semester_id → semester.semester_id
- course_outcome: same FKs as course_registration
- course_schedule.course_id → course, .semester_id → semester, .staff_id → faculty
- degree_plan.student_id → student, .course_id → course
- faculty.department_id → department.department_id

## Important Notes
- All column types are STRING in Athena. Cast for aggregations: CAST(cumulative_gpa AS DOUBLE), CAST(score AS INTEGER).
- Course codes follow pattern DEPT-NNNNN (e.g. COMP-0100, AERO-0200).
- course_registration.status only contains 'completed' in this dataset.
- degree_plan.status is 'completed' or 'pending'.
- student.enroll_status is 'enrolled', 'admitted', or 'declined'.

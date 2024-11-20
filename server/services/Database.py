"""
"""

# IMPORTS
import pandas as pd
import os
from flask import current_app
from sqlalchemy import text, delete, insert, update
from datetime import datetime
from sqlalchemy import or_

from models.Course import Course
from models.Student import Student
from models.Preferences import Preferences
from models.Enrollments import enrollments
from models.User import User
from models.ScheduleProgression import ScheduleProgression

from exceptions import InvalidUploadFile, InvalidFileType, DataNotFound, DatabaseError, DataAlreadyExists, InvalidEmailAddress, EmailAddressAlreadyInUse, UserNotFound


# CONSTANTS
DROP_COURSE_COLUMNS = [
    "Hrs",
    "Block Code (swvmday)",
    "Block Conflicts (swvmday)",
    "Instructor Conflicts (swvmday)",
    "Instructor Conflicts (swvmday) = 'Y'",
    "Meeting Day No. (swvmday)",
    "Room Conflicts (swvmday)",
    "Room Conflicts (swvmday)  =  'Y'",
    "Sorted By",
    "Sort Order",
    "Time",
]


# DATABASE CLASS
class Database:
    """ """

    def __init__(self, db):
        """ """
        self.db = db

    def bulk_course_update(self, file) -> list:
        """
        """
        if not file.filename.endswith(".xlsx"):
            raise InvalidFileType("Invalid file format. Please upload an XLSX file.")
        try:
            df = self.parse_bulk_course_upload_file(file)
            self.set_all_student_is_completed_and_is_approved_by_program_heads_to_false()
            student_enrollments = self.get_enrollments_by_student()
            self.upload_courses_to_database(df)
            self.update_student_enrollments(student_enrollments)
        except:
            raise InvalidUploadFile("Invalid file format. Error processing the file.")

    def update_student_enrollments(self, student_enrollments: dict):
        """
        """
        for student_id, groupings in student_enrollments.items():
            groupings = list(groupings)
            self.add_courses_by_groupings(student_id, groupings)

    def get_enrollments_by_student(self) -> dict:
        """
        """
        all_enrollments = self.db.session.query(enrollments).all()
        student_enrollments = {}
        for enrollment in all_enrollments:
            course_grouping = self.db.session.query(Course).filter(Course.id == enrollment.course_id).first().course_grouping
            if enrollment.student_id in student_enrollments:
                student_enrollments[enrollment.student_id].add(course_grouping)
            else:
                student_enrollments[enrollment.student_id] = {course_grouping}
        return student_enrollments

    def bulk_course_replace(self, file) -> list:
        """
        Save the bulk course upload file to the database.

        Args:
        -----
        file (FileStorage): The file to save.

        Returns:
        --------
        list: A list of invalid rows.

        Notes:
        ------
        1. The file is validated to ensure it is an XLSX file.
        2. The file is parsed to remove unnecessary columns.
        3. The data is normalized and uploaded to the database.
        4. Invalid rows are returned.

        Example:
        --------
        >>> db = Database()
        >>> db.save_bulk_course_upload_file(file)
        ... # Invalid rows returned
        ... # Course data uploaded to the database
        """
        if not file.filename.endswith(".xlsx"):
            raise InvalidFileType("Invalid file format. Please upload an XLSX file.")
        try:
            df = self.parse_bulk_course_upload_file(file)
            self.set_all_student_is_completed_and_is_approved_by_program_heads_to_false()
            return self.upload_courses_to_database(df)
        except:
            raise InvalidUploadFile("Invalid file format. Error processing the file.")

    def set_all_student_is_completed_and_is_approved_by_program_heads_to_false(self):
        """
        """
        try:
            self.db.session.query(Student).update({Student.is_completed: False, Student.is_approved_by_program_heads: False})
            self.db.session.query(ScheduleProgression).filter(ScheduleProgression.date == datetime.now().date()).update({ScheduleProgression.num_schedules_completed: 0, ScheduleProgression.num_approvals_from_program_heads: 0})
            self.db.session.commit()
        except Exception as e:
            raise DatabaseError(f"Error updating student: {str(e)}")

    def parse_bulk_course_upload_file(self, file) -> pd.DataFrame:
        """
        Parse the bulk course upload file to remove unnecessary columns.

        Args:
        -----
        file (FileStorage): The file to parse.

        Returns:
        --------
        pd.DataFrame: The parsed DataFrame.

        Notes:
        ------
        1. The file is read as a DataFrame.
        2. The columns are cleaned by removing special characters.
        3. The unnecessary columns are removed.
        4. The instructor names are cleaned.
        5. The data is grouped by the columns and the instructors are aggregated.
        6. The DataFrame is returned.

        Example:
        --------
        >>> db = Database()
        >>> db.parse_bulk_course_upload_file(file)
        ... # DataFrame returned

        Author: ``@ChinaiArman``
        """
        df = pd.read_excel(file)
        df = df.map(
            lambda x: (
                x.replace("*", "").replace("\n", "").strip()
                if isinstance(x, str)
                else x
            )
        )
        df.columns = df.columns.map(
            lambda x: x.replace("*", "").replace("\n", "").strip()
        )
        df.drop(columns=DROP_COURSE_COLUMNS, inplace=True)
        df["Instructor"] = df["Instructor"].map(lambda x: " ".join(x.split(", ")[::-1]))
        df = (
            df.groupby([column for column in df.columns if column != "Instructor"])
            .agg({"Instructor": lambda x: ",".join(set(x))})
            .reset_index()
        )
        return df

    def normalize_course_data(self, row: pd.Series) -> pd.Series:
        """
        Normalize the course data.

        Args:
        -----
        row (pd.Series): The row to normalize.

        Returns:
        --------
        pd.Series: The normalized row.

        Notes:
        ------
        1. Matches the column requirements for the Course model.

        Example:
        --------
        >>> db = Database()
        >>> db.normalize_course_data(row)
        ... # Normalized row returned
        """
        row["Status"] = "Active" if row["Status"] == "Active" else "Inactive"
        row["Block"] = row["Block"][:8]
        row["CRN"] = int(row["CRN"])
        row["Course"] = row["Course"][:8]
        row["Type"] = row["Type"][:3]
        row["Day"] = row["Day"][:3]
        row["Begin Time"] = datetime.strptime(
            str(int(row["Begin Time"])), "%H%M"
        ).time()
        row["End Time"] = datetime.strptime(str(int(row["End Time"])), "%H%M").time()
        row["Bldg/Room"] = row["Bldg/Room"][:10]
        row["Start Date"] = datetime.strptime(
            str(row["Start Date"]), "%Y-%m-%d %H:%M:%S"
        ).date()
        row["End Date"] = datetime.strptime(
            str(row["End Date"]), "%Y-%m-%d %H:%M:%S"
        ).date()
        row["Max."] = int(row["Max."])
        row["Act."] = int(row["Act."])
        row["FT/PT"] = True if row["FT/PT"] == "FT" else False
        row["Term Code (swvmday)"] = int(row["Term Code (swvmday)"])
        row["Instructor"] = row["Instructor"][:512]
        return row

    def upload_courses_to_database(self, df: pd.DataFrame) -> list:
        """
        Upload the courses to the database.

        Args:
        -----
        df (pd.DataFrame): The DataFrame to upload.

        Returns:
        --------
        list: A list of invalid rows.

        Notes:
        ------
        1. The courses are uploaded to the database.
        2. Invalid rows are returned.

        Example:
        --------
        >>> db = Database()
        >>> db.upload_courses_to_database(df)
        ... # Invalid rows returned
        ... # Courses uploaded to the database
        """
        self.db.session.query(enrollments).delete()
        self.db.session.query(Course).delete()
        self.db.session.commit()
        self.db.session.execute(text("ALTER TABLE courses AUTO_INCREMENT = 1"))
        invalid_rows = []
        for _, row in df.iterrows():
            try:
                row = self.normalize_course_data(row)
                course = Course(
                    status=row["Status"],
                    block=row["Block"],
                    crn=row["CRN"],
                    course_grouping=row["Block"] + row["Course"],
                    course_code=row["Course"],
                    course_type=row["Type"],
                    day=row["Day"],
                    begin_time=row["Begin Time"],
                    end_time=row["End Time"],
                    building_room=row["Bldg/Room"],
                    start_date=row["Start Date"],
                    end_date=row["End Date"],
                    max_capacity=row["Max."],
                    num_enrolled=row["Act."],
                    is_full_time=row["FT/PT"],
                    term_code=row["Term Code (swvmday)"],
                    instructor=row["Instructor"],
                )
                self.db.session.add(course)
            except:
                invalid_rows.append(
                    {
                        "crn": row["CRN"],
                        "course": row["Course"],
                        "block": row["Block"],
                        "instructor": row["Instructor"],
                    }
                )
        self.db.session.commit()
        return invalid_rows

    def bulk_student_replace(self, file) -> list:
        """ 
        Save the bulk student upload file to the database.

        Args:
        -----
        file (FileStorage): The file to save.

        Returns:
        --------
        list: A list of invalid rows.

        Notes:
        ------
        1. The file is validated to ensure it is a CSV file.
        2. The file is read as a DataFrame.
        3. The data is normalized and uploaded to the database.
        4. Invalid rows are returned.

        Example:
        --------
        >>> db = Database()
        >>> db.save_bulk_student_upload_file(file)
        ... # Invalid rows returned
        ... # Student data uploaded to the database
        """
        if not file.filename.endswith(".csv"):
            raise InvalidFileType("Invalid file format. Please upload an CSV file.")
        try:
            df = pd.read_csv(file)
            self.db.session.query(ScheduleProgression).filter(ScheduleProgression.date == datetime.now().date()).update({ScheduleProgression.num_schedules_completed: 0, ScheduleProgression.num_approvals_from_program_heads: 0})
            return self.upload_students_to_database(df)
        except:
            raise InvalidUploadFile("Invalid file format. Error processing the file.")

    def normalize_student_data(self, row: pd.Series) -> pd.Series:
        """ 
        Normalize the student data.

        Args:
        -----
        row (pd.Series): The row to normalize.

        Returns:
        --------
        pd.Series: The normalized row.
        
        Example:
        --------
        >>> db = Database()
        >>> db.normalize_student_data(row)
        ... # Normalized row returned
        """
        row["BCIT Student Number"] = row["BCIT Student Number"][:9]
        row["Legal First Name"] = row["Legal First Name"][:50]
        row["Legal Last Name"] = row["Legal Last Name"][:50]
        row["BCIT Email"] = row["BCIT Email"][:100]
        row["Term Code"] = int(row["Term Code"])
        preference_columns = [
            col for col in row.index if col.startswith("Course Code Preference")
        ]
        for col in preference_columns:
            row[col] = row[col][:8]
        return row

    def upload_students_to_database(self, df: pd.DataFrame) -> list:
        """ 
        Upload the students to the database.
        
        Args:
        -----
        df (pd.DataFrame): The DataFrame to upload.
        
        Returns:
        --------
        list: A list of invalid rows.
        
        Example:
        --------
        >>> db = Database()
        >>> db.upload_students_to_database(df)
        ...
        """
        try:
            self.db.session.query(enrollments).delete()
            self.db.session.query(Preferences).delete()
            self.db.session.query(Student).delete()
            invalid_rows = []
            for _, row in df.iterrows():
                try:
                    row = self.normalize_student_data(row)
                    student = Student(
                        id=row["BCIT Student Number"],
                        first_name=row["Legal First Name"],
                        last_name=row["Legal Last Name"],
                        email=row["BCIT Email"],
                        term_code=row["Term Code"],
                    )
                    self.db.session.add(student)

                    preferences = [row[f"Course Code Preference #{i}"] for i in range(1, 9) if row[f"Course Code Preference #{i}"] and row[f"Course Code Preference #{i}"] != ""] 
                    self.add_student_preferences(student.id, preferences)

                except Exception as e:
                    invalid_rows.append({"id": row["BCIT Student Number"]})
            self.db.session.commit()
            return invalid_rows
        except Exception as e:
            raise DatabaseError(f"Error uploading students to the database: {str(e)}")

    def bulk_student_update(self, file) -> list:
        """ 
        Save the bulk student upload file to the database.

        Args:
        -----
        file (FileStorage): The file to save.

        Returns:
        --------
        list: A list of invalid rows.

        Notes:
        ------
        1. The file is validated to ensure it is a CSV file.
        2. The file is read as a DataFrame.
        3. The data is normalized and uploaded to the database.
        4. Invalid rows are returned.

        Example:
        --------
        >>> db = Database()
        >>> db.save_bulk_student_upload_file(file)
        ...
        """
        if not file.filename.endswith(".csv"):
            raise InvalidFileType("Invalid file format. Please upload an CSV file.")
        try:
            df = pd.read_csv(file)
            return self.update_students_in_database(df)
        except:
            raise InvalidUploadFile("Invalid file format. Error processing the file.")
        
    def update_students_in_database(self, df: pd.DataFrame) -> list:
        """ 
        Update existing students in the database, only modifying fields that have changed.

        Args:
        -----
        df (pd.DataFrame): The DataFrame containing student updates.

        Returns:
        --------
        list: A list of invalid rows.

        Notes:
        ------
        1. Students are matched using BCIT Student Number
        2. Only modified fields are updated
        3. Invalid rows are tracked and returned
        4. No data is deleted from the enrollments table

        Example:
        --------
        >>> db = Database()
        >>> result = db.update_students_in_database(df)
        >>> print(f"Updated {len(result['updated_students'])} students")
        """
        results = {
            'invalid_rows': [],
            'updated_students': [],
            'added_students': []
        }

        for _, row in df.iterrows():
            try:
                # Normalize the incoming data
                row = self.normalize_student_data(row)
                
                # Find existing student by BCIT Student Number
                existing_student = self.db.session.query(Student).filter(
                    Student.id == row["BCIT Student Number"]
                ).first()

                if not existing_student:
                    results['added_students'].append({
                        "id": row["BCIT Student Number"]
                    })
                    student = Student(
                        id=row["BCIT Student Number"],
                        first_name=row["Legal First Name"],
                        last_name=row["Legal Last Name"],
                        term_code=row["Term Code"],
                        email=row["BCIT Email"],
                        is_completed=False,
                        is_approved_by_program_heads=False
                    )
                    self.db.session.add(student)
                    preferences = [row[f"Course Code Preference #{i}"] for i in range(1, 9) if row[f"Course Code Preference #{i}"] and row[f"Course Code Preference #{i}"] != ""]
                    self.add_student_preferences(student.id, preferences)
                    continue

                # Create dictionary of new values
                new_values = {
                    "first_name": row["Legal First Name"],
                    "last_name": row["Legal Last Name"],
                    "email": row["BCIT Email"],
                    "term_code": row["Term Code"]
                }

                # Track if any changes were made
                changes_made = False
                fields = []

                # Compare and update only changed fields
                for field, new_value in new_values.items():
                    current_value = getattr(existing_student, field)
                    if current_value != new_value:
                        setattr(existing_student, field, new_value)
                        fields.append(field)
                        changes_made = True

                if changes_made:
                    results['updated_students'].append({
                        "id": row["BCIT Student Number"],
                        "fields": fields
                    })

            except Exception as e:
                results['invalid_rows'].append({
                    "id": row.get("BCIT Student Number", "Unknown"),
                    "error": str(e)
                })

        # Commit all changes at once
        try:
            self.db.session.commit()
        except Exception as e:
            self.db.session


    def get_student_by_id(self, id: int) -> dict:
        """
        Get the student by ID.

        Args:
        -----
        id (int): The student ID.

        Returns:
        --------
        dict: The student information.

        Example:
        --------
        >>> db = Database()
        >>> db.get_student_by_id(1)
        ... {"id": 1, "firstName": "John", "lastName": "Doe", "selection": [], "courses": []}
        """
        try:
            student = self.db.session.query(Student).filter(Student.id == id).first()
        except Exception as e:
            raise DatabaseError(f"Error querying into database: {str(e)}")
        if not student:
            raise DataNotFound(f"Unable to find student by ID: {id}")
        return student.to_dict()

    def create_student(self, data) -> dict:
        """
        Create a new student.

        Args:
        -----
        data (dict): The student data.

        Returns:
        --------
        dict: The response message.

        Example:
        --------
        >>> db = Database()
        >>> student = Student(1, "John", "Doe")
        >>> db.create_student(student)
        ... {"message": "Student created successfully"}
        """
        try:
            print(data.get("preferences"))
            if self.db.session.query(Student).filter(Student.id == data.get("id")).first():
                raise DataAlreadyExists("Student already exists")
            student = {
                "BCIT Student Number": data.get("id"),
                "Legal First Name": data.get("first_name"),
                "Legal Last Name": data.get("last_name"),
                "Term Code": data.get("term_code"),
                "BCIT Email": data.get("email")
            }
            for i, preference in enumerate(data.get("preferences")):
                student[f"Course Code Preference #{i+1}"] = preference
            student = pd.Series(student)
            row = self.normalize_student_data(student)
            student = Student(
                id=row["BCIT Student Number"],
                first_name=row["Legal First Name"],
                last_name=row["Legal Last Name"],
                term_code=row["Term Code"],
                email=row["BCIT Email"],
                is_completed=False,
                is_approved_by_program_heads=False
            )
            self.db.session.add(student)

            preferences = [row[f"Course Code Preference #{i}"] for i in range(1, len(data.get("preferences"))) if row[f"Course Code Preference #{i}"]]

            self.change_student_preferences(student.id, preferences) 
            self.db.session.commit()
            return
        except Exception as e:
            raise DatabaseError(f"Error creating student: {str(e)}")

    def update_student(self, id: int, data: dict) -> dict:
        """
        Update the student by ID.

        Args:
        -----
        id (int): The student ID.
        data (dict): The student data.

        Returns:
        --------
        dict: The response message.

        Example:
        --------
        >>> db = Database()
        >>> db.update_student(1, {"first_name": "John", "last_name": "Doe", "term_code": 202101})
        ... 

        """
        try:
            student = self.db.session.query(Student).filter(Student.id == id).first()
            if not student:
                raise DataNotFound(f"Student with ID not found: {id}")
            
            updatable_columns = ['first_name', 'last_name', 'term_code', 'email', 'is_completed']
            for key, value in data.items():
                if key in updatable_columns and value is not None:
                    setattr(student, key, value)

            if data.get("preferences"):
                self.change_student_preferences(id, data.get("preferences"))

            if data.get("courses"):
                self.replace_courses_for_student(id, data.get("courses"))

            self.db.session.commit()
            return
        except Exception as e:
            raise DatabaseError(f"Error updating student: {str(e)}")

    def delete_student(self, id: int) -> dict:
        """
        Delete the student by ID.

        Args:
        -----
        id (int): The student ID.

        Returns:
        --------
        dict: The response message.

        Example:
        --------
        >>> db = Database()
        >>> db.delete_student(1)
        ... {"message": "Student deleted successfully"}
        """
        try:
            student = self.db.session.query(Student).filter(Student.id == id).first()
            if not student:
                raise DataNotFound(f"Student with ID not found: {id}")
            
            # if student marked as completed or approved by program heads, reduce the count
            self.db.session.query(ScheduleProgression).filter(ScheduleProgression.date == datetime.now().date()).update({ScheduleProgression.num_schedules_completed: ScheduleProgression.num_schedules_completed - (1 if student.is_completed else 0), ScheduleProgression.num_approvals_from_program_heads: ScheduleProgression.num_approvals_from_program_heads - (1 if student.is_approved_by_program_heads else 0)})
            self.delete_student_preferences(id)
            self.db.session.query(enrollments).filter(enrollments.c.student_id == id).delete()
            self.db.session.delete(student)
            self.db.session.commit()
            return
        except Exception as e:
            raise DatabaseError(f"Error deleting student: {str(e)}")

    def get_all_students(self) -> list:
        """
        Get all students.

        Returns:
        --------
        list: A list of all students.

        Example:
        --------
        >>> db = Database()
        >>> db.get_all_students()
        ... [{"id": 1, "firstName": "John", "lastName": "Doe", "selection": [], "courses": []}]
        """
        try:
            students = self.db.session.query(Student).all()
        except Exception as e:
            raise DatabaseError(f"Error querying into database: {str(e)}")
        return [student.to_dict() for student in students]

    def export_students(self) -> pd.DataFrame:
        """
        Export all students.

        Returns:
        --------
        pd.DataFrame: The DataFrame of all students.

        Example:
        --------
        >>> db = Database()
        >>> db.export_students()
        ... # DataFrame returned
        """
        try:
            students = self.db.session.query(Student).all()
        except Exception as e:
            raise DatabaseError(f"Error querying into database: {str(e)}")
        df = pd.DataFrame([student.to_dict() for student in students])
        file_path = "exports/students.csv"
        df.to_csv(file_path, index=False)
        return file_path

    def add_student_preferences(self, student_id: int, courses: list) -> dict:
        """
        Add student preferences to the database.

        Args:
        -----
        student_id (int): The student ID.
        courses (list): The list of course codes.

        Returns:
        --------
        dict: The response message.

        Example:
        --------
        >>> db = Database()
        >>> db.add_student_preferences(1, ["COMP 1001", "COMP 1002", "COMP 1003"])
        ... 
        """
        try:
            for priority, course_code in enumerate(courses, start=1):
                preference = Preferences(
                                student_id=student_id,
                                priority=priority,
                                preference=course_code
                            )
                self.db.session.add(preference)
            return
        except Exception as e:
            raise DatabaseError(f"Error adding student preference: {str(e)}")
    
    def change_student_preferences(self, student_id: int, courses: list) -> dict:
        """
        Change student preferences in the database.

        Args:
        -----
        student_id (int): The student ID.
        courses (list): The list of course codes.

        Returns:
        --------
        dict: The response message.

        Example:
        --------
        >>> db = Database()
        >>> db.change_student_preferences(1, ["COMP 1001", "COMP 1002", "COMP 1003"])
        ...
        """
        try:
            self.delete_student_preferences(student_id)
            self.add_student_preferences(student_id, courses)
        except Exception as e:
            raise DatabaseError(f"Error adding student preference: {str(e)}")
        
    def delete_student_preferences(self, student_id):
        """
        Delete student preferences from the database for the student.

        Args:
        -----
        student_id (int): The student ID.

        Returns:
        --------
        dict: The response message.

        Example:
        --------
        >>> db = Database()
        >>> db.delete_student_preferences(1)
        ...
        """
        try:
            self.db.session.query(Preferences).filter(Preferences.student_id == student_id).delete()
            return
        except Exception as e:
            raise DatabaseError(f"Error deleting student preferences: {str(e)}")

    def add_course_to_student(self, student_id: int, course_id: int) -> dict:
        """
        Add a course to a student.

        Args:
        -----
        student_id (int): The student ID.
        course_id (int): The course ID.

        Returns:
        --------
        dict: The response message.

        Example:
        --------
        >>> db = Database()
        >>> db.add_course_to_student(1, 1)
        ...
        """

        try:
            student = self.db.session.query(Student).filter(Student.id == student_id).first()
            if not student:
                raise DataNotFound(f"Student with ID not found: {student_id}")
            
            course = self.db.session.query(Course).filter(Course.id == course_id).first()
            if not course:
                raise DataNotFound(f"Course with ID not found: {course_id}")
            
            enrollment = self.db.session.query(enrollments).filter(enrollments.c.student_id == student_id, enrollments.c.course_id == course_id).first()
            if enrollment:
                raise DataAlreadyExists(f"Student is already enrolled in course: {course_id}")
            else :
                self.db.session.execute(enrollments.insert().values(student_id=student_id, course_id=course_id))

            self.db.session.commit()
            return
        except Exception as e:
            raise DatabaseError(f"Error adding course to student: {str(e)}")   

    def remove_course_from_student(self, student_id: int, course_id: int) -> dict:
        """
        Remove a course from a student.

        Args:
        -----
        student_id (int): The student ID.
        course_id (int): The course ID.

        Returns:
        --------
        dict: The response message.

        Example:
        --------
        >>> db = Database()
        >>> db.remove_course_from_student(1, 1)
        ...
        """
        try:
            student = self.db.session.query(Student).filter(Student.id == student_id).first()
            if not student:
                raise DataNotFound(f"Student with ID not found: {student_id}")
            
            course = self.db.session.query(Course).filter(Course.id == course_id).first()
            if not course:
                raise DataNotFound(f"Course with ID not found: {course_id}")
            
            enrollment = self.db.session.query(enrollments).filter(enrollments.c.student_id == student_id, enrollments.c.course_id == course_id).first()
            if not enrollment:
                raise DataNotFound(f"Student is not enrolled in course: {course_id}")
            else:
                self.db.session.execute(enrollments.delete().where(enrollments.c.student_id == student_id).where(enrollments.c.course_id == course_id))

            self.db.session.commit()
            return
        except Exception as e:
            raise DatabaseError(f"Error removing course from student: {str(e)}") 
        
    def replace_all_courses_for_student(self, student_id: int, course_list: str) -> dict:
        """
        Replace all courses for a student.

        Args:
        -----
        student_id (int): The student ID.
        course_list (str): The comma-separated list of course IDs.

        Returns:
        --------
        dict: The response message.

        Example:
        --------
        >>> db = Database()
        >>> db.replace_all_courses_for_student_route(1, "1,2,3")
        ...
        """
        try:
            new_courses = course_list.split(',')
            new_courses = {int(course) for course in new_courses}

            student = self.db.session.query(Student).filter(Student.id == student_id).first()
            if not student:
                raise DataNotFound(f"Student with ID not found: {student_id}")

            existing_courses = self.db.session.query(Course.id).filter(Course.id.in_(new_courses)).all()
            existing_course_ids = {course.id for course in existing_courses} 
            invalid_courses = [course for course in new_courses if course not in existing_course_ids]
            
            if invalid_courses:
                raise DataNotFound(f"Invalid course ID(s) found: {invalid_courses}")

            self.db.session.execute(enrollments.delete().where(enrollments.c.student_id == student_id))
            self.db.session.commit()

            new_enrollments = [{'student_id': student_id, 'course_id': course_id} for course_id in new_courses]
            
            self.db.session.execute(enrollments.insert(), new_enrollments)
            self.db.session.commit()
            return 
        except Exception as e:
            raise DatabaseError(f"Error replacing all courses for student: {str(e)}")

    def get_course_by_course_grouping(self, course_grouping):
        try:
            courses = self.db.session.query(Course).filter(Course.course_grouping == course_grouping).all()
            for course in courses:
                course.start_date = course.start_date.strftime("%Y-%m-%d")
                course.end_date = course.end_date.strftime("%Y-%m-%d")
                course.begin_time = course.begin_time.strftime("%H:%M")
                course.end_time = course.end_time.strftime("%H:%M")
            course_reprs = [course.to_dict() for course in courses]
            return course_reprs
        except Exception as e:
            raise DatabaseError(f"Error fetching course by course grouping: {str(e)}")

    def get_all_course_groupings_by_course_code(self, course_code, student_id):
        student = self.db.session.query(Student).filter(Student.id == student_id).first()
        try:
            courses = self.db.session.query(Course).filter(Course.course_code == course_code).all()
            groupings_to_remove = []
            for course in courses:
                if course.status != "Active":
                    groupings_to_remove.append(course.course_grouping)
                if course.num_enrolled >= course.max_capacity and student not in course.students:
                    groupings_to_remove.append(course.course_grouping)
                course.start_date = course.start_date.strftime("%Y-%m-%d")
                course.end_date = course.end_date.strftime("%Y-%m-%d")
                course.begin_time = course.begin_time.strftime("%H:%M")
                course.end_time = course.end_time.strftime("%H:%M")
            for grouping in groupings_to_remove:
                courses = [course for course in courses if course.course_grouping != grouping]
            course_reprs = [course.to_dict() for course in courses]
            course_groupings = {}
            for course in course_reprs:
                if course["course_grouping"] not in course_groupings:
                    course_groupings[course["course_grouping"]] = []
                course_groupings[course["course_grouping"]].append(course)
            return course_groupings
        except Exception as e:
            raise DatabaseError(f"Error fetching course by course code: {str(e)}")

    def get_course_by_course_id(self, id):
        try:
            course = self.db.session.query(Course).filter(Course.id == id).first()
            if not course:
                raise DataNotFound(f"Course with ID not found: {id}")
            course.start_date = course.start_date.strftime("%Y-%m-%d")
            course.end_date = course.end_date.strftime("%Y-%m-%d")
            course.begin_time = course.begin_time.strftime("%H:%M")
            course.end_time = course.end_time.strftime("%H:%M")
            return course.to_dict()
        except Exception as e:
            raise DatabaseError(f"Error fetching course by ID: {str(e)}")

    def get_course_students(self, course_grouping):
        try:
            courses = self.db.session.query(Course).filter(Course.course_grouping == course_grouping).all()
            if not courses:
                raise DataNotFound(f"Course with course grouping not found: {course_grouping}")
            students = []
            for course in courses:
                students.extend([student.to_dict() for student in course.students])
            return students
        except Exception as e:
            raise DatabaseError(f"Error fetching course students: {str(e)}")

    def get_user_by_email(self, email: str) -> User:
        """
        Get a user by email address.
        
        Args
        ----
        email (str): User email address.
        
        Returns
        -------
        user (User): The user object.

        Raises
        ------
        InvalidEmailAddress: If the email address is invalid.
        """
        user = self.db.session.query(User).filter(User.email == email).first()
        if not user:
            raise InvalidEmailAddress()
        return user
    
    def create_user(self, username, email, password, verification_code) -> User:
        """
        Create a new user in the database.

        Args
        ----
        email (str): User email address.
        password (str): User password.
        verification_code (str): User verification code.

        Returns
        -------
        user (User): The user object.

        Raises
        ------
        EmailAddressAlreadyInUse: If the email address is already in use.
        """
        if self.db.session.query(User).filter(User.email == email).first():
            raise EmailAddressAlreadyInUse()
        user = User(username=username, email=email, password=password, verification_code=verification_code, reset_code=None, is_verified=False, is_admin=False)
        self.db.session.add(user)
        self.db.session.commit()
        return user
    
    def update_password(self, user: User, password: str) -> None:
        """
        Update the password for a user.

        Args
        ----
        user (User): The user object.
        password (str): The new user password.

        Returns
        -------
        None
        """
        user.password = password
        user.reset_code = None
        self.db.session.commit()
        return
    
    def update_reset_code(self, user: User, reset_code: str) -> None:
        """
        Update the reset code for a user.

        Args
        ----
        user (User): The user object.
        reset_code (str): The new reset code.

        Returns
        -------
        None
        """
        user.reset_code = reset_code
        self.db.session.commit()
        return
    
    def verify_user(self, user: User) -> None:
        """
        Verify a user.

        Args
        ----
        user (User): The user object.

        Returns
        -------
        None
        """
        user.is_verified = True
        user.verification_code = None
        self.db.session.commit()
        return
    
    def get_user_by_id(self, user_id: int) -> User:
        """
        Get a user by ID.

        Args
        ----
        user_id (int): User ID.

        Returns
        -------
        user (User): The user object.

        Raises
        ------
        UserNotFound: If the user is not found.
        """
        user = self.db.session.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotFound()
        return user
    
    def get_all_users_info(self) -> list[dict]:
        """
        Get all users.

        Returns
        -------
        users (list[dict]): A list of dicts, each containing specified information of a user.
        """
        users = self.db.session.query(User.id, User.username, User.email, User.is_verified, User.is_admin).all()
        if not users:
            raise UserNotFound()
        users = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_verified": user.is_verified,
                "is_admin": user.is_admin
            }
            for user in users
        ]
        return users


    def change_user_admin_status(self, user_id: int) -> None:
        """
        Change the admin status of a user.

        Args
        ----
        user_id (int): User ID.

        Returns
        -------
        None
        """
        try:
            user = self.get_user_by_id(user_id)
            user.is_admin = not user.is_admin
            self.db.session.commit()
        except Exception as e:
            raise DatabaseError(f"Error changing user admin status: {str(e)}")
        return

    def update_user_info(self, user_id: int, username: str, email: str) -> None:
        """
        Update user information.

        Args
        ----
        user_id (int): User ID.
        username (str): User username.
        email (str): User email.

        Returns
        -------
        None
        """
        try:
            user = self.get_user_by_id(user_id)
            user.username = username
            user.email = email
            self.db.session.commit()
        except Exception as e:
            raise DatabaseError(f"Error updating user information: {str(e)}")

    def delete_user(self, user_id: int) -> None:
        """
        Delete a user by ID.

        Args
        ----
        user_id (int): User ID.

        Returns
        -------
        None
        """
        # check if user is_admin before delete
        user = self.get_user_by_id(user_id)
        if user.is_admin:
            raise DatabaseError("Cannot delete admin user")
        self.db.session.query(User).filter(User.id == user_id).delete()
        self.db.session.commit()
        return

    def create_unverified_user(self, username: str, email: str, password: str, verification_code: str) -> User:
        """
        Create a new unverified user with an initial password.
        
        Args
        ----
        username (str): The username
        email (str): The email address
        password (str): The initial password (encrypted)
        verification_code (str): The verification code
        
        Returns
        -------
        User: The created user object
        
        Raises
        ------
        EmailAddressAlreadyInUse: If the email is already registered
        DatabaseError: If there's an error creating the user
        """
        try:
            if self.db.session.query(User).filter(User.email == email).first():
                raise EmailAddressAlreadyInUse()
            
            user = User(
                username=username,
                email=email,
                password=password,  # Now we set the initial password
                verification_code=verification_code,
                reset_code=None,
                is_verified=False,
                is_admin=False
            )
            self.db.session.add(user)
            self.db.session.commit()
            return user
        except Exception as e:
            self.db.session.rollback()
            raise DatabaseError(f"Error creating unverified user: {str(e)}")

    def get_user_by_verification_code(self, verification_code: str) -> User:
        """
        Get a user by verification code.
        
        Args
        ----
        verification_code (str): The verification code
        
        Returns
        -------
        User: The user object if found
        
        Raises
        ------
        UserNotFound: If no user is found with the given verification code
        """
        try:
            user = self.db.session.query(User).filter(User.verification_code == verification_code).first()
            if not user:
                raise UserNotFound("Invalid verification code")
            return user
        except Exception as e:
            raise DatabaseError(f"Error fetching user by verification code: {str(e)}")

    def verify_user_with_password(self, user: User, password: str) -> None:
        """
        Verify a user and set their initial password.
        
        Args
        ----
        user (User): The user object to verify
        password (str): The encrypted password to set
        
        Returns
        -------
        None
        
        Raises
        ------
        DatabaseError: If there's an error updating the user
        """
        try:
            user.password = password
            user.is_verified = True
            user.verification_code = None
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise DatabaseError(f"Error verifying user and setting password: {str(e)}")

    def get_jumbotron_data(self) -> dict:
        """
        """
        total_students = self.db.session.query(Student).count()
        total_students_with_schedules_finalized = self.db.session.query(Student).filter(Student.is_completed == True).count()
        total_students_with_courses = self.db.session.query(Student).filter(or_(Student.courses.any(), Student.is_completed == True)).count()
        total_students_with_schedules_in_progress = total_students_with_courses - total_students_with_schedules_finalized
        total_students_without_course = total_students - total_students_with_courses
        return {
            "total_students": total_students,
            "total_schedules_in_progress": total_students_with_schedules_in_progress,
            "total_schedules_finalized": total_students_with_schedules_finalized,
            "total_students_without_course": total_students_without_course
        }

    def flip_mark_done(self, student_id) -> None:
        """
        """
        student = self.db.session.query(Student).filter(Student.id == student_id).first()
        student.is_completed = not student.is_completed
        today = datetime.now().date()
        today = today.strftime("%Y-%m-%d")
        schedule_progression = self.db.session.query(ScheduleProgression).filter(ScheduleProgression.date == today).first()
        if not schedule_progression:
            schedules_completed = self.db.session.query(Student).filter(Student.is_completed == True).count()
            approvals_from_program_heads = self.db.session.query(Student).filter(Student.is_approved_by_program_heads == True).count()
            schedule_progression = ScheduleProgression(date=today, num_schedules_completed=schedules_completed, num_approvals_from_program_heads=approvals_from_program_heads)
            self.db.session.add(schedule_progression)
        elif student.is_completed:
            schedule_progression.num_schedules_completed += 1
        else:
            schedule_progression.num_schedules_completed -= 1
        self.db.session.commit()
        return
    
    def flip_program_head_approval(self, student_id) -> None:
        """
        """
        student = self.db.session.query(Student).filter(Student.id == student_id).first()
        student.is_approved_by_program_heads = not student.is_approved_by_program_heads
        today = datetime.now().date()
        today = today.strftime("%Y-%m-%d")
        schedule_progression = self.db.session.query(ScheduleProgression).filter(ScheduleProgression.date == today).first()
        if not schedule_progression:
            schedules_completed = self.db.session.query(Student).filter(Student.is_completed == True).count()
            approvals_from_program_heads = self.db.session.query(Student).filter(Student.is_approved_by_program_heads == True).count()
            schedule_progression = ScheduleProgression(date=today, num_schedules_completed=schedules_completed, num_approvals_from_program_heads=approvals_from_program_heads)
            self.db.session.add(schedule_progression)
        elif student.is_approved_by_program_heads:
            schedule_progression.num_approvals_from_program_heads += 1
        else:
            schedule_progression.num_approvals_from_program_heads -= 1
        self.db.session.commit()
        return

    def remove_all_course_groupings(self, student_id) -> None:
        """
        """
        student = self.db.session.query(Student).filter(Student.id == student_id).first()
        for course in student.courses:
            course.num_enrolled -= 1
        student.courses = []
        self.db.session.commit()
        return
    
    def add_courses_by_groupings(self, student_id, groupings_list):
        """
        """
        student = self.db.session.query(Student).filter(Student.id == student_id).first()
        for grouping in groupings_list:
            courses = self.db.session.query(Course).filter(Course.course_grouping == grouping).all()
            if not courses:
                pass
            for course in courses:
                student.courses.append(course)
                course.num_enrolled += 1
        self.db.session.commit()
        return

    def save_schedules_to_local_file(self) -> list:
        """
        """
        # get all students
        schedule = []
        students = self.db.session.query(Student).all()
        for student in students:
            for course in student.courses:
                row = [
                    student.id,
                    student.first_name,
                    student.last_name,
                    student.term_code,
                    student.email,
                    student.is_completed,
                    student.is_approved_by_program_heads,
                    course.course_code,
                    course.crn,
                    course.block,
                    course.day,
                    course.start_date,
                    course.end_date,
                    course.begin_time,
                    course.end_time,
                    course.building_room,
                    course.instructor
                ]
                schedule.append(row)
        df = pd.DataFrame(schedule, columns=[
            "Student ID",
            "First Name",
            "Last Name",
            "Term Code",
            "Email",
            "Is Completed",
            "Is Approved By Program Heads",
            "Course Code",
            "CRN",
            "Block",
            "Day",
            "Start Date",
            "End Date",
            "Begin Time",
            "End Time",
            "Building Room",
            "Instructor"
        ])
        file_path = os.path.join(current_app.root_path, 'exports/schedule.csv')
        if not os.path.exists(os.path.join(current_app.root_path, 'exports')):
            os.makedirs(os.path.join(current_app.root_path, 'exports'))
        df.to_csv(file_path, index=False)
        return file_path
    
    def get_schedule_progression(self) -> dict:
        """
        """
        # get the 7 latest schedule progressions
        schedule_progressions = self.db.session.query(ScheduleProgression).order_by(ScheduleProgression.date.desc()).limit(7).all()
        total_students = self.db.session.query(Student).count()
        information = {
            "schedule_progressions": [schedule_progression.to_dict() for schedule_progression in schedule_progressions],
            "total_students": total_students
        }
        return information
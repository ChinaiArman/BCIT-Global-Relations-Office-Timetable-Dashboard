"""
"""

# IMPORTS
import pandas as pd
from sqlalchemy import text, delete, insert, update
from datetime import datetime

from models.Course import Course
from models.Student import Student
from models.Preferences import Preferences
from models.Enrollments import enrollments

from exceptions import InvalidUploadFile, InvalidFileType, DataNotFound, DatabaseError, DataAlreadyExists


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

    def bulk_course_upload(self, file) -> list:
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
            return self.upload_courses_to_database(df)
        except:
            raise InvalidUploadFile("Invalid file format. Error processing the file.")

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

    def bulk_student_upload(self, file) -> list:
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
            self.db.session.rollback()
            raise DatabaseError(f"Error uploading students to the database: {str(e)}")

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
        return student.__repr__()

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
            }
            for i, preference in enumerate(data.get("preferences")):
                student[f"Course Code Preference #{i+1}"] = preference
            student = pd.Series(student)
            row = self.normalize_student_data(student)
            student = Student(
                id=row["BCIT Student Number"],
                first_name=row["Legal First Name"],
                last_name=row["Legal Last Name"],
                term_code=row["Term Code"]
            )
            self.db.session.add(student)

            preferences = [row[f"Course Code Preference #{i}"] for i in range(1, len(data.get("preferences"))) if row[f"Course Code Preference #{i}"]]

            self.change_student_preferences(student.id, preferences) 
            self.db.session.commit()
            return
        except Exception as e:
            self.db.session.rollback()
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
            
            updatable_columns = ['first_name', 'last_name', 'term_code']
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
            self.db.session.rollback()
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
        return [student.__repr__() for student in students]

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
        df = pd.DataFrame([student.__repr__() for student in students])
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
            self.db.session.rollback()
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
            self.db.session.rollback()
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
            self.db.session.rollback()
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
            self.db.session.rollback()
            raise DatabaseError(f"Error adding course to student: {str(e)}")    
        
    def replace_courses_for_student(self, student_id: int, new_courses: list) -> dict:
        """
        Replace courses for a student.

        Args:
        -----
        student_id (int): The student ID.
        new_courses (list): The list of course IDs.

        Returns:
        --------
        dict: The response message.

        Example:
        --------
        >>> db = Database()
        >>> db.replace_courses_for_student(1, [1, 2, 3])
        ...
        """
        try:
            student = self.db.session.query(Student).filter(Student.id == student_id).first()
            if not student:
                raise DataNotFound(f"Student with ID not found: {student_id}")

            existing_courses = self.db.session.query(Course.id).filter(Course.id.in_(new_courses)).all()
            existing_course_ids = {course.id for course in existing_courses} 
            invalid_courses = [course for course in new_courses if course not in existing_course_ids]
            
            if invalid_courses:
                raise DataNotFound(f"Invalid course ID(s) found: {invalid_courses}")

            self.db.session.query(enrollments).filter(enrollments.c.student_id == student_id).delete()

            new_enrollments = [{'student_id': student_id, 'course_id': course_id} for course_id in new_courses]
            
            self.db.session.execute(enrollments.insert(), new_enrollments)
            return 
        except Exception as e:
            self.db.session.rollback()
            raise DatabaseError(f"Error replacing courses for student: {str(e)}")

    def get_course_by_course_grouping(self, course_grouping):
        try:
            courses = self.db.session.query(Course).filter(Course.course_grouping == course_grouping).all()
            for course in courses:
                course.start_date = course.start_date.strftime("%Y-%m-%d")
                course.end_date = course.end_date.strftime("%Y-%m-%d")
                course.begin_time = course.begin_time.strftime("%H:%M")
                course.end_time = course.end_time.strftime("%H:%M")
            course_reprs = [course.__repr__() for course in courses]
            return course_reprs
        except Exception as e:
            self.db.session.rollback()
            raise DatabaseError(f"Error fetching course by course grouping: {str(e)}")

    def get_course_by_course_code(self, course_code):
        try:
            courses = self.db.session.query(Course).filter(Course.course_code == course_code).all()
            if not courses:
                raise DataNotFound(f"Course with course code not found: {course_code}")
            for course in courses:
                course.start_date = course.start_date.strftime("%Y-%m-%d")
                course.end_date = course.end_date.strftime("%Y-%m-%d")
                course.begin_time = course.begin_time.strftime("%H:%M")
                course.end_time = course.end_time.strftime("%H:%M")
            course_reprs = [course.__repr__() for course in courses]
            return course_reprs
        except Exception as e:
            self.db.session.rollback()
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
            return course.__repr__()
        except Exception as e:
            self.db.session.rollback()
            raise DatabaseError(f"Error fetching course by ID: {str(e)}")

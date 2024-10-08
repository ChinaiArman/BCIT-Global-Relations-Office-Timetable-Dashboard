"""
"""

# IMPORTS
import pandas as pd
from sqlalchemy import text
from datetime import datetime

from models.Course import Course
from models.Student import Student

from exceptions import InvalidUploadFile


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
            raise InvalidUploadFile("Invalid file format. Please upload an XLSX file.")
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
        """ """
        if not file.filename.endswith(".csv"):
            raise InvalidUploadFile("Invalid file format. Please upload an CSV file.")
        try:
            df = pd.read_csv(file)
            return self.upload_students_to_database(df)
        except:
            raise InvalidUploadFile("Invalid file format. Error processing the file.")

    def normalize_student_data(self, row: pd.Series) -> pd.Series:
        """ """
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
        """ """
        self.db.session.query(Student).delete()
        self.db.session.commit()
        invalid_rows = []
        for _, row in df.iterrows():
            try:
                row = self.normalize_student_data(row)
                student = Student(
                    id=row["BCIT Student Number"],
                    first_name=row["Legal First Name"],
                    last_name=row["Legal Last Name"],
                    term_code=row["Term Code"],
                    preferences=",".join(
                        [
                            row[f"Course Code Preference #{i}"]
                            for i in range(1, 9)
                            if row[f"Course Code Preference #{i}"]
                        ]
                    ),
                )
                self.db.session.add(student)
            except Exception as e:
                print(e)
                invalid_rows.append({"id": row["BCIT Student Number"]})
        self.db.session.commit()
        return invalid_rows

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

            if student:
                return {
                    "status": 200,
                    "message": "Student Found",
                    "data": {
                        "id": student.id,
                        "firstName": student.first_name,
                        "lastName": student.last_name,
                        "preferences": (
                            student.preferences.split(",")
                            if student.preferences
                            else []
                        ),
                    },
                }
            else:
                return {"status": 404, "message": "Student not found"}

        except Exception as e:
            return {
                "status": 500,
                "message": "Error querying into database",
                "data": str(e),
            }

    def create_student(self, data) -> dict:
        """
        Create a new student.

        Args:
        -----
        student (Student): The student to create.

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

            if (
                self.db.session.query(Student)
                .filter(Student.id == data.get("id"))
                .first()
            ):
                return {"status": 400, "message": "Student ID already exists"}

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
                term_code=row["Term Code"],
                preferences=",".join(
                    [
                        row[f"Course Code Preference #{i}"]
                        for i in range(1, len(data.get("preferences")))
                        if row[f"Course Code Preference #{i}"]
                    ]
                ),
            )
            self.db.session.add(student)
            self.db.session.commit()
            return {"status": 201, "message": "Student created successfully"}
        except Exception as e:
            return {"status": 500, "message": str(e)}

    def update_student(self, id: int, data: dict) -> dict:
        """
        Update the student by ID.

        Args:
        -----
        id (int): The student ID.
        student (Student): The student to update.

        Returns:
        --------
        dict: The response message.

        Example:
        --------
        >>> db = Database()
        >>> student = Student(1, "John", "Doe")
        >>> db.update_student(1, student)
        ... {"message": "Student updated successfully"}
        """
        try:
            df = pd.read_csv("server/data/students.csv")

            if id not in df["BCIT ID"].values:
                return {"status": 404, "message": "Student not found"}

            invalid_keys = [key for key in data.keys() if key not in df.columns]
            if invalid_keys:
                return {"status": 400, "message": f"Invalid keys: {invalid_keys}"}

            df.loc[df["BCIT ID"] == id, data.keys()] = data.values()
            df.to_csv("server/data/students.csv", index=False)
            return {"status": 200, "message": "Student updated successfully"}

        except Exception as e:
            return {"status": 500, "message": str(e)}

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
            df = pd.read_csv("server/data/students.csv")
            if id not in df["BCIT ID"].values:
                return {"status": 404, "message": "Student not found"}
            df = df[df["BCIT ID"] != id]
            df.to_csv("server/data/students.csv", index=False)
            return {"status": 200, "message": "Student deleted successfully"}
        except Exception as e:
            return {"status": 500, "message": str(e)}

    def get_student_courses(self, id: int) -> dict:
        """
        Get the courses for the student by ID.

        Args:
        -----
        id (int): The student ID.

        Returns:
        --------
        dict: The response message.

        Example:
        --------
        >>> db = Database()
        >>> db.get_student_courses(1)
        ... {"message": "Student courses found"}
        """
        try:
            student = self.db.session.query(Student).filter(Student.id == id).first()
            if student:
                courses = student.preferences.split(",")
                if courses:
                    return {
                        "status": 200,
                        "message": "Student preferences found",
                        "data": courses,
                    }
                else:
                    return {"status": 404, "message": "Student preferences found"}
            else:
                return {"status": 404, "message": "Student not found"}
        except Exception as e:
            return {
                "status": 500,
                "message": "Error in querying into database",
                "data": str(e),
            }

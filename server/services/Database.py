"""
"""

# IMPORTS
import pandas as pd

from models.Course import Course
from models.Student import Student


# CONSTANTS
DROP_COURSE_COLUMNS = ["Hrs", "Block Code (swvmday)", "Block Conflicts (swvmday)", "Instructor Conflicts (swvmday)", "Instructor Conflicts (swvmday) = 'Y'", "Meeting Day No. (swvmday)", "Room Conflicts (swvmday)", "Room Conflicts (swvmday)  =  'Y'", "Sorted By", "Sort Order", "Time"]


# DATABASE CLASS
class Database:
    """
    """
    def __init__(self, db):
        """
        """
        self.db = db

    def load_courses_from_file(self, file) -> dict:
        """
        Save the bulk course upload file to the server.

        Args:
        -----
        file (FileStorage): The file to save.

        Returns:
        --------
        dict: The response message.

        Notes:
        ------
        1. The file is saved in the `server/data/` directory.
        2. The file is parsed to remove unnecessary columns.

        Example:
        --------
        >>> db = Database()
        >>> db.save_bulk_course_upload_file(file)
        ... {"status": 201, "message": "File uploaded successfully"}
        ... # File saved in `server/data/` directory

        Author: ``@ChinaiArman``
        """
        if not (file.filename.endswith(".xlsx") or file.filename.endswith(".csv")):
            return {"status": 400, "message": "Invalid file type. Please upload an Excel file."}
        try:
            df = self.parse_bulk_course_upload_file(file)
            self.save_bulk_course_upload_file(df)
        except KeyError as e:
            print(e)
            return {"status": 400, "message": "Invalid file format. Please use course upload template."}
        return {"status": 201, "message": "File uploaded successfully"}
    
    def parse_bulk_course_upload_file(self, file) -> None:
        """
        Parse the bulk course upload file to remove unnecessary columns.

        Args:
        -----
        file (FileStorage): The file to parse.

        Returns:
        --------
        None

        Notes:
        ------
        1. The file is read as a DataFrame.
        2. The columns are cleaned by removing special characters.
        3. The unnecessary columns are removed.
        4. The DataFrame is saved as a CSV file in the `server/data/` directory.

        Example:
        --------
        >>> db = Database()
        >>> db.parse_bulk_course_upload_file(file)
        ... # File saved as CSV in `server/data/` directory

        Author: ``@ChinaiArman``
        """
        df = pd.read_excel(file)
        df = df.map(lambda x: x.replace("*", "").replace("\n", "").strip() if isinstance(x, str) else x)
        df.columns = df.columns.map(lambda x: x.replace("*", "").replace("\n", "").strip())
        df.drop(columns=DROP_COURSE_COLUMNS, inplace=True)
        df["Instructor"] = df["Instructor"].map(lambda x: " ".join(x.split(", ")[::-1]))
        df = df.groupby([column for column in df.columns if column != "Instructor"]).agg({'Instructor': lambda x: ' & '.join(set(x))}).reset_index()
        df["Instructor"] = df["Instructor"].map(lambda x: x[:256])
        df.to_csv("server/data/courses.csv", index=False)
        return df
    
    def save_bulk_course_upload_file(self, df) -> None:
        """
        """
        self.db.session.query(Course).delete()
        self.db.session.commit()
        for _, row in df.iterrows():
            course = Course(status='Active', block=row['Block'], crn=row['CRN'], course_grouping=row['Block'] + row['Course'], course_code=row['Course'], course_type=row['Type'], day=row['Day'], begin_time=row['Begin Time'], end_time=row['End Time'], building_room=row['Bldg/Room'], start_date=row['Start Date'], end_date=row['End Date'], max_capacity=row['Max.'], num_enrolled= row['Act.'], is_full_time=row['FT/PT'], term_code=row["Term Code (swvmday)"], instructor=row['Instructor'])
            self.db.session.add(course)
        self.db.session.commit()
        return

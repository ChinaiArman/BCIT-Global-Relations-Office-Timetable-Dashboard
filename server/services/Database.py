"""
"""

# IMPORTS
import pandas as pd
from datetime import datetime

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
            return False
        try:
            df = self.parse_bulk_course_upload_file(file)
            df = self.normalize_student_data(df)
            self.save_bulk_course_upload_file(df)
            return True
        except:
            return False
    
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
        df = df.groupby([column for column in df.columns if column != "Instructor"]).agg({'Instructor': lambda x: ','.join(set(x))}).reset_index()
        return df

    def normalize_student_data(self, df: pd.DataFrame) -> None:
        """
        """
        df["Status"] = df["Status"].map(lambda x: "Active" if x == "Active" else "Inactive")
        df["Block"] = df["Block"].map(lambda x: x[:8])
        df["CRN"] = df["CRN"].map(lambda x: int(x))
        df["Course"] = df["Course"].map(lambda x: x[:8])
        df["Type"] = df["Type"].map(lambda x: x[:3])
        df["Day"] = df["Day"].map(lambda x: x[:3])
        df["Begin Time"] = df["Begin Time"].map(lambda x: datetime.strptime(str(int(x)), "%H%M").time())
        df["End Time"] = df["End Time"].map(lambda x: datetime.strptime(str(int(x)), "%H%M").time())
        df["Bldg/Room"] = df["Bldg/Room"].map(lambda x: x[:10])
        df["Start Date"] = df["Start Date"].map(lambda x: datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S").date())
        df["End Date"] = df["End Date"].map(lambda x: datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S").date())
        df["Max."] = df["Max."].map(lambda x: int(x))
        df["Act."] = df["Act."].map(lambda x: int(x))
        df["FT/PT"] = df["FT/PT"].map(lambda x: True if x == "FT" else False)
        df["Term Code (swvmday)"] = df["Term Code (swvmday)"].map(lambda x: int(x))
        df["Instructor"] = df["Instructor"].map(lambda x: x[:512])
        return df

    def save_bulk_course_upload_file(self, df: pd.DataFrame) -> None:
        """
        """
        self.db.session.query(Course).delete()
        self.db.session.commit()
        for _, row in df.iterrows():
            try: 
                course = Course(status='Active', block=row['Block'], crn=row['CRN'], course_grouping=row['Block'] + row['Course'], course_code=row['Course'], course_type=row['Type'], day=row['Day'], begin_time=row['Begin Time'], end_time=row['End Time'], building_room=row['Bldg/Room'], start_date=row['Start Date'], end_date=row['End Date'], max_capacity=row['Max.'], num_enrolled= row['Act.'], is_full_time=row['FT/PT'], term_code=row["Term Code (swvmday)"], instructor=row['Instructor'])
                self.db.session.add(course)
            except:
                pass
        self.db.session.commit()
        return

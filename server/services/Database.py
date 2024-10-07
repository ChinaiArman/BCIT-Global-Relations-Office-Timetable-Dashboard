"""
"""

# IMPORTS
import pandas as pd
from sqlalchemy import text
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
        if not file.filename.endswith(".xlsx"):
            return False
        try:
            df = self.parse_bulk_course_upload_file(file)
            self.save_bulk_course_upload_file(df)
            return True
        except Exception as e:
            print(e)
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

    def normalize_course_data(self, row) -> None:
        """
        """
        row["Status"] = "Active" if row["Status"] == "Active" else "Inactive"
        row["Block"] = row["Block"][:8]
        row["CRN"] = int(row["CRN"])
        row["Course"] = row["Course"][:8]
        row["Type"] = row["Type"][:3]
        row["Day"] = row["Day"][:3]
        row["Begin Time"] = datetime.strptime(str(int(row["Begin Time"])), "%H%M").time()
        row["End Time"] = datetime.strptime(str(int(row["End Time"])), "%H%M").time()
        row["Bldg/Room"] = row["Bldg/Room"][:10]
        row["Start Date"] = datetime.strptime(str(row["Start Date"]), "%Y-%m-%d %H:%M:%S").date()
        row["End Date"] = datetime.strptime(str(row["End Date"]), "%Y-%m-%d %H:%M:%S").date()
        row["Max."] = int(row["Max."])
        row["Act."] = int(row["Act."])
        row["FT/PT"] = True if row["FT/PT"] == "FT" else False
        row["Term Code (swvmday)"] = int(row["Term Code (swvmday)"])
        row["Instructor"] = row["Instructor"][:512]
        return row

    def save_bulk_course_upload_file(self, df: pd.DataFrame) -> None:
        """
        """
        self.db.session.query(Course).delete()
        self.db.session.commit()
        # reset auto increment back to 1
        self.db.session.execute(text("ALTER TABLE courses AUTO_INCREMENT = 1"))
        for _, row in df.iterrows():
            try: 
                row = self.normalize_course_data(row)
                course = Course(status=row['Status'], block=row['Block'], crn=row['CRN'], course_grouping=row['Block'] + row['Course'], course_code=row['Course'], course_type=row['Type'], day=row['Day'], begin_time=row['Begin Time'], end_time=row['End Time'], building_room=row['Bldg/Room'], start_date=row['Start Date'], end_date=row['End Date'], max_capacity=row['Max.'], num_enrolled= row['Act.'], is_full_time=row['FT/PT'], term_code=row["Term Code (swvmday)"], instructor=row['Instructor'])
                self.db.session.add(course)
            except Exception as e:
                print(e)
                pass
        self.db.session.commit()
        return

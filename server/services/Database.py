"""
"""

# IMPORTS
import pandas as pd


# CONSTANTS
DROP_COURSE_COLUMNS = ["Hrs", "Block Code (swvmday)", "Block Conflicts (swvmday)", "Instructor Conflicts (swvmday)", "Instructor Conflicts (swvmday) = 'Y'", "Meeting Day No. (swvmday)", "Room Conflicts (swvmday)", "Room Conflicts (swvmday)  =  'Y'", "Sorted By", "Sort Order", "Time"]

# DATABASE CLASS
class Database:
    """
    """
    def __init__(self):
        """
        """
        pass

    def save_bulk_course_upload_file(self, file):
        """
        """
        if file.filename.endswith(".xlsx") or file.filename.endswith(".csv"):
            file.save(f"server/data/bulk_course_upload_file.{file.filename.split('.')[-1]}")
            try:
                self.parse_bulk_course_upload_file(file)
            except KeyError:
                return {"status": 400, "message": "Invalid file format. Please use course upload template."}
            return {"status": 201, "message": "File uploaded successfully"}
        else:
            return {"status": 400, "message": "Invalid file type. Please upload an Excel file."}
    
    def parse_bulk_course_upload_file(self, file):
        """
        """
        df = pd.read_excel(file)
        df = df.map(lambda x: x.replace("*", "").replace("\n", "").strip() if isinstance(x, str) else x)
        df.columns = df.columns.map(lambda x: x.replace("*", "").replace("\n", "").strip())
        df.drop(columns=DROP_COURSE_COLUMNS, inplace=True)
        df.to_csv("server/data/courses.csv", index=False)
        return


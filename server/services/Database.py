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

    def save_bulk_course_upload_file(self, file) -> dict:
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

        Author: @ChinaiArman
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

        Author: @ChinaiArman
        """
        df = pd.read_excel(file)
        df = df.map(lambda x: x.replace("*", "").replace("\n", "").strip() if isinstance(x, str) else x)
        df.columns = df.columns.map(lambda x: x.replace("*", "").replace("\n", "").strip())
        df.drop(columns=DROP_COURSE_COLUMNS, inplace=True)
        df.to_csv("server/data/courses.csv", index=False)
        return

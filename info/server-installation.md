### Installation

1. Clone the repo (or download the ZIP file and extract it to a folder on your local machine)

   ```sh
   git clone https://github.com/ChinaiArman/BCIT-Global-Relations-Office-Timetable-Dashboard.git       # Clone the repository
   ```

2. Create a virtual environment

   2.1 Create a virtual environment in the project's root directory using the following commands:

   ```sh
   cd BCIT-Global-Relations-Office-Timetable-Dashboard      # Change to the project directory
   python -m venv .venv                                     # Create a virtual environment
   ```

   2.2 Activate the virtual environment:

   - Mac:
     - Activation command:
     ```sh
     source .venv/bin/activate     # Activate the virtual environment
     ```
     - Deactivation command:
     ```sh
     source .venv/bin/deactivate       # Deactivate the virtual environment
     ```
   - Windows:
     - Activation command:
     ```sh
     .venv\Scripts\activate.bat        # Activate the virtual environment
     ```
     - Deactivation command:
     ```sh
     .venv\Scripts\deactivate.bat      # Deactivate the virtual environment
     ```
     Your interpreter should now be set to the Virtual Environment instance of python.

3. Install required Python libraries

   ```sh
   cd server                           # Change to the server directory
   pip install -r requirements.txt     # Install the required libraries
   ```

   - If after running the command, none of the packages have installed, restart the terminal and try again, ensuring that the virtual environment is activated.
   - If a single package fails to install, try installing it separately using the following command:

   ```sh
   pip install <package_name>          # Install the package separately
   ```

4. Set up environment variables

   - Create a `.env` file in the server directory of the project.
   - Add the following environment variables to the `.env` file:

   ```sh
   PORT=""                 # Port number for the server
   DB_USERNAME=""          # Database username
   DB_PASSWORD=""          # Database password
   DB_HOST=""              # Database host
   DB_PORT=""              # Database port
   DB_NAME=""              # Database name
   DB_SSL_CERT=""          # Database SSL certificate as a string
   GMAIL_EMAIL=""          # Gmail email address
   GMAIL_PASSWORD=""       # Gmail password
   CLIENT_URL=""           # Client URL
   ```

5. Install MYSQL Server

   - Install MySQL Server on your local machine from the following link (recommend to install both server and workbench):
     - [MySQL Community Server](https://dev.mysql.com/downloads/installer/)
   - Create a new database and user for the project.
   - Add the database credentials to the `.env` file.

6. Run the server

   ```sh
   cd ..                      # Change to the project directory
   python server/app.py       # Run the server
   ```

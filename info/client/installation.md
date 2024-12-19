### Installation

1. Clone the repo (or download the ZIP file and extract it to a folder on your local machine)

   ```sh
   git clone https://github.com/ChinaiArman/BCIT-Global-Relations-Office-Timetable-Dashboard.git       # Clone the repository
   ```

2. Install Node Packages

    ```sh
    cd client                           # Change to the client directory
    npm install                         # Install the required libraries
    ```
    
    - If after running the command, none of the packages have installed, restart the terminal and try again.
    - If a single package fails to install, try installing it separately using the following command:
    
    ```sh
    npm install <package_name>          # Install the package separately
    ```

3. Set up environment variables

   - Create a `.env` file in the client directory of the project.
   - Add the following environment variables to the `.env` file:

   ```sh
   REACT_APP_API_URL=""                 # URL of the server API
   ```

4. Start the development server

    ```sh
    npm start                           # Start the development server
    ```

    The development server should now be running on `http://localhost:3001/`. Open this URL in your browser to view the application.
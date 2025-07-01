# GGE Attack Detect

This project is a tool for scanning and analyzing islands in the Goodgame Empire (GGE) game. It connects to the GGE game server, scans the map for specific types of islands, and provides information about them through a web interface.

## Features
- Connects to the GGE game server using a websocket.
- Scans the map for islands of different levels (Level 60, 70, 80).
- Provides a web interface to view and interact with the scan results.
- Supports normal, storm, and spiral scan modes.

## Requirements
- Python 3.10+
- The following Python packages (add these to `requirements.txt`):
  - Flask
  - requests
  - pygge (custom or third-party, see below)

## Setup
1. **Install Python dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   If `pygge` is not available on PyPI, install it from your custom source or provide the module in the project directory.

2. **Run the server:**
   - If you have a `server.exe`, simply run it:
     ```sh
     server.exe
     ```
   - If running from source, use:
     ```sh
     python server.py
     ```

3. **Access the web interface:**
   - Open your browser and go to `http://localhost:5000` (or the port specified in your server output).

## Usage Procedure
1. **Login:**
   - Enter your GGE username and password in the web interface to log in.

2. **Start a Scan:**
   - Choose the scan type (normal, storm, or spiral) and start the scan.
   - The server will connect to the GGE game server and begin scanning the map for islands.

3. **View Results:**
   - The results will be displayed in the web interface, showing the locations and levels of detected islands.
   - You can sort or filter the results as needed.

4. **Repeat as Needed:**
   - You can run multiple scans or change scan parameters as required.

## Notes
- The `pygge` module is required for websocket communication with the GGE server. If you do not have this module, the tool will not work.
- Credentials are only used to log in to the GGE server and are not sent anywhere else.
- For any issues, check the server logs for error messages.

## Security
- The code does not send your credentials or scan data to any third-party service.
- Always review the code and dependencies before running.

---

**Enjoy scanning and analyzing GGE islands!**

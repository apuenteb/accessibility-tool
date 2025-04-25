This tool has been developed using Python 3.12.3 version. It is recommended that it is run using this py version.

Steps:
1. Clone repo (open terminal and run: git clone https://github.com/apuenteb/accessibility-tool.git)
2. To create myvenv with Python 3.12 run in terminal: python3.12 -m venv myenv
3. To activate myvenv:
   On Windows, run: myvenv\Scripts\activate
   On macOS, run: source myvenv/bin/activate
4. To install the required packages, run: pip install -r requirements.txt
   4.1 you might need to re-install manually pyserial:
       pip uninstall pyserial
       pip install pyserial==3.5 
5. Run the code app.py: python app.py
6. Open a new command line window and activate the same environment: myvenv\Scripts\activate 
7. Run the code request_Arduino_websocket.py: python request_Arduino_websocket.py # first check which COM port Arduino is running on

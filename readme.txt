This tool has been developed using Python 3.12.3 version. It is recommended that it is run using this py version.

Steps:
1. Clone repo (open terminal and run: git clone https://github.com/apuenteb/accessibility-tool.git)
   If you het an LST error you can ignore it
   You need to manually download large files from drive folders provided in ReadMe files for:
   'assets>geojsons'
   'assets>csv_files'
   'preprocessing>donwload and create networks>public transit>networks'
2. To create myvenv with Python 3.12 run in terminal: python3.12 -m venv myenv
   If you're using conda: conda create -n accessibility python=3.12
3. To activate myvenv:
   On Windows, run: myvenv\Scripts\activate
   On macOS, run: source myvenv/bin/activate
   If you're using conda: conda activate accessibility
4. To install the required packages, cd to the right directory and run: pip install -r requirements.txt
   4.1 you might need to re-install manually pyserial:
       pip uninstall pyserial
       pip install pyserial==3.5 
5. Run the code app.py: python app.py
6. Open a new command line window and activate the same environment: myvenv\Scripts\activate 
7. Run the code request_Arduino_websocket.py: python request_Arduino_websocket.py # first check which COM port Arduino is running on

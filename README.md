# AutoStart - 
### A Python script that sequentially initiates a 'start' and subsequent 'stop' of PC programs using instructions from a simple .json text file.
Run the Python script or use the autostart.exe executable for Windows 10/11. Use a text editor like Notepad to edit the autostart.json file to specify the sequence of programs to start and stop when the corresponding button is clicked. Place all of the files in the same directory.

## autostart.json
There are two sections. The "startup" contains the paths to the programs to start and the delay before starting in seconds. The "shutdown" section contains the paths to the running programs to stop (shutdown), the sequence and the delay in seconds before initiating a program stop. 

Just follow normal .json formatting in your file.

```
{  
  "startup": [  
    {"path": "C:\\WSJT31\\bin\\wsjtx.exe", "delay": 1},  
    {"path": "C:\\Users\\dfdol\\AppData\\Local\\WSJT-X\\WSJTX-CoPilot.exe", "delay": 2}  
],  
  "shutdown": [  
    {"path": "C:\\WSJT31\\bin\\wsjtx.exe", "delay": 1},  
    {"path": "C:\\Users\\dfdol\\AppData\\Local\\WSJT-X\\WSJTX-CoPilot.exe", "delay": 2}  
  ]  
}
```

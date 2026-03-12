# AutoStart - 
### A Python script that sequentially starts and stops PC programs using simple .json instructions
Run the Python script or use the provided executable. Use a text editor like Notepad to edit the autostart.json file to specify which programs to start and shutdown, the sequence and the delay in seconds between each app.


## autostart.json
There are two sections. The first is the "startup" paths and the delay before going to the next startup item. The second section is which programs to "shutdown", the sequence and the dealy in seconds between each app.

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


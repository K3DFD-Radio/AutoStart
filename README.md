# AutoStart - 
### A Python script that sequentially 'startup' and 'shutdown' PC programs using instructions from a simple .json text file
Run the Python script or use the provided autostart.exe executable for Windows 10/11. Use a text editor like Notepad to edit the autostart.json file to specify which programs to startup and shutdown, the sequence and the delay in seconds between each program.

## autostart.json
There are two sections. The first are the paths to the programs to 'startup' and the delay before going to the next startup item. The second section are the paths to the programs to 'shutdown', the sequence and the delay in seconds between each program. Keep the autostart.py or autostart.exe and autostart.json files in the same directory.

Just follow normal .json formatting in your file. Remember to use '\\' instead of '\' in the executable file path. Edit as required for your OS.

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


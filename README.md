# Images to gif
```transforma_gif.py --path path_to_files --size 2 --frame 12 --out out_file```


## cmdline_verify 
Just some functions to make the options more easy and clearly like framerate, extensions if yu wanto specificy
some extensions the scripts will read only images with that extension.
the ideia is make the things more fast, too soon is comming a GUI.

## find_files_byPATH
If you use -e --ext --extension the script read all the files with that extension.
if you dont, rename the frames files with img_0001.jpg|png... in order.

### background_remove scheme
> L-channel: brightness.<br>
> A-channel: variation between red and green.<br>
> B-channel: variation between yellow and blue.<br>

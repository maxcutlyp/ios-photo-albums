## Prerequisites
You will need `libimobiledevice` to get the data required for the script.
- On Debian and derivatives, these packages are: `ideviceinstaller python-imobiledevice libimobiledevice-utils libimobiledevice4 libplist2 python-plist ifuse`
- On Arch and derivatives, these packages are: `ideviceinstaller libimobiledevice`

Then you'll need to pair and mount your iOS device
1. Connect it via USB
2. Pair it with `idevicepair pair`
3. Create a mountpoint (e.g. `~/iPhone`) with ifuse:
```bash
mkdir ~/iPhone
ifuse ~/iPhone
```

You should see that the mountpoint you made has a few files and directories in it. The ones we care about are `DCIM`, `PhotoData/AlbumsMetadata`, and `PhotoData/Photos.sqlite`, so copy them to somewhere outside of the mountpoint. After that, you can unmount your iOS device with `fusermount -u ~/iPhone`.

## Install
1. Download the script (preferably to a similar place you copied that file and folders to)
2. Make it executable with `chmod +x wherever/you/saved/it/iosphotoalbums.py` (or in your file manager)

## Usage
The script takes three positional arguments:
- the path to the DCIM folder
- the path to the Photos.sqlite folder
- the path to the AlbumsMetadata folder

By default, the script will output everything to the current directory, so I'd recommend passing a path to `-o` (output). This is where the album folders will be placed. Put together, the command will look something like this:
```bash
./iosphotoalbums.py ./DCIM ./Photos.sqlite ./AlbumsMetadata -o ./albums
```

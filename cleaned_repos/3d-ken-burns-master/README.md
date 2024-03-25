# 3d-ken-burns
This is a reference implementation of 3D Ken Burns Effect from a Single Image using PyTorch. Given a single input image, it animates this still image with a virtual camera scan and zoom subject to motion parallax.

## usage
To run it on an image and generate the 3D Ken Burns effect fully automatically, use the following command.

```
python autozoom.py --in ./images/doublestrike.jpg --out ./autozoom.mp4
```

To start the interface that allows you to manually adjust the camera path, use the following command. You can then navigate to `http://localhost:8080/` and load an image using the button on the bottom right corner. Please be patient when loading an image and saving the result, there is a bit of background processing going on.

```
python interface.py
```

To run the depth estimation to obtain the raw depth estimate, use the following command.

```
python depthestim.py --in ./images/doublestrike.jpg --out ./depthestim.npy
```

To benchmark the depth estimation, run `python benchmark-ibims.py` or `python benchmark-nyu.py`. You can use it to easily verify that the provided implementation runs as expected.
# opencv_stream

Under construction

Developed by Olivier 

## Examples of How To Use 

Creating A Stream


```python
from opencv_stream import VideoStreamer, FpsDrawer

stream = VideoStreamer.from_webcam()
fps_drawer = FpsDrawer()

@stream.on_next_frame
def func(image:np.ndarray):
    fps_drawer.draw(image)

```

```python
from opencv_stream import VideoStreamer

path = "[PATH TO VIDEO]"
stream = VideoStreamer.from_video_input(path)

@stream.on_next_frame
def func(image:np.ndarray):
    pass

```

"""APIs for playing videos"""

import typing

from ffpyplayer import pic, player
from PIL import Image
from tkintertools.core import containers
from tkintertools.toolbox import enhanced

__all__ = [
    "VideoCanvas",
]


class VideoCanvas(containers.Canvas):
    """A canvas that is scalable and playable for videos"""

    def __init__(
        self,
        master: "containers.Tk | containers.Canvas",
        *,
        max_fps: int = 60,
        expand: typing.Literal["", "x", "y", "xy"] = "xy",
        zoom_item: bool = False,
        keep_ratio: typing.Literal["min", "max"] | None = None,
        free_anchor: bool = False,
        name: str = "Canvas",
        **kwargs,
    ) -> None:
        """
        * `master`: parent widget
        * `max_fps`: limitation of FPS
        * `expand`: the mode of expand, `x` is horizontal, and `y` is vertical
        * `zoom_item`: whether or not to scale its items
        * `keep_ratio`: the mode of aspect ratio, `min` follows the minimum
        value, `max` follows the maximum value
        * `free_anchor`: whether the anchor point is free-floating
        * `kwargs`: compatible with other parameters of class `tkinter.Canvas`
        """
        containers.Canvas.__init__(
            self, master, expand=expand, zoom_item=zoom_item,
            keep_ratio=keep_ratio, free_anchor=free_anchor, name=name, **kwargs)
        self.delay = 1000 // max_fps
        self._video = self.create_image(0, 0, anchor="nw")

    def _refresh(self) -> None:
        """Refresh the canvas"""
        frame, val = self.media.get_frame()
        if val != 'eof' and frame is not None:
            img, _ = frame
            img = pic.SWScale(
                *img.get_size(), img.get_pixel_format(), *self._size).scale(img)
            self.frame = enhanced.PhotoImage(Image.frombytes(
                "RGB", self._size, img.to_bytearray()[0]))
            self.itemconfigure(self._video, image=self.frame)
        self.schedule = self.after(self.delay, self._refresh)

    def play(self, file: str) -> None:
        """Play the video"""
        self.media = player.MediaPlayer(file)
        self._refresh()

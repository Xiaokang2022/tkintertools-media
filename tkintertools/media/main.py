"""APIs for playing videos"""

import typing

import ffpyplayer.pic
import ffpyplayer.player
import PIL.Image
import tkintertools.animation.animations
import tkintertools.animation.controllers
import tkintertools.core.containers
import tkintertools.standard.widgets
import tkintertools.toolbox.enhanced

__all__ = [
    "VideoCanvas",
]


class VideoCanvas(tkintertools.core.containers.Canvas):
    """A canvas that is scalable and playable for videos"""

    def __init__(
        self,
        master: "tkintertools.core.containers.Tk \
            | tkintertools.core.containers.Canvas",
        *,
        control: bool = False,
        max_fps: int = 30,
        expand: typing.Literal["", "x", "y", "xy"] = "xy",
        zoom_item: bool = True,
        keep_ratio: typing.Literal["min", "max"] | None = None,
        free_anchor: bool = False,
        name: str = "Canvas",
        **kwargs,
    ) -> None:
        """
        * `master`: parent widget
        * `control`: whether to enable the built-in UI
        * `max_fps`: limitation of FPS
        * `expand`: the mode of expand, `x` is horizontal, and `y` is vertical
        * `zoom_item`: whether or not to scale its items
        * `keep_ratio`: the mode of aspect ratio, `min` follows the minimum
        value, `max` follows the maximum value
        * `free_anchor`: whether the anchor point is free-floating
        * `kwargs`: compatible with other parameters of class `tkinter.Canvas`
        """
        tkintertools.core.containers.Canvas.__init__(
            self, master, expand=expand, zoom_item=zoom_item,
            keep_ratio=keep_ratio, free_anchor=free_anchor, name=name, **kwargs)
        self.delay = 1000 // max_fps
        self._control = control
        self._video = self.create_image(0, 0, anchor="nw")

    def _initialization(self) -> None:
        tkintertools.core.containers.Canvas._initialization(self)
        if self._control:
            self.control()
            self.bind("<Enter>", lambda _: self._an(True), "+")
            self.bind("<Leave>", lambda _: self._an(False), "+")

    def _refresh(self) -> None:
        """Refresh the canvas"""
        frame, val = self.media.get_frame()
        if val != 'eof' and frame is not None:
            img, pts = frame
            img = ffpyplayer.pic.SWScale(
                *img.get_size(), img.get_pixel_format(), *self._size).scale(img)
            self.frame = tkintertools.toolbox.enhanced.PhotoImage(
                PIL.Image.frombytes("RGB", self._size, img.to_bytearray()[0]))
            self.itemconfigure(self._video, image=self.frame)
            if self._control:
                self.p.set(pts / self.metadata["duration"])
        elif val == 'eof' and self._control:
            self.p.set(1)
        self.schedule = self.after(self.delay, self._refresh)

    def play(self, file: str) -> None:
        """Play the video"""
        self.media = ffpyplayer.player.MediaPlayer(file, autoexit=True)
        self.metadata = self.media.get_metadata()
        self._refresh()

    def control(self) -> None:
        """"""
        self.bottom = tkintertools.Frame(
            self, zoom_item=True, free_anchor=True)
        self.bottom.place(width=1280, height=60, y=self._size[1])
        tkintertools.standard.widgets.Button(
            self.bottom, (10, 10), text="播放 / 暂停",
            command=self.media.toggle_pause)
        self.p = tkintertools.standard.widgets.ProgressBar(
            self.bottom, (150, 20), (800, 20))
        tkintertools.standard.widgets.Text(
            self.bottom, (1000, 30), text="音量", anchor="center")
        tkintertools.standard.widgets.Slider(
            self.bottom, (1050, 15), (200, 30),
            command=self.media.set_volume, default=1)

    def _an(self, up: bool) -> None:
        """"""
        k = -1 if up else 1
        tkintertools.animation.animations.MoveTkWidget(
            self.bottom, 250, (0, self.bottom._size[1]*k), fps=60,
            controller=tkintertools.animation.controllers.smooth).start()

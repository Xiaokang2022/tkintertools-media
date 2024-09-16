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
        auto_play: bool = False,
        click_pause: bool = True,
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
        * `auto_play`: whether to start playing the video automatically
        * `click_pause`: whether to pause when clicked
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
        self._auto_play = auto_play
        self._video = self.create_image(0, 0, anchor="nw")
        if click_pause:
            self.bind("<ButtonRelease-1>",
                      lambda _: self.media.toggle_pause(), "+")

    def _initialization(self) -> None:
        tkintertools.core.containers.Canvas._initialization(self)
        if self._control:
            self._control_ui()
            self.bind("<Enter>", lambda _: self._an(True), "+")
            self.bind("<Leave>", lambda _: self._an(False), "+")
            self.bind("<MouseWheel>", lambda event: self.v.set(
                self.v.get() + 0.05*((1, -1)[event.delta < 0]),
                callback=True), "+")

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
                self.t.set(f"{self._tiem_convert(
                    pts)} / {self._tiem_convert(self.metadata["duration"])}")
        elif val == 'eof' and self._control:
            self.media.set_pause(True)
            self.p.set(1)
        self.schedule = self.after(self.delay, self._refresh)

    def _tiem_convert(self, t: float) -> str:
        """Convert seconds to a special format"""
        m, s = divmod(round(t), 60)
        return f"{m:02d}:{s:02d}"

    def play(self, file: str) -> None:
        """Play the video"""
        self.media = ffpyplayer.player.MediaPlayer(file, autoexit=True)
        self.metadata = self.media.get_metadata()
        if not self._auto_play:
            self.media.set_pause(True)
        self._refresh()

    def _control_ui(self) -> None:
        """UI for bottom bar"""
        self.bottom = tkintertools.core.containers.Frame(
            self, zoom_item=True, free_anchor=True)
        self.bottom.place(width=1280, height=60, y=self._size[1])
        self.t = tkintertools.standard.widgets.Text(
            self.bottom, (215, 30), text="00:00 / 00:00", anchor="center")
        tkintertools.standard.widgets.Button(
            self.bottom, (10, 10), text="播放 / 暂停",
            command=self.media.toggle_pause)
        self.p = tkintertools.standard.widgets.Slider(
            self.bottom, (300, 15), (650, 30),
            command=lambda p: (
                self.media.seek(p*self.metadata["duration"], relative=False),
                self.t.set(f"{self._tiem_convert(
                    p*self.metadata["duration"])} / {
                        self._tiem_convert(self.metadata["duration"])}")))
        tkintertools.standard.widgets.Text(
            self.bottom, (1000, 30), text="音量", anchor="center")
        self.v = tkintertools.standard.widgets.Slider(
            self.bottom, (1040, 15), (150, 30),
            command=self.media.set_volume, default=1)
        tkintertools.standard.widgets.ToggleButton(
            self.bottom, (1210, 10), text="全屏",
            command=self.master.fullscreen
        )

    def _an(self, up: bool) -> None:
        """Animation for bottom bar"""
        k = -1 if up else 1
        dy = 0 if up else self.bottom._size[1]
        tkintertools.animation.animations.Animation(
            250, tkintertools.animation.controllers.smooth, fps=60,
            callback=lambda p: self.bottom.place(
                y=self._size[1] + self.bottom._size[1]*p*k - dy)
        ).start()

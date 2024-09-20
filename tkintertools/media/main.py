"""APIs for playing videos"""

import abc
import platform
import time
import typing

import ffpyplayer.pic
import ffpyplayer.player
import PIL.Image
import PIL.ImageTk
import typing_extensions
from tkintertools.animation import animations, controllers
from tkintertools.core import containers, virtual
from tkintertools.standard import images, widgets
from tkintertools.style import manager
from tkintertools.toolbox import enhanced

from . import icons

__all__ = [
    "VideoCanvas",
]


class _CustomizedWidget(virtual.Widget, abc.ABC):
    """Provide the ability to switch icon theme"""

    def _bind(self, *, icon: str) -> None:
        """process some thing about theme"""
        self._icon = icon
        self._theme(manager.get_color_mode() == "dark")
        manager.register_event(self._theme)

    def _theme(self, dark: bool) -> None:
        """Switch the icon theme of the widget"""
        if self._images:
            self._images[0].destroy()
        images.StillImage(
            self, image=self.master.master._icons[
                self._icon]["dark" if dark else "light"])


class _FullscreenToggleButton(widgets.ToggleButton, _CustomizedWidget):
    """Customized toggle button for function of fullscreen"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, name="ToggleButton", **kwargs)
        self._bind(icon="fullscreen")


class _AudioImage(widgets.Image, _CustomizedWidget):
    """Customized image widget for displaying audio icon"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, name="Image", **kwargs)
        self._bind(icon="audio")


class _PlayButton(widgets.Button, _CustomizedWidget):
    """Customized Button for the ability to play or pause the video"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, name="Button", **kwargs)
        self._bind(icon="play")

    def _toggle(self) -> None:
        """Force to change the icon image"""
        self._icon = "pause" if self._icon == "play" else "play"
        self._theme(manager.get_color_mode() == "dark")
        self._images[0].zoom((1, 1))


class VideoCanvas(containers.Canvas):
    """A canvas that is scalable and playable for videos"""

    def __init__(
        self,
        master: "containers.Tk | containers.Canvas",
        *,
        controls: bool = False,
        loop: bool = False,
        click_pause: bool = True,
        expand: typing.Literal["", "x", "y", "xy"] = "xy",
        zoom_item: bool = False,
        keep_ratio: typing.Literal["min", "max"] | None = None,
        free_anchor: bool = False,
        name: str = "Canvas",
        **kwargs,
    ) -> None:
        """
        * `master`: parent widget
        * `controls`: whether to enable the built-in UI
        * `loop`: whether the video loops automatically
        * `click_pause`: whether to pause when clicked
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

        self._icons = icons.parse()
        self._player = self._schedule = None
        self._video = self.create_image(0, 0, anchor="center")
        self._controls = controls
        self._loop = loop

        if click_pause:
            self.bind("<ButtonRelease-1>", lambda _: (
                self._player.toggle_pause() if self._player else None,
                self._play_button._toggle() if self._controls else None), "+")

    @typing_extensions.override
    def _initialization(self) -> None:
        containers.Canvas._initialization(self)
        if self._controls:
            self._load_control_bar()
            self.bind("<Motion>", lambda _: self._display_control_bar(True), "+")
            self.bind("<Leave>", lambda _: self._display_control_bar(False), "+")
            if platform.system() == "Linux":
                self.bind("<Button-4>", lambda _: self._volume_bar.set(
                    self._volume_bar.get() + 0.05, callback=True), "+")
                self.bind("<Button-5>", lambda _: self._volume_bar.set(
                    self._volume_bar.get() - 0.05, callback=True), "+")
            else:
                self.bind("<MouseWheel>", lambda event: self._volume_bar.set(
                    self._volume_bar.get() + 0.05*((1, -1)[event.delta < 0]),
                    callback=True), "+")

    @typing_extensions.override
    def _re_place(self) -> None:
        containers.Canvas._re_place(self)
        self.update_idletasks()
        if self._player is not None:
            self._resize()

    def open(
        self,
        file: str,
        *,
        auto_play: bool = False,
        muted: bool = False,
    ) -> None:
        """
        Open a video file and play

        * `file`: the video file path
        * `auto_play`: whether to start playing the video automatically
        * `muted`: whether or not to mute the video at the start
        """
        if self._player is not None:
            raise RuntimeError("The player is in use.")

        self.update_idletasks()
        self._player = ffpyplayer.player.MediaPlayer(file, autoexit=True)
        self._play({"auto_play": auto_play, "muted": muted})

    def close(self) -> None:
        """Close the video player"""
        if self._player is None:
            return
        self.after_cancel(self._schedule)
        self._player.close_player()
        self._player = self._schedule = None

    def _play(self, init_prams: dict[str, bool] | None = None) -> None:
        """Refresh the canvas"""
        start = time.time()
        frame, val = self._player.get_frame()

        if val != "eof" and frame is not None:
            if init_prams is not None:
                self._player.set_pause(not init_prams["auto_play"])
                self._player.set_volume(not init_prams["muted"])
                self._resize()
                if self._controls:
                    self._volume_bar.set(not init_prams["muted"])
                    if init_prams["auto_play"]:
                        self._play_button._toggle()
                init_prams = None
            img, pts = frame
            self.__frame = enhanced.PhotoImage(PIL.Image.frombytes(
                "RGB", img.get_size(), img.to_bytearray()[0]))
            self.itemconfigure(self._video, image=self.__frame)
            if self._controls:
                self._refresh_control_bar(pts)
            fps = self._player.get_metadata()["frame_rate"][0] / \
                self._player.get_metadata()["frame_rate"][1]
            interval = round(1000/fps - (time.time()-start) * 1000)
        elif val == 'eof':
            if self._controls:
                self._progress_bar.set(not self._loop)
            if self._loop:
                self._player.seek(0, relative=False)
            else:
                self._player.set_pause(True)
                self._play_button._toggle()
            interval = 0
        else:
            interval = 0

        self._schedule = self.after(
            interval if interval > 0 else 1, self._play,
            init_prams if init_prams is not None else None)

    def _resize(self) -> None:
        """Resize the size of video"""
        self.coords(self._video, self._size[0]/2, self._size[1]/2)
        size = self._player.get_metadata()["src_vid_size"]
        if self._size[0] / self._size[1] <= size[0] / size[1]:
            self._player.set_size(width=self._size[0])
        else:
            self._player.set_size(height=self._size[1])

    def _refresh_control_bar(self, pts: float) -> None:
        """Refresh the stat of the control bar"""
        self._progress_bar.set(pts/self._player.get_metadata()["duration"])
        self._timer.set("%02d:%02d / %02d:%02d" % (
            *divmod(round(pts), 60),
            *divmod(round(self._player.get_metadata()["duration"]), 60)))

    def _load_control_bar(self) -> None:
        """UI for bottom bar"""
        k = self._size[0] / 1280
        self._control_bar = containers.Frame(
            self, zoom_item=True, free_anchor=True)
        self._control_bar.place(
            width=self._size[0], height=60*k, y=self._size[1])
        self._play_button = _PlayButton(
            self._control_bar, (10*k, 10*k), (40*k, 40*k),
            command=lambda: (
                self._player.toggle_pause() if self._player else None,
                self._play_button._toggle())
        )
        self._timer = widgets.Text(
            self._control_bar, (130*k, 30*k), text="00:00 / 00:00",
            anchor="center", fontsize=round(20*k))
        self._progress_bar = widgets.Slider(
            self._control_bar, (215*k, 15*k), (750*k, 30*k),
            command=lambda p: (
                self._player.seek(p*self._player.get_metadata()
                                  ["duration"], relative=False),
                self._timer.set("%02d:%02d / %02d:%02d" % (
                    *divmod(round(
                        self._player.get_metadata()["duration"]*p), 60),
                    *divmod(round(
                        self._player.get_metadata()["duration"]), 60))))
            if self._player else None)
        _AudioImage(self._control_bar, (1000*k, 30*k), anchor="center")
        self._volume_bar = widgets.Slider(
            self._control_bar, (1035*k, 15*k), (180*k, 30*k), default=1,
            command=lambda p: self._player.set_volume(p)
            if self._player else None)
        _FullscreenToggleButton(
            self._control_bar, (1230*k, 10*k), (40*k, 40*k), fontsize=round(20*k),
            command=getattr(self.master, "fullscreen", lambda _: None)
        )

    def _display_control_bar(self, value: bool) -> None:
        """Animation for bottom bar"""
        if value:
            if getattr(self, "_slide", None) is not None:
                self.after_cancel(self._slide)
                self._slide = self.after(
                    5000, self._display_control_bar, False)
                return
            k, dy = -1, 0
            self._slide = self.after(5000, self._display_control_bar, False)
        else:
            rx, ry = self.winfo_rootx(), self.winfo_rooty() + self._size[1]
            px, py = self.winfo_pointerxy()
            if -self._control_bar._size[1] <= py-ry <= 0 <= px-rx <= self._size[0]:
                return self._display_control_bar(True)
            k, dy = 1, self._control_bar._size[1]
            self.after_cancel(self._slide)
            self.configure(cursor="none")
            self._slide = None

        animations.Animation(
            250, controllers.smooth, fps=60,
            callback=lambda p: self._control_bar.place(
                y=self._size[1] + self._control_bar._size[1]*p*k - dy)
        ).start()

"""APIs for playing videos"""

from ffpyplayer import player
from PIL import Image
from tkintertools.core import containers
from tkintertools.standard import widgets
from tkintertools.toolbox import enhanced

__all__ = [
    "VideoCanvas",
]


class VideoCanvas(containers.Canvas):
    """A canvas that is scalable and playable for videos"""

    # @typing.override
    def _initialization(self) -> None:
        containers.Canvas._initialization(self)
        self.video = widgets.Image(self, (0, 0), self.size)

    def _refresh(self) -> None:
        """Refresh the canvas"""
        frame, val = self.media.get_frame()
        if val != 'eof' and frame is not None:
            img, _ = frame
            self.video.set(enhanced.PhotoImage(Image.frombytes(
                "RGB", img.get_size(), bytes(img.to_bytearray()[0]))).resize(
                    *self._initial_size))
        self.after(16, self._refresh)

    def play(self, file: str) -> None:
        """Play the video"""
        self.media = player.MediaPlayer(file)
        self._refresh()

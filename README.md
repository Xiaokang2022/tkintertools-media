<h1 align="center">tkintertools-media</h1>

<p align="center">Extension package for tkintertools to media</p>

<p align="center">
<a href="https://github.com/Xiaokang2022/tkintertools-media/releases"><img alt="Version" src="https://img.shields.io/github/v/release/Xiaokang2022/tkintertools-media?include_prereleases&logo=github&label=Version" title="Latest Version" /></a>
<a href="https://pypistats.org/packages/tkintertools-media"><img alt="Downloads" src="https://img.shields.io/pypi/dm/tkintertools-media?label=Downloads&logo=pypi&logoColor=skyblue" title="Downloads" /></a>
<a href="https://pepy.tech/project/tkintertools-media"><img alt="Total Downloads" src="https://img.shields.io/pepy/dt/tkintertools-media?logo=pypi&logoColor=gold&label=Total%20Downloads" title="Total Downloads" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools-media"><img alt="Size" src="https://img.shields.io/github/languages/code-size/Xiaokang2022/tkintertools-media?label=Size&logo=github" title="Code Size"/></a>
<br/>
<a href="https://github.com/Xiaokang2022/tkintertools-media/watchers"><img alt="Watchers" src="https://img.shields.io/github/watchers/Xiaokang2022/tkintertools-media?label=Watchers&logo=github&style=flat" title="Watchers" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools-media/forks"><img alt="Forks" src="https://img.shields.io/github/forks/Xiaokang2022/tkintertools-media?label=Forks&logo=github&style=flat" title="Forks" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools-media/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/Xiaokang2022/tkintertools-media?label=Stars&color=gold&logo=github&style=flat" title="Stars" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools-media/issues"><img alt="Issues" src="https://img.shields.io/github/issues/Xiaokang2022/tkintertools-media?label=Issues&logo=github" title="Issues" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools-media/pulls"><img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/Xiaokang2022/tkintertools-media?label=Pull%20Requests&logo=github" title="Pull Requests" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools-media/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/Xiaokang2022/tkintertools-media?label=Discussions&logo=github" title="Discussions" /></a>
</p>

<p align="center">
<a href="https://github.com/Xiaokang2022/tkintertools-media/pulse"><img alt="Insights" src="https://repobeats.axiom.co/api/embed/0be944bbd1d27b25b519ea2ac7ffcdfbc98369fb.svg" /></a>
</p>

<p align="center">
    <a href="https://star-history.com/#Xiaokang2022/tkintertools-media&Date">
        <picture>
            <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Xiaokang2022/tkintertools-media&type=Date&theme=dark" />
            <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=Xiaokang2022/tkintertools-media&type=Date" />
            <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Xiaokang2022/tkintertools-media&type=Date" />
        </picture>
    </a>
</p>

📦 Installation
----------------

```bash
pip install tkintertools-media
```

> [!IMPORTANT]  
> `tkintertools`: https://github.com/Xiaokang2022/tkintertools

### 👀 Preview

> [!WARNING]  
> The sample video from: https://github.com/Xiaokang2022/tkintertools-demos/tree/main/assets/videos. Please note that the video is for testing purposes only and may not be used for commercial purposes!

![preview-1](./preview-1.png)

![preview-2](./preview-2.png)

```python
import tkintertools as tkt
import tkintertools.media as media

root = tkt.Tk(title="tkintertools-media")
cv = media.VideoCanvas(root, free_anchor=True, keep_ratio="min", controls=True)
cv.place(width=1280, height=720, x=640, y=360, anchor="center")
cv.open("your_video_file.mp4")
root.mainloop()
```

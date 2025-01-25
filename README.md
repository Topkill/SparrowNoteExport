# SparrowNoteExport
麻雀记图文笔记导出

> 注意：本程序只支持麻雀记中**类型为图文**的笔记导出。

## 步骤

可以下载源码使用 `python` 命令运行脚本，也可以直接下载 `release` 里的 `SparrowNoteExport.zip` 解压。

以下载 `release` 里的 `SparrowNoteExport.zip` 为例，

- `zip` 解压后可以得到两个 `exe` 程序

  ![image](https://github.com/user-attachments/assets/64963fd9-c3ee-446e-916f-adc2b16496e3)


- 首先双击运行 `麻雀记图文笔记导出.exe` ，输入备份文件绝对路径或拖动麻雀记的备份文件到程序窗口，回车即可，会在当前目录下生成一个 **麻雀记** 文件夹，里面是 `html` 格式的图文笔记

  ![image](https://github.com/user-attachments/assets/510db9f3-df01-40e4-9340-6a0db4ad0ff5)


- 之后如果想把 `html` 转换 `md` 文档，可以使用 `html转换md（保留源文件时间）.exe`，双击运行，软件会自动查找当前目录下的 **麻雀记** 文件夹，进行转换，生成 **麻雀记_md** 文件夹，存放转换后的 `md` 文档。

  ![image](https://github.com/user-attachments/assets/35a2d12a-2880-4814-b541-a9df674312c1)

  
  > 如果不想使用作者提供的 `html` 转 `md` 的程序（此程序我写的比较简单），可以自行寻找其他方案，比如找一个支持导入 `html` 的笔记软件，导入之后再导出为 `markdown` 文档。

到此已经完成了麻雀记图文笔记的导出。

但是因为麻雀记的笔记插入图片时是转换成图床链接存放在开发者的服务器上，所以程序导出的 `md` 文档里的图片是以图床链接形式存在。

为了防止开发者服务器关闭导致图片失效，推荐你使用其他工具进行离线化，

这里放两个我找到的实现离线化的开源工具，请自行探索：

https://github.com/YellowAndGreen/Md-ImgLocalize

https://github.com/HaujetZhao/Markdown-Toolbox

如果有更好的离线化工具，可以告诉我哦！ :smirk:

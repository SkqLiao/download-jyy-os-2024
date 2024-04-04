# Download JYY OS 2024

课程：南京大学 操作系统：设计与实现 (2024 春季学期) 蒋炎岩
主页：https://jyywiki.cn/OS/2024/

## 功能

- 下载示例代码
- 将同一节的课件打包成一个（可以本地运行的）HTML和PDF（实现方式：图像转base64、其他链接转为绝对路径）

## 使用方法

```shell
pip install -r requirements.txt
```

```shell
> python run.py -h
usage: run.py [-h] [--force] [--lectures LECTURES [LECTURES ...]] [--logging]

下载jyy OS 2024 讲义与代码

options:
  -h, --help            show this help message and exit
  --force               强制下载（否则若文件夹存在则不下载）
  --lectures LECTURES [LECTURES ...]
                        指定要下载的Lecture序号
  --logging             输出日志信息
```

其中 `convert.py` 是下载课件并转换为HTML和PDF的脚本，`get.py` 是下载示例代码的脚本。

文件会下载到当前路径的`os_lectures`文件夹下，第`num`节课的文件夹为`./os_lectures/lec{num}`。

## 结果

```shell
> python run.py --lectures 1 2 --force
Running convert.py on Lecture 1
Running get.py on Lecture 1
Running convert.py on Lecture 2
Running get.py on Lecture 2
Processing lectures: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:41<00:00, 20.75s/it]

> tree lec1 lec2 -L 1

lec1
├── 1.1.html
├── 1.2.html
├── 1.3.html
├── 1.4.html
├── lec1.html
├── lec1.pdf
├── logisim
├── mini-rv32ima
└── tar
lec2
├── 2.1.html
├── 2.2.html
├── 2.3.html
├── 2.4.html
├── compiler-opt
├── hanoi
├── lec2.html
├── lec2.pdf
├── minimal
├── strace
└── tar
```

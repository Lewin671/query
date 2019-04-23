# 有道词典terminal版 2.0

## 下载
`git clone https://github.com/Lewin671/query.git`, 欢迎大家pull和star。

### 安装说明: 

#### for linux
1. 安装Python相关库： `pip install -r requirements.txt`。

2. 进入项目的文件夹，然后在终端下执行命令:`bash startup.sh` 或者`./startup.sh`。

#### for windows
1. 安装Python相关库： `pip install -r requirements.txt`。

2. 进入项目的文件夹，然后以管理员身份运行`startup.bat`。

3. 安装`cmder`终端，并设置`cmder_home`系统变量。

### 使用说明：

1. 默认查询命令是`query [单词或者短语]`。如果需要更改命令，请在`~/.bashrc`中更改别名(alias)。

2. 如果有例句有显示出来，最多显示三条。

3. 默认发音为英式发音，可以在`config.py`更改相关配置．

注： 似乎有些电脑无法使用正常pygame，如果遇到这种情况，那么最好把播放读音的配置关闭。
   
### 效果

注： 颜色可以在main.py自行更改。

![example1](./pic/example1.png)

![example2](./pic/example2.png)

### 此次更新

1. 将原来使用笨重的Scrapy框架改为轻量级的requests框架，可以加快查询的速度。

2. 优化数据库结构。这里采用python的sqlalchemy来实现ORM数据库模型，从而让模型更加明确，代码更加结构化。

3. 使用双线程分别播放读音和显示翻译答案。这也大大加快了查询的速度。 

4. 整体优化项目结构．

5. 添加了Windows下的使用方法。

### 目标更新

这个项目是不断改进的项目，从一开始到现在的优化，至少在查询速度方面已经快了很多了，不会让人有等待感（除非网络不好而且没有查询过）。当然，这个项目也不仅仅就到此为止，这里先给出以后更新的设想：

1. 添加查询统计，用来分析自己常用的查询单词。

2. 添加整句翻译

注意： 该项目仅仅供自己学习和分享给大家学习用途。如果有问题可以通过邮箱联系我：2596736318@qq.com




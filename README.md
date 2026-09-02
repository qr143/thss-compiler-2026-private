# thss-compiler-2026

该仓库是清华大学软件学院《汇编与编译原理》2026年秋季课程的代码实验仓库。

`README.md` 中的内容节选自《实验手册》 PA0 环境配置章节，阅读一次即可。

## Cloning this Repository

1. 在你的 GitHub 账号下创建一个新的仓库，给它取一个名字（例如 `thss-compiler-2026-private`），并将访问权限设置为 **Private**。

2. 在你的开发机上，对课程公共仓库做一次裸克隆：

```shell :no-line-numbers
git clone --bare https://github.com/Nboxff/thss-compiler-2026.git thss-compiler-2026-public
```

3. 接下来，把公共仓库中的所有内容镜像到你自己的私有仓库。假设你的 GitHub 用户名是 `student`、私有仓库名是 `thss-compiler-2026-private`，镜像的命令如下：

```shell :no-line-numbers
cd thss-compiler-2026-public

# 使用 HTTPS 拉取 / 推送
git push https://github.com/student/thss-compiler-2026-private.git main

# 使用 SSH 拉取 / 推送
git push git@github.com:student/thss-compiler-2026-private.git main
```

这一步会把公共仓库中的所有内容复制到你的私有仓库。现在你可以删除本地这份公共仓库的裸克隆：

```shell :no-line-numbers
cd ..
rm -rf thss-compiler-2026-public
```

4. 克隆你的私有仓库到开发机

```shell :no-line-numbers
# 使用 HTTPS 拉取 / 推送
git clone https://github.com/student/thss-compiler-2026-private.git

# 使用 SSH 拉取 / 推送
git clone git@github.com:student/thss-compiler-2026-private.git
```

5. 将课程公共仓库添加为第二个远程仓库，这样你就能够在本学期中随时拉取课程公共仓库的更新，并与你编写的代码进行合并：

```shell :no-line-numbers
git remote add upstream https://github.com/Nboxff/thss-compiler-2026.git
```

你可以用下面的命令验证远程是否添加成功：

```shell :no-line-numbers
git remote -v
# origin	https://github.com/student/thss-compiler-2026-private.git (fetch)
# origin	https://github.com/student/thss-compiler-2026-private.git (push)
# upstream	https://github.com/Nboxff/thss-compiler-2026.git (fetch)
# upstream	https://github.com/Nboxff/thss-compiler-2026.git (push)
```

现在，你可以根据需要把课程公共仓库的更新拉取到本地：

```shell :no-line-numbers
git pull upstream main
```

在之后的每次实验开始前，你需要执行下面的命令，获取最新的实验仓库代码：

```shell :no-line-numbers
git pull upstream main
```

## Setup

1. 在命令行（终端）执行下面的命令：

```shell :no-line-numbers
sudo apt update
sudo apt install build-essential cmake git pkg-config python3 openjdk-11-jdk curl clang git zip
```

2. 安装 ANTLR4。从官网下载 antlr-4.13.1 的 jar 包:

```shell :no-line-numbers
sudo curl -L -o /usr/local/lib/antlr-4.13.1-complete.jar https://www.antlr.org/download/antlr-4.13.1-complete.jar
```

将下面的内容添加到`~/.bashrc`或`~/.zshrc`来设置环境变量和别名：

```shell
export CLASSPATH=/usr/local/lib/antlr-4.13.1-complete.jar:.
alias antlr4='java -jar /usr/local/lib/antlr-4.13.1-complete.jar'
```

在更改完 ~/.bashrc 或 ~/.zshrc 之后，可以使用 `source` 命令使更改立即生效，如 `source ~/.bashrc`

## Build

进入对应的实验目录，以`pa0`为例:

``` shell :no-line-numbers
cd pa0
```

部分项目使用 CMake 构建，在项目根目录(`pa0/`)的命令行中执行下面的命令：

```shell :no-line-numbers
mkdir build
cd build
cmake ..
make -j4
```

## Submit

在完成代码开发后，在项目根目录(`pa0/`)的命令行中执行下面的命令，生成提交到 GradeScope 的压缩包：

```shell :no-line-numbers
python3 package.py
```

期望的压缩包结构：

```
pa0.zip
└── word_counter.cpp
```

而不是：
```
pa0.zip
└── pa0
    └── word_counter.cpp
```

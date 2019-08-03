# Ubuntu上非常实用的命令行工具！

Ubuntu的默认命令行工具是bash，配置文件是`.bashrc`。

1. 首先，放弃`bash`，使用`zsh`：`sudo apt install zsh`

2. 将`.bashrc`中配置的别名、变量，以及其他配置转移到`.zshrc`中

```shell
cp ~/.bashrc ~/.zshrc
# 删除无用的行
vim .zshrc
```

3. 安装`oh-my-zsh`

一个zsh的扩展库，让zsh简单易用，并且用更强大的的功能、主题和插件。

github地址：https://github.com/robbyrussell/oh-my-zsh

- 安装

```shell
sh -c "$(wget -O- https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

编辑.zshrc，`vim .zshrc`

```shell
# 主题
ZSH_THEME="agnoster"
# 插件
plugins={
      git
      git-open
      }
```
主题需要支持powerline字体，安装powerline字体：

powerline字体github页面：https://github.com/powerline/fonts

```shell
# 可能需要设置字体为powerline
sudo apt install fonts-powerline
```

4. ccat

ccat is the colorizing cat. It works similar to cat but displays content with syntax highlighting.

github地址：https://github.com/jingweno/ccat

使用方法：

下载rlease中的对应版本，解压，里面是二进制文件（不是source压缩文件），将`ccat`文件复制到`/usr/`目录下，就可以使用`ccat [filename]`命令了


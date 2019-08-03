# Ubuntu上非常实用的命令行工具！

Ubuntu的默认命令行工具是bash，配置文件是`.bashrc`。

## 首先，放弃`bash`


使用`zsh`：`sudo apt install zsh`

将`.bashrc`中配置的别名、变量，以及其他配置转移到`.zshrc`中

```shell
cp ~/.bashrc ~/.zshrc
# 删除无用的行
vim .zshrc
```

## 安装`oh-my-zsh`

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

## ccat

ccat is the colorizing cat. It works similar to cat but displays content with syntax highlighting.

github地址：https://github.com/jingweno/ccat

使用方法：

下载rlease中的对应版本，解压，里面是二进制文件（不是source压缩文件），将`ccat`文件复制到`/usr/`目录下，就可以使用`ccat [filename]`命令了

## tldr

tldr是一个可以用来代替Linux命令行中的`man`命令的命令行工具

github地址：https://github.com/tldr-pages/tldr-python-client

- 安装

```shell
pip install tldr
tldr tar
# tar                                                                              
                                                                                   
  Archiving utility.                                                               
  Often combined with a compression method, such as gzip or bzip.                  
  More information: <https://www.gnu.org/software/tar>.                            
                                                                                   
- Create an archive from files:                                                    
                                                                                   
  tar -cf target.tar file1 file2 file3                                             
                                                                                   
- Create a gzipped archive:                                                        
                                                                                   
  tar -czf target.tar.gz file1 file2 file3                                         
                                                                                   
- Extract an archive in a target directory:                                        
                                                                                   
  tar -xf source.tar -C directory                                                  
                                                                                   
- Extract a gzipped archive in the current directory:                              
                                                                                   
  tar -xzf source.tar.gz                                                           
                                                                                   
- Extract a bzipped archive in the current directory:                              
                                                                                   
  tar -xjf source.tar.bz2                                                          
                                                                                   
- Create a compressed archive, using archive suffix to determine the compression program:
                                                                                   
  tar -caf target.tar.xz file1 file2 file3                                         
                                                                                   
- List the contents of a tar file:                                                 
                                                                                   
  tar -tvf source.tar                                                              
                                                                                   
- Extract files matching a pattern:                                                
                                                                                   
  tar -xf source.tar --wildcards "*.html" 
```

可以直接使用，也可以在`.zshrc`中自定义他的颜色输出，`vim .zshrc`

```shell
export TLDR_COLOR_BLANK="white"
export TLDR_COLOR_NAME="cyan"
export TLDR_COLOR_DESCRIPTION="white"
export TLDR_COLOR_EXAMPLE="green"
export TLDR_COLOR_COMMAND="red"
export TLDR_COLOR_PARAMETER="white"
export TLDR_CACHE_ENABLED=1
export TLDR_CACHE_MAX_AGE=720
```



#!/usr/bin/env sh
set -e;

echo "安装brew环境"
command -v brew || /bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
# 一些备用的命令，如果brew安装东西慢可以修改brew的下载源地址为国内地址，达到提速目的
# 修改brew镜像源
# git -C "$(brew --repo)" remote set-url origin https://mirrors.ustc.edu.cn/brew.git
# 修改homebrew-core镜像源
# git -C "$(brew --repo homebrew/core)" remote set-url origin https://mirrors.ustc.edu.cn/homebrew-core.git
# 修改homebrew-cask镜像源（需要安装后才能修改）
# git -C "$(brew --repo homebrew/cask)" remote set-url origin https://mirrors.ustc.edu.cn/homebrew-cask.git
# 更新
brew update

plugins=()

# 安装ohmyzsh配置
curl https://gitee.com/mirrors/oh-my-zsh/raw/master/tools/install.sh | sh
echo "########## ohmyzsh 安装成功."
# 安装命令提示插件
git clone https://github.com/zsh-users/zsh-autosuggestions \
 ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && plugins[0]="zsh-autosuggestions"
echo "########## ohmyzsh插件zsh-autosuggestions 安装成功."
# 安装shell语法高亮插件
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git \
 ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting && plugins[1]="zsh-syntax-highlighting"

echo "########## ohmyzsh插件zsh-stntax-highlighting 安装成功."

space=" "
for $i in ${plugins[@]}; do $space=$space+i done
echo "插件配置写入.zshrc文件 >>>> {$space}"
# Mac版sed奇怪的语法，-i后面根两个字符串，第一个为备份文件名，第二个为替换正则
sed -i '' "s/(git/(git {$space}/g" cache || echo "插件配置写入.zshrc文错误，手动将{$space}添加到 plugins=(git 后面"

echo "ohmyzsh环境配置完毕"
source ~/.zshrc

echo "安装翻译工具Bob，php包管理软件composer，wget"
brew install bob composer wget
echo "开始下载docker compose文件"
curl https://gitee.com/belingud/sources/raw/master/utils/config/env_init/docker-compose.yml > docker-compose.yml
curl https://gitee.com/belingud/sources/raw/master/utils/config/env_init/Dockerfile > Dockerfile
echo "docker compose文件下载完成，根据环境修改后在compose目录下使用 docker-compose up -d 启动"

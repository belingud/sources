#!/bin/bash
set -e;

echo "安装brew环境"
command -v brew || git clone --depth=1 https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/install.git brew-install ; /bin/bash brew-install/install.sh ; rm -rf brew-install
# 一些备用的命令，如果brew安装东西慢可以修改brew的下载源地址为国内地址，达到提速目的
# 修改brew镜像源
# git -C "$(brew --repo)" remote set-url origin https://mirrors.ustc.edu.cn/brew.git
# 修改homebrew-core镜像源
# git -C "$(brew --repo homebrew/core)" remote set-url origin https://mirrors.ustc.edu.cn/homebrew-core.git
# 修改homebrew-cask镜像源（需要安装后才能修改）
# git -C "$(brew --repo homebrew/cask)" remote set-url origin https://mirrors.ustc.edu.cn/homebrew-cask.git
# 替换上游brew
brew tap --custom-remote --force-auto-update homebrew/core https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git
brew tap --custom-remote --force-auto-update homebrew/cask https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-cask.git

# 除 homebrew/core 和 homebrew/cask 仓库外的 tap 仓库仍然需要设置镜像
brew tap --custom-remote --force-auto-update homebrew/command-not-found https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-command-not-found.git
brew update
echo "brew环境安装完成"
brew update

plugins=()

# 安装ohmyzsh配置
command -v omz || curl https://gitee.com/mirrors/oh-my-zsh/raw/master/tools/install.sh | sh
echo "########## ohmyzsh 安装成功."

# 安装命令提示插件
if [ ! -d ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions ]; then
    git clone https://github.com/zsh-users/zsh-autosuggestions \
    ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && plugins[0]="zsh-autosuggestions"
fi
echo "########## ohmyzsh插件zsh-autosuggestions 安装成功."

# 安装shell语法高亮插件
if [ ! -d ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting ]; then
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git \
    ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting && plugins[1]="zsh-syntax-highlighting"
fi

echo "########## ohmyzsh插件zsh-stntax-highlighting 安装成功."

# 安装pypi ohmyzsh插件
if [ ! -d ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/pypi ]; then
    git clone https://github.com/belingud/pypi \
    ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/pypi && plugins[2]="pypi"
fi

space=" "
for $i in ${plugins[@]}; do $space=$space+i done
echo "插件配置写入.zshrc文件 >>>> {$space}"
# Mac版sed奇怪的语法，-i后面根两个字符串，第一个为备份文件名，第二个为替换正则
sed -i '' "s/(git/(git {$space}/g" cache || echo "插件配置写入.zshrc文错误，手动将{$space}添加到 plugins=(git 后面"

echo "ohmyzsh环境配置完毕"
source ~/.zshrc

# echo "安装翻译工具Bob，php包管理软件composer，wget"
# brew install bob composer wget
# echo "开始下载docker compose文件"
# curl https://gitee.com/belingud/sources/raw/master/utils/config/env_init/docker-compose.yml > docker-compose.yml
# curl https://gitee.com/belingud/sources/raw/master/utils/config/env_init/Dockerfile > Dockerfile
# echo "docker compose文件下载完成，根据环境修改后在compose目录下使用 docker-compose up -d 启动"

echo "############# Install pyenv #############"
brew install pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

echo "############# Install CHANGELOG generator git cliff #############"
brew install git-cliff

echo "############# Install git-delta #############"
brew install git-delta
git config --global core.pager "delta"
git config --global interactive.diffFilter "delta --color-only --color-words"
git config --global merge.conflictstyle diff3
git config --global diff.colorMoved default
git config --global delta.line-numbers true
git config --global delta.navigate true
git config --global delta.syntax-theme 'GitHub'

echo "############# Clone delta repo to ~/.config/delta #############"
git clone https://github.com/dandavison/delta.git ~/.config/delta
git config --global include.path $HOME/.config/delta/themes.gitconfig
echo "############# Set delta theme to villsau #############"
git config --global delta.features villsau

echo "############# Install wget/axel/bat/ccat/htop/tldr/dblab/tssh/fzf/ruff/gdu/yt-dlp/jq #############"
command -v wget || brew install wget
command -v axel || brew install axel
command -v bat || brew install bat
command -v ccat || brew install ccat
command -v htop || brew install htop
command -v tldr || brew install tldr
command -v dlab || brew install dlab
command -v tssh || brew install tssh
command -v fzf || brew install fzf
command -v redis-cli || brew install aoki/homerew-redis-cli/redis-cli
command -v gdu || brew install gdu
command -v ruff || brew install ruff
command -v yt-dlp || brew install yt-dlp
command -v jq || brew install jq

echo "############# Install thefuck #############"
command -v thefuck || brew install thefuck
echo 'eval $(thefuck --alias)' >> ~/.zshrc

echo "############# Install pipx #############"
brew install pipx
pipx ensurepath

echo "############# Install charmbracelet/tap/freeze #############"
command -v freeze || brew install charmbracelet/tap/freeze

echo "############# Install just #############"
command -v just || brew install just

echo "############# Install gh #############"
command -v gh || brew install gh

echo "############# Install dozer/onlyoffice/iina/pot/orbstack/qlcolorcode/qlstephen/qlmarkdown/qlimagesize/quicklook-json/openinterminal/lulu/insomnia/warp #############"
brew install --cask dozer onlyoffice iina pot orbstack qlcolorcode qlstephen qlmarkdown qlimagesize quicklook-json openinterminal lulu insomnia warp

echo "############# Install android-file-transfer/visual-studio-code/localsend #############"
brew install --cask android-file-transfer
command -v code || brew install --cask visual-studio-code
brew install --cask localsend

echo "############# Install mise #############"
command -v mise || brew install mise
echo 'eval "$(~/.local/bin/mise activate zsh)"' >> ~/.zshrc
echo 'export PATH="$HOME/.local/share/mise/shims:$PATH"' >> ~/.zprofile
echo '# let mise load .env
export MISE_ENV_FILE=.env' >> ~/.zshrc

echo "############# Install gibo ###############"
command -v gibo || brew install simonwhitaker/tap/gibo

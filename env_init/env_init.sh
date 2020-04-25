command_exists() {
    command -v "$@"
}

install_package() {
    if ((whoami == root)); then
        sh -c 'apt install -y $@'
    else
        sh -c 'sudo apt install -y $@'
    fi
}

check_and_install() {
    for comm in $@; do
        command_exists $comm || {
            echo "############### $comm not found, install $comm ################"
            install_package $comm
        }
    done
}

check_and_install git wget curl
echo "################git wget curl installed###############"
sh -c "$(curl https://pyenv.run | bash)"
echo "################pyenv installed##############"
check_and_install zsh
echo "###############zsh installed#################"
sh -c "$(wget -O- --no-check-certificate https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# if (( uname -s == Linux))
# then
#     wget -P ~/downloads https://github.com/jingweno/ccat/releases/download/v1.1.0/linux-amd64-1.1.0.tar.gz
# fi

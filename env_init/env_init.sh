command_exists() {
    command "$@"
}

install_package() {
    if ((whoami == root)); then
        apt install -y $@
    else
        sudo apt install -y $@
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

check_and_install zsh git wget curl
curl https://pyenv.run | bash
sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# if (( uname -s == Linux))
# then
#     wget -P ~/downloads https://github.com/jingweno/ccat/releases/download/v1.1.0/linux-amd64-1.1.0.tar.gz
# fi

# 好用的Mac工具和Mac技巧

## 卸载Nix

>emove Nix from launchd (see `/Library/LaunchDaemons` and `~/Library/LaunchDaemons`)
>Remove nix from `/etc/synthetic.conf`
>Remove nix from `/etc/fstab` (use `vifs`)
>Remove Nix from shell (e.g. `~/.zshrc`)
>(good time to reboot)
>Remove Nix APFS volume (not sure how to do this in shell, but the Disk Utility app should do the trick)
>Remove Nix user group (once again not sure how to with shell, can System Preferences > Users & Groups covers this)
>Users can be removed with dscl (e.g. sudo dscl . delete `/Users/_nixbld1`)
>Remove any nix traces in ~/Applications (none in my case)
>Remove .nix* files in `~/`, `~/.config` and `~/.cache`
>Remove /etc/nix
>Remove .nix* files in `/var/root/` and `/var/root/.cache`
>Cleanup `/etc/bash.bashrc`, `/etc/bashrc`
>Cleanup `/etc/zshrc`

## 浏览器

### cookie

导出浏览器cookies的命令行工具

`cookies`

安装:`brew install barnardb/cookies/cookies`,github地址：https://github.com/barnardb/cookies

golang写的命令行工具，浏览器支持使用的是 [kooky](https://github.com/zellyn/kooky)，支持的浏览器可以在仓库中查看，截止2024.10.1不支持Arc浏览器


```bash
$ cookies https://www.youtube.com -b chrome
CONSENT=WP.28a5e4;PREF=f6=400000
```

## 下载

批量下载bilibili视频，并且使用分P的标题作为文件名：`lux`

安装：`brew install lux`，github地址：https://github.com/iawia002/lux

使用golang写的命令行下载工具，可以结合`cookies`来使用

下载bilibili合集视频，并使用分P的标题作为文件名

```bash
lux -eto -c $(cookies https://www.bilibili.com) BV1xp4y1f7HP
```

普通下载

```bash
lux -c $(cookies https://www.bilibili.com) https://www.bilibili.com/video/BV1X5tSe9EDg
```

```bash
$ lux "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

 Site:      YouTube youtube.com
 Title:     Rick Astley - Never Gonna Give You Up (Video)
 Type:      video
 Stream:
     [248]  -------------------
     Quality:         1080p video/webm; codecs="vp9"
     Size:            63.93 MiB (67038963 Bytes)
     # download with: lux -f 248 ...

 41.88 MiB / 63.93 MiB [=================>-------------]  65.51% 4.22 MiB/s 00m05s
```

## rar

brew中的unrar包被移除，如果想使用原版的unrar包，可以使用github用户的备份：

```bash
brew install carlocab/personal/unrar
```

github地址：https://github.com/carlocab/homebrew-personal


## 网络

### 防火墙

lulu，Mac上的开源GUI防火墙软件，mac的设置中禁止联网不生效，可以使用lulu来进行联网管理，在程序进行联网前会询问是否同意，同意后会添加到规则中。可以用来禁止WPS联网

```bash
brew install lulu
```

## 插件

### wechat

wechattweak-cli：防撤回

```bash
brew install wechattweak-cli
# 使用
sudo wechattweak-cli install
```

## 实用工具

### itsycal
itsycal，日历应用，可以在菜单栏中查看

```bash
brew install itsycal
```

### ghostty

ghostty，终端应用

```bash
brew install ghostty
```

### timg

timg，终端查看图片的工具，支持kitty协议和iterm2协议

```bash
brew install timg
```


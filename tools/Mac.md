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


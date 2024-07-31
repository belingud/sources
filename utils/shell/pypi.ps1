#!/usr/bin/env pwsh

function pypi {
    param (
        [string]$Command,
        [string[]]$Options
    )

    $help = @"
Usage: pypi <command> [options]

Commands:
  list                 List all supported PyPI mirrors and their URLs.
  use <shortname>      Switch to a specified PyPI mirror. Replace <shortname> with the desired mirror's shortname.
  ping <shortname|url> Check network connectivity to a specified PyPI mirror or URL.

Options:
  -h, --help           Show this help message and exit.

Examples:
  pypi list            # Lists all supported PyPI mirrors
  pypi use aliyun      # Switches to the Alibaba Cloud mirror
  pypi ping tsinghua   # Checks connectivity to the Tsinghua University mirror
  pypi ping https://pypi.org/simple/  # Checks connectivity to the official PyPI URL

For more details on each command, you can run:
  pypi <command> -h/--help

Note:
  The 'ping' command can accept either a mirror shortname or a direct URL.
  The 'use' command requires a valid shortname from the list of supported mirrors.
"@

    function Print-Help {
        Write-Output $help
    }

    if (-not $Command) {
        Print-Help
        return
    }

    function List-Mirrors {
        Write-Output "Supported PyPI mirrors:"
        Write-Output "[Shortname]    [URL]"
        Write-Output "pypi:          https://pypi.org/simple/"                             # PyPI Official
        Write-Output "aliyun:        https://mirrors.aliyun.com/pypi/simple/"              # Alibaba Cloud
        Write-Output "tencent:       https://mirrors.cloud.tencent.com/pypi/simple/"       # Tencent Cloud
        Write-Output "huawei:        https://repo.huaweicloud.com/repository/pypi/simple/" # Huawei Cloud
        Write-Output "163:           https://mirrors.163.com/pypi/simple/"                 # 163
        Write-Output "volces:        https://mirrors.volces.com/pypi/simple/"              # Volces/HuoShan Engine
        Write-Output "cernet:        https://mirrors.cernet.edu.cn/pypi/web/simple/"       # China Education and Research Network
        Write-Output "tsinghua:      https://pypi.tuna.tsinghua.edu.cn/simple/"            # Tsinghua University
        Write-Output "sustech:       https://mirrors.sustech.edu.cn/pypi/web/simple/"      # Southern University of Science and Technology
        Write-Output "bfsu:          https://mirrors.bfsu.edu.cn/pypi/web/simple/"         # Beijing Foreign Studies University
        Write-Output "nju:           https://mirror.nju.edu.cn/pypi/web/simple/"           # Nanjing University
        Write-Output "dnui:          https://mirrors.neusoft.edu.cn/pypi/web/simple/"      # Dalian Neusoft University of Information
        Write-Output "pku:           https://mirrors.pku.edu.cn/pypi/web/simple/"          # Peking University
        Write-Output "njtech:        https://mirrors.njtech.edu.cn/pypi/web/simple/"       # Nanjing Tech University
        Write-Output "nyist:         https://mirrors.njtech.edu.cn/pypi/web/simple/"       # Nanyang Institute of Technology
        Write-Output "sjtu:          https://mirror.sjtu.edu.cn/pypi/web/simple/"          # Shanghai Jiao Tong University
        Write-Output "zju:           https://mirrors.zju.edu.cn/pypi/web/simple/"          # Zhejiang University
        Write-Output "jlu:           https://mirrors.jlu.edu.cn/pypi/web/simple/"          # Jilin University
        Write-Output "testpypi:      https://test.pypi.org/simple/"                        # Test PyPI
    }

    function Use-Mirror {
        param (
            [string]$Shortname
        )

        if (-not $Shortname -or $Shortname -eq "--help" -or $Shortname -eq "-h") {
            Write-Output @"
Usage: pypi use <shortname>

Switches to a specified PyPI mirror. Replace <shortname> with the desired mirror's shortname.
Example: pypi use aliyun
"@
            return
        }

        $index_url = $null
        $trusted_host = $null

        switch ($Shortname) {
            "pypi" { $index_url = "https://pypi.org/simple/"; $trusted_host = "pypi.org" }
            "aliyun" { $index_url = "https://mirrors.aliyun.com/pypi/simple/"; $trusted_host = "mirrors.aliyun.com" }
            "tencent" { $index_url = "https://mirrors.cloud.tencent.com/pypi/simple/"; $trusted_host = "mirrors.cloud.tencent.com" }
            "163" { $index_url = "https://mirrors.163.com/pypi/simple/"; $trusted_host = "mirrors.163.com" }
            "volces" { $index_url = "https://mirrors.volces.com/pypi/simple/"; $trusted_host = "mirrors.volces.com" }
            "huawei" { $index_url = "https://repo.huaweicloud.com/repository/pypi/simple/"; $trusted_host = "repo.huaweicloud.com" }
            "testpypi" { $index_url = "https://test.pypi.org/simple/"; $trusted_host = "test.pypi.org" }
            "cernet" { $index_url = "https://mirrors.cernet.edu.cn/pypi/web/simple/"; $trusted_host = "mirrors.cernet.edu.cn" }
            "tsinghua" { $index_url = "https://pypi.tuna.tsinghua.edu.cn/simple/"; $trusted_host = "pypi.tuna.tsinghua.edu.cn" }
            "sustech" { $index_url = "https://mirrors.sustech.edu.cn/pypi/web/simple/"; $trusted_host = "mirrors.sustech.edu.cn" }
            "bfsu" { $index_url = "https://mirrors.bfsu.edu.cn/pypi/web/simple/"; $trusted_host = "mirrors.bfsu.edu.cn" }
            "nju" { $index_url = "https://mirror.nju.edu.cn/pypi/web/simple/"; $trusted_host = "mirror.nju.edu.cn" }
            "dnui" { $index_url = "https://mirrors.neusoft.edu.cn/pypi/web/simple/"; $trusted_host = "mirrors.neusoft.edu.cn" }
            "pku" { $index_url = "https://mirrors.pku.edu.cn/pypi/web/simple/"; $trusted_host = "mirrors.pku.edu.cn" }
            "njtech" { $index_url = "https://mirrors.njtech.edu.cn/pypi/web/simple/"; $trusted_host = "mirrors.njtech.edu.cn" }
            "nyist" { $index_url = "https://mirrors.njtech.edu.cn/pypi/web/simple/"; $trusted_host = "mirrors.njtech.edu.cn" }
            "sjtu" { $index_url = "https://mirror.sjtu.edu.cn/pypi/web/simple/"; $trusted_host = "mirror.sjtu.edu.cn" }
            "zju" { $index_url = "https://mirrors.zju.edu.cn/pypi/web/simple/"; $trusted_host = "mirrors.zju.edu.cn" }
            "jlu" { $index_url = "https://mirrors.jlu.edu.cn/pypi/web/simple/"; $trusted_host = "mirrors.jlu.edu.cn" }
            "nwafu" { $index_url = "https://mirrors.nwafu.edu.cn/pypi/"; $trusted_host = "mirrors.nwafu.edu.cn" }
            default { Write-Output "Unknown mirror: $Shortname"; return 1 }
        }

        pip config set global.index-url $index_url
        pip config set install.trusted-host $trusted_host

        Write-Output "Switched to $Shortname: $index_url"
    }

    function Ping-Mirror {
        param (
            [string]$ShortnameOrUrl
        )

        if (-not $ShortnameOrUrl -or $ShortnameOrUrl -eq "--help" -or $ShortnameOrUrl -eq "-h") {
            Write-Output @"
Usage: pypi ping <shortname|url>

Checks network connectivity to a specified PyPI mirror or URL.
Example: pypi ping tsinghua
"@
            return
        }

        $url = $null
        switch ($ShortnameOrUrl) {
            "pypi" { $url = "https://pypi.org/simple/" }
            "aliyun" { $url = "https://mirrors.aliyun.com/pypi/simple/" }
            "tencent" { $url = "https://mirrors.cloud.tencent.com/pypi/simple/" }
            "163" { $url = "https://mirrors.163.com/pypi/simple/" }
            "volces" { $url = "https://mirrors.volces.com/pypi/simple/" }
            "huawei" { $url = "https://repo.huaweicloud.com/repository/pypi/simple/" }
            "testpypi" { $url = "https://test.pypi.org/simple/" }
            "cernet" { $url = "https://mirrors.cernet.edu.cn/pypi/web/simple/" }
            "tsinghua" { $url = "https://pypi.tuna.tsinghua.edu.cn/simple/" }
            "sustech" { $url = "https://mirrors.sustech.edu.cn/pypi/web/simple/" }
            "bfsu" { $url = "https://mirrors.bfsu.edu.cn/pypi/web/simple/" }
            "nju" { $url = "https://mirror.nju.edu.cn/pypi/web/simple/" }
            "dnui" { $url = "https://mirrors.neusoft.edu.cn/pypi/web/simple/" }
            "pku" { $url = "https://mirrors.pku.edu.cn/pypi/web/simple/" }
            "njtech" { $url = "https://mirrors.njtech.edu.cn/pypi/web/simple/" }
            "nyist" { $url = "https://mirrors.njtech.edu.cn/pypi/web/simple/" }
            "sjtu" { $url = "https://mirror.sjtu.edu.cn/pypi/web/simple/" }
            "zju" { $url = "https://mirrors.zju.edu.cn/pypi/web/simple/" }
            "jlu" { $url = "https://mirrors.jlu.edu.cn/pypi/web/simple/" }
            "nwafu" { $url = "https://mirrors.nwafu.edu.cn/pypi/" }
            default { $url = $ShortnameOrUrl }
        }

        if ($url -notmatch "^https://") {
            Write-Output "Error: $url is not a valid URL"
            return 1
        }

        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -ErrorAction SilentlyContinue
        $status = $response.StatusCode
        $delay = $response.ResponseTime

        $delay = [math]::Round($delay * 1000, 2)
        $max_status = 300
        if ($ShortnameOrUrl -eq "cernet") {
            $max_status = 400
        }

        if ($status -ge 200 -and $status -lt $max_status) {
            Write-Output "Mirror $url is REACHABLE (status: $status, delay: $delay ms)"
        } else {
            Write-Output "Error: $url is UNREACHABLE (status: $status, delay: $delay ms)"
        }
    }

    switch ($Command) {
        "list" { List-Mirrors }
        "use" { Use-Mirror @Options }
        "ping" { Ping-Mirror @Options }
        "-h" { Print-Help }
        "--help" { Print-Help }
        "help" { Print-Help }
        "" { Print-Help }
        default { Write-Output "Invalid command: $Command"; Print-Help }
    }
}
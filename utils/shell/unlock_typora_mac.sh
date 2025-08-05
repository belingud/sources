#!/bin/bash
# 使用gitee链接获取并执行
# curl -fsSL https://gitee.com/belingud/sources/raw/master/utils/shell/unlock_typora_mac.sh | bash

# 检测并设置sed命令
if command -v gsed >/dev/null 2>&1; then
    SED_CMD="gsed"
    echo "检测到 gsed 命令，使用 GNU sed"
else
    SED_CMD="sed"
    echo "使用系统默认 sed 命令"
    echo "💡 提示: 如果遇到问题，可以使用 'brew install gnu-sed' 安装 gsed 命令"
fi

# 导航到指定目录
TARGET_DIR="/Applications/Typora.app/Contents/Resources/TypeMark/page-dist/static/js/"
echo "正在处理 Typora 许可证文件..."

# 检查目录是否存在
if [ ! -d "$TARGET_DIR" ]; then
    echo "错误: 目录不存在: $TARGET_DIR"
    exit 1
fi

# 切换到目标目录
cd "$TARGET_DIR" || exit 1
echo "已切换到目录: $(pwd)"

# 查找LicenseIndex相关的JS文件
JS_FILE=$(find . -name "LicenseIndex*.js" | head -1)
if [ -z "$JS_FILE" ]; then
    echo "错误: 未找到 LicenseIndex 相关的JS文件"
    echo "当前目录中的JS文件:"
    ls -la *.js 2>/dev/null || echo "未找到JS文件"
    exit 1
fi

# 移除前面的 ./
JS_FILE=${JS_FILE#./}
echo "找到文件: $JS_FILE"

# 首先检查是否已经破解
if grep -q 'hasActivated="true"=="true"' "$JS_FILE"; then
    echo "✅ 检测到文件已被破解 (存在 hasActivated=\"true\"==\"true\")"
    echo "无需重复运行脚本"
    exit 0
fi

# 搜索并替换
echo "搜索并修改 hasActivated 相关代码..."
echo "使用 $SED_CMD 命令进行替换..."

# 检查文件中是否包含目标字符串并尝试替换
if grep -q 'hasActivated="true"==e\.hasActivated' "$JS_FILE"; then
    echo "找到目标字符串，正在替换..."
    # 使用检测到的 sed 命令进行替换，根据不同的 sed 使用不同的语法
    if [ "$SED_CMD" = "gsed" ]; then
        gsed -i "s/hasActivated=\"true\"==e\.hasActivated/hasActivated=\"true\"==\"true\"/g" "$JS_FILE"
    else
        sed -i '' "s/hasActivated=\"true\"==e\.hasActivated/hasActivated=\"true\"==\"true\"/g" "$JS_FILE"
    fi
    
    # 验证替换是否成功
    if grep -q 'hasActivated="true"=="true"' "$JS_FILE"; then
        echo "✅ 成功修改文件"
        echo "已将 e.hasActivated 替换为 \"true\""
    else
        echo "❌ 替换可能失败，请手动检查"
        if [ "$SED_CMD" = "sed" ]; then
            echo "💡 建议安装 GNU sed: brew install gnu-sed"
        fi
        exit 1
    fi
elif grep -q 'e\.hasActivated' "$JS_FILE"; then
    echo "找到 e.hasActivated，但格式可能不同"
    echo ""
    echo "如果需要手动替换，请使用以下命令:"
    if [ "$SED_CMD" = "gsed" ]; then
        echo "gsed -i 's/你找到的具体字符串/替换后的字符串/g' \"$JS_FILE\""
    else
        echo "sed -i '' 's/你找到的具体字符串/替换后的字符串/g' \"$JS_FILE\""
    fi
    echo ""
    if [ "$SED_CMD" = "sed" ]; then
        echo "💡 如果上述命令出现问题，建议安装 GNU sed: brew install gnu-sed"
    fi
    exit 1
else
    echo "⚠️  未找到 e.hasActivated 相关内容"
    if grep -q "hasActivated" "$JS_FILE"; then
        echo "找到 hasActivated 相关内容，共 $(grep -c 'hasActivated' "$JS_FILE") 处"
        echo "可能的匹配内容:"
        grep -n 'hasActivated' "$JS_FILE" | head -3
    else
        echo "未找到任何 hasActivated 相关内容"
    fi
    echo ""
    exit 1
fi

echo ""
echo "脚本执行完成!"
echo "处理的文件: $JS_FILE"
echo "使用的 sed 命令: $SED_CMD"
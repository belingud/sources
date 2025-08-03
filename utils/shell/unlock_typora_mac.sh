#!/bin/bash

# 导航到指定目录
TARGET_DIR="/Applications/Typora.app/Contents/Resources/TypeMark/page-dist/static/js/"

echo "正在处理 Typora 许可证文件..."

# 检查是否安装了gsed
if ! command -v gsed &> /dev/null; then
    echo "错误: 未找到 gsed 命令"
    echo "请先安装 GNU sed: brew install gnu-sed"
    exit 1
fi

# 检查目录是否存在
if [ ! -d "$TARGET_DIR" ]; then
    echo "错误: 目录不存在: $TARGET_DIR"
    exit 1
fi

# 切换到目标目录
cd "$TARGET_DIR" || exit 1
echo "已切换到目录: $(pwd)"

# 查找LicenseIndex相关的JS文件
JS_FILE=$(find . -name "*LicenseIndex*.js" -o -name "*Licenselndex*.js" | head -1)

if [ -z "$JS_FILE" ]; then
    echo "错误: 未找到 LicenseIndex 相关的JS文件"
    echo "当前目录中的JS文件:"
    ls -la *.js 2>/dev/null || echo "未找到JS文件"
    exit 1
fi

# 移除前面的 ./
JS_FILE=${JS_FILE#./}
echo "找到文件: $JS_FILE"

# 创建备份
echo "创建备份文件..."
cp "$JS_FILE" "${JS_FILE}.backup.$(date +%Y%m%d_%H%M%S)"

# 搜索并替换
echo "搜索并修改 hasActivated 相关代码..."

# 检查文件中是否包含目标字符串
if grep -q 'hasActivated="true"==e\.hasActivated' "$JS_FILE"; then
    echo "找到目标字符串，正在替换..."
    gsed -i 's/hasActivated="true"==e\.hasActivated/hasActivated="true"=="true"/g' "$JS_FILE"
    echo "✅ 成功修改文件"
    echo "已将 e.hasActivated 替换为 \"true\""
elif grep -q 'e\.hasActivated' "$JS_FILE"; then
    echo "找到 e.hasActivated，但格式可能不同"
    echo "匹配的行数: $(grep -c 'e\.hasActivated' "$JS_FILE")"
    echo ""
    echo "如果需要手动替换，请使用以下命令:"
    echo "gsed -i 's/你找到的具体字符串/替换后的字符串/g' \"$JS_FILE\""
else
    echo "⚠️  未找到 e.hasActivated 相关内容"
    if grep -q "hasActivated" "$JS_FILE"; then
        echo "找到 hasActivated 相关内容，共 $(grep -c 'hasActivated' "$JS_FILE") 处"
    else
        echo "未找到任何 hasActivated 相关内容"
    fi
fi

echo ""
echo "脚本执行完成!"
echo "处理的文件: $JS_FILE"
echo "备份文件已保存，如需还原请查看 *.backup.* 文件"

# 显示所有备份文件
echo ""
echo "当前备份文件:"
ls -la *.backup.* 2>/dev/null || echo "无备份文件"

# macOS NCM转换器

这是一个 [nondance/ncmdump](https://github.com/nondanee/ncmdump "nondance/ncmdump") 的macOS图形界面Fork版本，添加了更好的用户体验和新功能。感谢原作者的付出！

![shield](https://img.shields.io/badge/python-2.7%20%7C%203.4%2B-blue)

## 下载使用

### 下载方式
1. 通过Release下载（推荐）：
   - 访问 [Releases](https://github.com/zenenznze/macos-auto-ncmdump/releases) 页面
   - 下载最新版本的 `NCM转换器-v1.0.0.zip`
   - 解压后将应用拖入Applications文件夹

2. 直接下载源码编译版本：
   - [NCM转换器.app](https://github.com/zenenznze/macos-auto-ncmdump/blob/main/releases/NCM转换器.app)

### 首次使用说明
如果提示"无法打开，因为来源不明"：
- 在访达中右键点击应用 -> 打开 -> 点击"打开"按钮

### 使用方法
1. 启动后：
   - 点击"选择文件"可以选择单个或多个NCM文件
   - 点击"选择文件夹"可以选择包含NCM文件的文件夹
   - 点击"开始转换"开始批量转换
   - 点击"清除列表"可以清空当前选择的文件
2. 程序会记住上次使用的文件夹，方便下次使用

## 功能特点

- 支持批量选择NCM文件或文件夹进行转换
- 图形界面操作，简单易用
- 自动将NCM文件转换为MP3格式
- 转换完成后自动删除原NCM文件
- 自动记住上次使用的文件夹

## 自行编译

### 环境要求
- Python 3.4+ (推荐使用Python 3.12)
- macOS 10.13+

### 依赖安装
```bash
# 安装编译和运行所需依赖
pip install pyinstaller ncmdump
```

### 编译步骤
1. 克隆代码仓库
```bash
git clone https://github.com/zenenznze/macos-auto-ncmdump.git
cd macos-auto-ncmdump
```

2. 编译应用程序
```bash
pyinstaller --windowed --noconfirm --name "NCM转换器" --add-data "Info.plist:." ncm_converter.py
```

编译后的应用程序位于 `dist/NCM转换器.app`

### 权限说明
应用程序需要以下权限：
- 文件访问权限：用于读取NCM文件和保存转换后的MP3文件
- Application Support目录访问权限：用于保存配置文件（保存在 ~/Library/Application Support/NCM转换器/）

如果遇到权限问题：
1. 首次运行时通过"右键 -> 打开"的方式运行
2. 在"系统偏好设置 -> 安全性与隐私 -> 隐私"中授予相应权限

## 其他平台

### Windows版本
访问原项目 [auto-ncmdump](https://github.com/iKunpw/auto-ncmdump) 获取Windows版本。

软件仅供学习交流，请勿用于商业及非法用途，如产生法律纠纷与本人无关。

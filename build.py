import PyInstaller.__main__
import os

# 打包配置
PyInstaller.__main__.run([
    'screenshot_app.py',     # 主程序文件
    '--onefile',             # 打包成单个exe文件
    '--windowed',            # 不显示控制台窗口
    '--icon=icon.ico',       # 设置程序图标
    '--name=ES Screenshot', # 输出文件名
    '--add-data=icon.ico;.', # 包含图标文件
    '--clean'                # 清理临时文件
])

import sys
import os
import time
import platform
from PIL import ImageGrab # type: ignore
import keyboard # type: ignore
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox # type: ignore
from PyQt5.QtGui import QIcon # type: ignore

class ScreenshotTool:
    def __init__(self):
        print("初始化中...")
        
        # 调试信息
        print(f"Python版本: {platform.python_version()}")
        print(f"操作系统: {platform.system()} {platform.release()}")
        print('ESS版本: b0.2')
        self.check_dependencies()
        
        # 创建应用
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # 检查图标文件
        icon_path = self.resource_path("icon.ico")
        print(f"图标路径: {icon_path}")
        if not os.path.exists(icon_path):
            self.show_error("文件缺失", f"无法找到文件: {icon_path}")
            sys.exit(1)
        
        # 初始化托盘图标
        self.init_tray_icon()
        
        # 注册快捷键
        keyboard.add_hotkey('ctrl+alt+o', self.capture_screen)
        
        print("初始化中...")

    def check_dependencies(self):
        """检查所有必要依赖"""
        try:
            from PIL import ImageGrab # type: ignore
            import keyboard # type: ignore
            from PyQt5.QtWidgets import QApplication # type: ignore
            print("所有依赖包已正确安装")
        except ImportError as e:
            self.show_error("依赖缺失", f"缺少必要组件: {str(e)}\n请执行: pip install pillow keyboard pyqt5 pywin32")
            sys.exit(1)

    def init_tray_icon(self):
        """初始化托盘图标"""
        print("初始化中...")
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon(self.resource_path("icon.ico")))
        
        # 创建菜单
        menu = QMenu()
        menu.addAction("截图", self.capture_screen)
        menu.addSeparator()
        menu.addAction("退出", self.quit_app)
        self.tray.setContextMenu(menu)
        
        self.tray.show()
        self.tray.showMessage("ES", "程序已启动至托盘", QSystemTrayIcon.Information, 2000)
        print("启动成功")

    def resource_path(self, relative_path):
        """获取资源绝对路径"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def capture_screen(self):
        """截取屏幕"""
        print("正在截图...")
        try:
            desktop = os.path.join(os.path.expanduser("~"), 'Desktop')
            desktop = desktop.encode('utf-8').decode('gbk')
            filename = os.path.join(desktop, f"screenshot_{time.strftime('%Y%m%d_%H%M%S')}.png")

            ImageGrab.grab().save(filename)
            print(f"截图已保存: {filename}")
            
            self.tray.showMessage("截图成功", f"截图已保存到: {filename}", QSystemTrayIcon.Information, 3000)
        except Exception as e:
            print(f"截图失败: {str(e)}")
            self.show_error("截图失败", str(e))

    def show_error(self, title, message):
        """显示错误信息"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def quit_app(self):
        """退出应用程序"""
        print("退出中...")
        self.tray.hide()
        keyboard.unhook_all_hotkeys()
        self.app.quit()

if __name__ == "__main__":
    print("欢迎使用ESS")
    try:
        app = ScreenshotTool()
        print("进入主事件循环...")
        sys.exit(app.app.exec_())
    except Exception as e:
        print(f"程序崩溃: {str(e)}")
        QMessageBox.critical(None, "错误", f"程序发生致命错误: {str(e)}")
    finally:
        print("程序结束")

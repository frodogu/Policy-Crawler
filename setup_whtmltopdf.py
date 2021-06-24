from pywinauto import application
import time

def setup_pck():
    app = application.Application().start('wkhtmltox-0.12.6-1.msvc2015-win64.exe')
    time.sleep(5)

    window_title = 'wkhtmltox 0.12.6-1 Setup'
    # print(app[window_title].print_control_identifiers())

    app[window_title].child_window(title="I &Agree", class_name="Button").click()
    time.sleep(1)

    # 修改默认安装路径
    app[window_title].child_window(class_name="Edit").set_edit_text(r'C:\Program Files\wkhtmltopdf')


    app[window_title].child_window(title="&Install", class_name="Button").click()
    time.sleep(10)

    app[window_title].child_window(title="&Close", class_name="Button").click()

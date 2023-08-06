"""PyWebIO 的中文版, 提供一系列命令式的交互函数来在浏览器上获取用户输入和进行输出，
将浏览器变成了一个“富文本终端”，可以用于构建简单的 Web 应用或基于浏览器的 GUI 应用。
PyWebIO 还可以方便地整合进现有的 Web 服务，让你不需要编写 HTML 和 JS 代码，
就可以构建出具有良好可用性的应用。
"""

从 pywebio 导入 start_server
从 pywebio.io_ctrl 导入 Output
导入 pywebio

从 汉化通用 导入 _反向注入

def 启动服务器(应用々, 端口=0, 主机='', 调试=假, cdn=真, 静态目录=空, 远程访问=假,
              重连超时=0):
    start_server(applications=应用々, port=端口, host=主机,
                 debug=调试, cdn=cdn, static_dir=静态目录,
                 remote_access=远程访问,
                 reconnect_timeout=重连超时)
                 # allowed_origins=None, check_origin=None,
                 # auto_open_webbrowser=False,
                 # max_payload_size='200M',
                 # **tornado_app_settings)

# 从 . 导入 输入
# 从 . 导入 输出

# 除了要对 utils 应用猴子补丁，还要对其他模块应用，为什么？
套路 __check_dom_name_value(value, name='`name`'):
    无操作

pywebio.utils.check_dom_name_value = __check_dom_name_value
pywebio.input.check_dom_name_value = __check_dom_name_value
pywebio.output.check_dom_name_value = __check_dom_name_value
pywebio.pin.check_dom_name_value = __check_dom_name_value

类 〇输出(Output):
    套路 显示(分身):
        分身.send()
    
    套路 样式(分身, css样式):
        返回 分身.style(css样式)
    
    套路 当点击时(分身, 回调函数):
        返回 分身.onclick(回调函数)

_反向注入(〇输出, Output)

_类型字典 = {
    '文本' : 'text',
    '数字' : 'number',
    '浮点数' : 'float',
    '密码' : 'password',
    # url
    '日期' : 'date',
    '时间' : 'time',
    '颜色' : 'color',
    '本地日期时间' : 'datetime-local',
    # '复选框' : 'checkbox',
    # '单选按钮' : 'radio',
    # '选择框' : 'select',
    # '文本域' : 'textarea',
}

_颜色字典 = {
    '主色' : 'primary',
    '副色' : 'secondary',
    '成功' : 'success',
    '危险' : 'danger',
    '警告' : 'warning',
    '信息' : 'info',
    '浅色' : 'light',
    '深色' : 'dark',
}

套路 _按钮选项翻译(按钮列表):
    按钮类型字典 = {
        '提交' : 'submit',
        '重置' : 'reset',
        '取消' : 'cancel',
    }
    取 i, 按钮 于 枚举(按钮列表):
        如果 是实例(按钮, 字典型):
            如果 '标签' 在 按钮:
                按钮['label'] = 按钮.弹出('标签')
            如果 '值' 在 按钮:
                按钮['value'] = 按钮.弹出('值')
            如果 '禁用' 在 按钮:
                按钮['disabled'] = 按钮.弹出('禁用')
            如果 '类型' 在 按钮:
                按钮类型 = 按钮.弹出('类型')
                按钮['type'] = 按钮类型字典.获取(按钮类型, 按钮类型)
            如果 '颜色' 在 按钮:
                按钮颜色 = 按钮.弹出('颜色')
                按钮['color'] = _颜色字典.获取(按钮颜色, 按钮颜色)
        否则:
            如果 是实例(按钮, 列表型):  # 对于列表, 直接修改
                如果 长(按钮) > 2:
                    按钮[2] = 按钮类型字典.获取(按钮[2], 按钮[2])
            否则:
                如果 是实例(按钮, 元组型):  # 对于元组, 先变成列表
                    按钮 = 列表型(按钮)
                    如果 长(按钮) > 2:
                        按钮[2] = 按钮类型字典.获取(按钮[2], 按钮[2])
                    按钮列表[i] = 按钮   # 这一步很关键

__版本__ = '0.1.170'

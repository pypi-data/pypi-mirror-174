"""
本模块提供了一系列函数来输出不同形式的内容到用户浏览器，并支持灵活的输出控制。

函数清单

标记有 * 的函数表示其支持接收 输出xxx 调用作为参数。
标记有 † 的函数表示其支持作为上下文管理器使用。

函数清单

1. 输出内容的容器 - Scope

输出容器        put_scope       创建一个新的容器
使用容器        use_scope†      进入容器
获取容器        get_scope       获取当前正在使用的容器
清空            clear           清空容器内容
移除            remove          移除容器
滚动到          scroll_to       将页面滚动到容器处

2. 内容输出

输出文本                put_text
输出md                  put_markdown
输出消息                put_info*†
输出成功消息            put_success*†
输出警告消息            put_warning*†
输出错误消息            put_error*†
输出html                put_html
输出链接                put_link
输出进度条              put_processbar
输出加载动画            put_loading†
输出代码                put_code
输出表格                put_table*
输出按钮                put_button
输出按钮々              put_buttons
输出图像                put_image
输出文件                put_file
输出选项卡々            put_tabs*
输出折叠内容            put_collapse*†
输出可滚动内容          put_scrollable*†
输出控件                put_widget*

3. 其他交互

通知                    toast
弹窗                    popup*†
关闭弹窗                close_popup

4. 布局与样式

输出行                  put_row*†
输出列                  put_column*†
输出栅格                put_grid*
跨单元格                span

"""

从 pywebio.output 导入 *
从 . 导入 _颜色字典

类 〇弹窗大小:
    大 = 'large'
    普通 = 'normal'
    小 = 'small'

类 〇位置:
    顶部 = 'top'
    中间 = 'middle'
    底部 = 'bottom'

类 〇输出位置:
    顶部 = 0
    底部 = -1

套路 设置容器(名称, 父容器=空, 位置=〇输出位置.底部, 如存在=空):
    """set_scope
    创建一个新的容器
    """
    返回 set_scope(名称, container_scope=父容器, position=位置, if_exist=如存在)


套路 获取容器(栈索引=-1):
    """get_scope
    获取当前正在使用的容器"""
    返回 get_scope(栈索引)


套路 清空(容器=空):
    """clear
    """
    返回 clear(容器)


套路 移除(容器=空):
    """remove
    """
    返回 remove(容器)


套路 滚动到(容器=空, 位置=〇位置.顶部):
    """scroll_to
    """
    返回 scroll_to(scope=容器, position=位置)


套路 输出文本(*文本々, 分隔符=' ', 行内=假, 容器=空, 位置=〇输出位置.底部):
    """put_text
    输出纯文本"""
    返回 put_text(*文本々, sep=分隔符, inline=行内, scope=容器, position=位置)


套路 输出消息(*内容々, 可关闭=假, 容器=空, 位置=〇输出位置.底部):
    """put_info"""
    返回 put_info(*内容々, closable=可关闭, scope=容器, position=位置)


套路 输出成功消息(*内容々, 可关闭=假, 容器=空, 位置=〇输出位置.底部):
    """put_success"""
    返回 put_success(*内容々, closable=可关闭, scope=容器, position=位置)


套路 输出警告消息(*内容々, 可关闭=假, 容器=空, 位置=〇输出位置.底部):
    """put_warning"""
    返回 put_warning(*内容々, closable=可关闭, scope=容器, position=位置)


套路 输出错误消息(*内容々, 可关闭=假, 容器=空, 位置=〇输出位置.底部):
    """put_error"""
    返回 put_error(*内容々, closable=可关闭, scope=容器, position=位置)


套路 输出html(html, 净化=假, 容器=空, 位置=〇输出位置.底部):
    """put_html"""
    返回 put_html(html, sanitize=净化, scope=容器, position=位置)


套路 输出代码(内容, 语言='', 行数=空, 容器=空, 位置=〇输出位置.底部):
    """put_code"""
    返回 put_code(内容, language=语言, rows=行数, scope=容器, position=位置)


套路 输出md(md内容, 左修剪=真, 选项々=空, 净化=真, 容器=空, 位置=〇输出位置.底部, **关键词参数々):
    """put_markdown"""
    返回 put_markdown(md内容, lstrip=左修剪, options=选项々,
            sanitize=净化, scope=容器, position=位置, **关键词参数々)


套路 跨单元格(内容, 行=1, 列=1):
    """span
    在 '输出表格' 和 '输出栅格' 函数中创建跨行或跨列内容"""
    返回 span(内容, row=行, col=列)


套路 输出表格(数据, 表头=空, 容器=空, 位置=〇输出位置.底部):
    """put_table"""
    返回 put_table(数据, header=表头, scope=容器, position=位置)


套路 输出按钮々(按钮々, 当点击时, 小=空, 链接样式=假, 轮廓=假, 组合=假,
              容器=空, 位置=〇输出位置.底部, **回调选项々):
    """put_buttons
    按钮々: 按钮列表, 列表元素的可用形式如下:
            1. 字典:
                {
                    '标签': 字符串, 按钮标签
                    '值': 对象, 按钮值
                    '颜色': 可选, 字符串, 按钮颜色
                    '禁用': 可选, 布尔值, 是否禁用
                }
            2. 元组或列表: (按钮标签, 按钮值)
            3. 单值, 此时按钮标签和按钮值具有相同的值
        按钮颜色值可以为: '主色', '副色', '成功', '危险', '警告', '信息', '浅色', '深色'
    """
    取 按钮 于 按钮々:
        如果 是实例(按钮, 字典型):
            如果 '标签' 在 按钮:
                按钮['label'] = 按钮.弹出('标签')
            如果 '值' 在 按钮:
                按钮['value'] = 按钮.弹出('值')
            如果 '禁用' 在 按钮:
                按钮['disabled'] = 按钮.弹出('禁用')
            如果 '颜色' 在 按钮:
                按钮颜色 = 按钮.弹出('颜色')
                按钮['color'] = _颜色字典.获取(按钮颜色, 按钮颜色)

    返回 put_buttons(按钮々, 当点击时, small=小, link_style=链接样式,
            outline=轮廓, group=组合, scope=容器, position=位置, **回调选项々)


套路 输出按钮(标签, 当点击时, 颜色=空, 小=空, 链接样式=假, 轮廓=假, 禁用=假,
             容器=空, 位置=〇输出位置.底部):
    """put_button
    颜色选项: '主色', '副色', '成功', '危险', '警告', '信息', '浅色', '深色'
    """
    颜色 = _颜色字典.获取(颜色, 颜色)
    返回 put_button(标签, 当点击时, color=颜色, small=小, link_style=链接样式,
            outline=轮廓, disabled=禁用, scope=容器, position=位置)


套路 输出图像(源, 格式=空, 标题='', 宽度=空, 高度=空, 容器=空,
             位置=〇输出位置.底部):
    """put_image"""
    返回 put_image(源, format=格式, title=标题, width=宽度,
            height=高度, scope= 容器, position=位置)


套路 输出文件(名称, 内容, 标签=空, 容器=空, 位置=〇输出位置.底部):
    """put_file
    输出一个文件下载链接"""
    返回 put_file(名称, 内容, label=标签, scope=容器, position=位置)


套路 输出链接(名称, url=空, 应用=空, 新窗口=假, 容器=空, 位置=〇输出位置.底部):
    """put_link
    输出指向其他网页或 pywebio 应用页面的超链接"""
    返回 put_link(名称, url=url, app=应用, new_window=新窗口,
                 scope=容器, position=位置)


套路 输出进度条(名称, 初始值=0, 标签=空, 自动关闭=假,
               容器=空, 位置=〇输出位置.底部):
    """put_processbar"""
    返回 put_processbar(名称, init=初始值, label=标签, auto_close=自动关闭,
                scope=容器, position=位置)


套路 设置进度条(名称, 值, 标签=空):
    """set_processbar
    设置进度条的进度"""
    返回 set_processbar(名称, 值, label=标签)


套路 输出加载动画(形状='转圈', 颜色='深色', 容器=空, 位置=〇输出位置.底部):
    """put_loading
    形状选项: '转圈', '扩大'
    颜色选项: '主色', '副色', '成功', '危险', '警告', '信息', '浅色', '深色'
    """
    形状字典 = {
        '转圈' : 'border',
        '扩大' : 'grow'
    }
    形状 = 形状字典.获取(形状, 形状)
    颜色 = _颜色字典.获取(颜色, 颜色)
    返回 put_loading(shape=形状, color=颜色, scope=容器, position=位置)


套路 输出折叠内容(标题, 内容=[], 展开=假, 容器=空, 位置=〇输出位置.底部):
    """put_collapse"""
    返回 put_collapse(标题, content=内容, open=展开, scope=容器, position=位置)


套路 输出可滚动内容(内容=[], 高度=400, 保持底部=假, 边框=真, 容器=空,
                  位置=〇输出位置.底部, **关键词参数々):
    """put_scrollable"""
    返回 put_scrollable(content=内容, height=高度, keep_bottom=保持底部,
            border=边框, scope=容器, position=位置, **关键词参数々)


套路 输出选项卡々(选项卡々, 容器=空, 位置=〇输出位置.底部):
    """put_tabs
    选项卡々 - 选项卡列表, 列表元素为字典: {'标题': ..., '内容': ...}
    """
    取 选项卡 于 选项卡々:
        如果 '标题' 在 选项卡:
            选项卡['title'] = 选项卡.弹出('标题')
        如果 '内容' 在 选项卡:
            选项卡['content'] = 选项卡.弹出('内容')
    返回 put_tabs(选项卡々, scope=容器, position=位置)


套路 输出控件(模板, 数据, 容器=空, 位置=〇输出位置.底部):
    """put_widget"""
    返回 put_widget(模板, 数据, scope=容器, position=位置)


套路 输出行(内容=[], 大小=空, 容器=空, 位置=〇输出位置.底部):
    """put_row
    使用行布局输出内容"""
    返回 put_row(content=内容, size=大小, scope=容器, position=位置)


套路 输出列(内容=[], 大小=空, 容器=空, 位置=〇输出位置.底部):
    """put_column
    使用列布局输出内容"""
    返回 put_column(content=内容, size=大小, scope=容器, position=位置)


套路 输出栅格(内容, 单元宽度='自动', 单元高度='自动', 列宽=空, 行高=空,
        方向='行', 容器=空, 位置=〇输出位置.底部):
    """put_grid
    使用栅格布局输出内容
    方向选项: '行', '列'
    """
    如果 单元宽度 == '自动': 单元宽度 = 'auto'
    如果 单元高度 == '自动': 单元高度 = 'auto'
    如果 方向 == '行': 方向 = 'row'
    如果 方向 == '列': 方向 = 'column'
    返回 put_grid(内容, cell_width=单元宽度, cell_height=单元高度,
            cell_widths=列宽, cell_heights=行高, direction=方向,
            scope=容器, position=位置)


套路 输出容器(名称, 内容=[], 容器=空, 位置=〇输出位置.底部):
    """put_scope
    输出一个容器"""
    返回 put_scope(名称, content=内容, scope=容器, position=位置)


# 套路 输出(*内容々):
#     返回 output(*内容々)


# 套路 样式(输出々, css样式):
#     """style
#     自定义输出内容的 css 样式"""
#     返回 style(输出々, css样式)


套路 弹窗(标题, 内容=空, 大小=〇弹窗大小.普通, 隐式关闭=真, 可关闭=真):
    """popup"""
    返回 popup(标题, content=内容, size=大小, implicit_close=隐式关闭,
              closable=可关闭)


套路 关闭弹窗():
    """close_popup"""
    返回 close_popup()


套路 通知(内容, 持续时间=2, 位置='居中', 颜色='信息', 当点击时=空):
    """toast
    显示通知消息
    位置选项: '左', '居中', '右'
    颜色选项: '成功', '错误', '警告', '信息'
    """
    位置字典 = {
        '左' : 'left',
        '居中' : 'center',
        '右' : 'right',
    }
    颜色字典 = {
        '成功' : 'success',
        '错误' : 'error',
        '警告' : 'warn',
        '信息' : 'info',
    }
    位置 = 位置字典.获取(位置, 位置)
    颜色 = 颜色字典.获取(颜色, 颜色)
    返回 toast(内容, duration=持续时间, position=位置, color=颜色, onclick=当点击时)


套路 使用容器(名称=空, 清空=假, **关键词参数々):
    """use_scope"""
    返回 use_scope(name=名称, clear=清空, **关键词参数々)


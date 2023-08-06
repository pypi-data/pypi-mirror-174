""" Параметры, которые можно изменить """
formBackgroundColor= "#3c3f41"      # Цвет фона формы
editorBackgroundColor= "#2b2b2b"    # Цвет фона редактора
fontColor="#9f9f9f"                 # Цвет текста

""" Стили темы """
toolTipStyle = '''QToolTip { 
    background-color: #9ea6ab; 
    color: black; 
    /*border: #8ad4ff solid 1px*/
}'''
listWidgetStyle="""
border: 0px;
"""
scrollBarStyle= """
QScrollBar:vertical {
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130), stop:1 rgb(32, 47, 130));
    min-height: 0px;
}
QScrollBar::add-line:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));
    height: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));
    height: 0 px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}
"""
formStyle = f'''
    background-color:{formBackgroundColor}; 
    color: {fontColor};
'''
editorStyle = f"""
background: {editorBackgroundColor};
color: {fontColor};
padding: 10px;
border-radius: 10px;
/*{scrollBarStyle}*/
"""


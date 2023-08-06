COMMAND_HELP = '''iQWorkBook - система накопления знаний для linux на все случаи жизни.
Синтаксис командной строки:
\tiQWorkBook [ПАРАМЕТР] [ПУТЬ]
\tЗапуск без параметров - открытие программы с полным интерфейсом и всеми возможностями
[ПАРАМЕТР]:
\t-h, --help — вывести экранную справку
\t-r, --read — режим просмотра (только просмотр)
\t-l, --log  — вести полный отладочный лог на экране   
[ПУТЬ]:
\tможет быть только папкой, либо пустой, либо содержащей книгу (*.книга) и ее файлы структуры данных. Если папка пуста - будет запущен мастер новой книги после чего она будет добавлена в перечень книг.
'''
# --- Визард создания книги --------------------------------------------------
PAGE1_TEXT='''
  Вы в одном шаге от того, чтобы начать использовать iQWorkBook - самую удобную 
и понятную систему накопления знаний для Linux!

  Для того, чтобы сделать все правильно - просто введите начальные данные.
'''
PAGE1_TEXT1='''
  Книга «вещественная» — это значит, что в ней можно будет найти записи по 
используемым материалам и инструментам. То есть в ней ведутся записи о 
«материальном» (вещественном) процессе.

  Так, кулинарная книга с рецептами - будет вещественной, поскольку в ней 
нужно будет искать рецепты по используемым материалам (ингредиентам). 
А телефонная книга - нет.
'''

# --- Текстовые глифы --------------------------------------------------------
MENU_SYMBOL             = '≣'
SELECTION_SYMBOL        = "#"
THEME_SYMBOL            = "🌓"
MOVE_SYMBOL             = '⇒'
EDITOR_TAGS_SYMBOL      = '#'
EDITOR_MATERIALS_SYMBOL = '⊂'
EDITOR_TOOLS_SYMBOL     = '⚒'
VIEW_SYMBOL             = '⚫'
ATTACHMENTS_SYMBOL      = '📎'

# --- Темы -------------------------------------------------------------------
DARK_THEME = '''
* { background-color:"#3c3f41";
    color: "#9f9f9f";
    }

QLineEdit {
    background-color:"#353739";
    color: "#9f9f9f";
    border-radius: 6px;
    padding: 3px 4px;
    min-height: 1em;
}

QTextEdit {
    background-color:"#353739";
    color: "#9f9f9f";
    border-radius: 6px;
    padding: 10px 10px;
}

QTreeView {
    background-color:"#353739";
    color: "#9f9f9f";
    border-radius: 6px;
    padding: 10px 10px;
}

/* Кнопки */
QPushButton {
    border: 1px solid #353739;
    padding: 4px 8px;
    border-radius: 4px;
}

QPushButton:flat,
QPushButton:default {
    border: 1px solid #353739;
    padding: 5px 9px;
}

QPushButton:hover,
QPushButton:flat:hover {
    background: "#353739" /* это выделение при наведении */
}

QPushButton:pressed,
QPushButton:flat:pressed,
QPushButton:checked:pressed,
QPushButton:flat:checked:pressed {
    background: #313335; /*цвет нажатой кнопки*/
}
/* скроллбары */
QScrollBar {
    background: #353739;
}
QScrollBar:horizontal {
    height: 5px;
}
QScrollBar:vertical {
    width: 5px;
}

QScrollBar::handle {
    background: #3c3f41;        /*цвет ползунка*/
    border-radius: 2px
}

QScrollBar::handle:hover {
    background: #727373;        /*цвет при наведении*/
    border-radius: 2px
}

QScrollBar::sub-line,
QScrollBar::add-line {          /*это кнопки - уменьшающая и увеличивающая*/
    background: transparent;
}

'''

LIGHT_THEME = '''
* {
    background-color:#dddddd;
}

QLineEdit {
    background-color:white;
    border-radius: 6px;
    padding: 3px 4px;
    min-height: 1em;
}

QTextEdit {
    background-color:white;
    border-radius: 6px;
    padding: 10px 10px;
}

QTreeView {
    background-color:white;
    border-radius: 6px;
    padding: 10px 10px;
}

QPushButton {
    border: 1px solid white;
    padding: 4px 8px;
    border-radius: 4px;
}

QPushButton:flat,
QPushButton:default {
    border: 1px solid white;
    padding: 5px 9px;
}

QPushButton:hover,
QPushButton:flat:hover {
    background: white /* это выделение при наведении */
}
QPushButton:pressed,
QPushButton:flat:pressed,
QPushButton:checked:pressed,
QPushButton:flat:checked:pressed {
    background: #cfcfcf; /* цвет нажатой кнопки */
}
/* скроллбары */
QScrollBar {
    background: white;
}
QScrollBar:horizontal {
    height: 5px;
}
QScrollBar:vertical {
    width: 5px;
}

QScrollBar::handle {
    background: #dddddd;        /*цвет ползунка*/
    border-radius: 2px
}

QScrollBar::handle:hover {
    background: #727373;        /*цвет при наведении*/
    border-radius: 2px
}

QScrollBar::sub-line,
QScrollBar::add-line {          /*это кнопки - уменьшающая и увеличивающая*/
    background: transparent;
}
'''

# --- Web справка и «о программе» --------------------------------------------
WEB_HELP = 'https://iqworkbook.gitflic.space/'
ABOUTE = '''<center><h1>iQWorkBook</h1></center>
<p>Эта программа написана группой энтузиастов</p>
<center><h3>iQStudio</h3></center>
<center><p>Руководитель команды — Хильченко А.Н.,<br>г. Биробиджан, 2022.</p></center>
<center><p>Подробности в <a href="https://iqnotes.gitflic.space/">«Книге проекта»</a></p></center>
'''

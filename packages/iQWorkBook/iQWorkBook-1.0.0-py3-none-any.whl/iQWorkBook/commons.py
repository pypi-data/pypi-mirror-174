import json
import logging
import os
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QFileSystemModel, QFileIconProvider, QStyledItemDelegate, QMessageBox

from iQWorkBook.actions import getImage


class Settings:
    # вычисление путей
    __homeDir = str(Path.home())
    __configDir = f"{__homeDir}/.config"
    __configProgrammDir = f"{__configDir}/iQWorkBook"
    __dataDir = f"{__configProgrammDir}/iQWorkBook data"
    __iniPath = f"{__configProgrammDir}/.rc"
    # инициализация переменных
    __w_splitter = [27, 200, 1600]  # состояние сплиттера
    __w_isMaximized = False  # развернутость
    __w_isFullScreen = False  # на весь экран
    __theme_button_checked = False  # состояние кнопки тем
    __lasl_book_path = ''  # путь к последней неглавной книге
    __books = []  # список книг
    __last_rec: str = ''  # путь к последней записи главной книги
    # справочник для подготовки данных
    __settings = dict()

    def __init__(self, parent):
        self.parent = parent
        if Path(self.__iniPath).exists():
            self.load()
            self.check_books()
        else:
            dir = Path(self.__dataDir)
            dir.mkdir(parents=True, exist_ok=True)
            rcFile = Path(self.__iniPath)
            rcFile.touch(mode=0o666, exist_ok=True)
            self.save();
            logging.debug('Первый запуск программы')

    def save(self):
        ''' сохранение настроек '''
        self.__settings['theme'] = self.__theme_button_checked
        self.__settings['maximized'] = self.__w_isMaximized
        self.__settings['fullScreen'] = self.__w_isFullScreen
        self.__settings['lastBook'] = self.__lasl_book_path
        self.__settings['books'] = self.__books
        self.__settings['lastRec'] = self.__last_rec
        self.__settings['splitter'] = self.__w_splitter
        with open(self.__iniPath, "w") as write_file:
            json.dump(self.__settings, write_file)
        logging.debug(' настройки сохранены')

    def load(self):
        ''' загрузка настроек '''
        with open(self.__iniPath, "r") as read_file:
            self.__settings = json.load(read_file)
            self.__theme_button_checked = self.__settings['theme']
            self.__w_isMaximized = self.__settings['maximized']
            self.__w_isFullScreen = self.__settings['fullScreen']
            self.__w_splitter = self.__settings['splitter']
            self.__lasl_book_path = self.__settings['lastBook']
            self.__books = self.__settings['books']
            self.__last_rec = self.__settings['lastRec']
        logging.debug(' настройки загружены')

    def check_books(self):
        '''
        проверка существования путей к книгам, если путь существует,
        то и книга есть…
        '''
        res = []
        for i in self.__books:
            if Path(i).exists(): res += [i]
        self.__books = res
        logging.debug(' перечень доступных книг проверен и зачищен')

    # геттеры
    def get_splitter_config(self):
        return self.__w_splitter

    def get_window_fullscreen(self):
        return self.__w_isFullScreen

    def get_window_maximized(self):
        return self.__w_isMaximized

    def get_theme_button_checked(self):
        return self.__theme_button_checked

    def get_last_book_path(self):
        return self.__lasl_book_path

    def get_last_rec(self):
        return self.__last_rec

    def get_books(self):
        return self.__books

    def get_data_dir(self):
        """ возвращает путь до главной книги
        (той, что открывается по-умолчанию)
        """
        return self.__dataDir

    # сеттеры
    def set_splitter_config(self, value):
        self.__w_splitter = value

    def set_window_fullscreen(self, value):
        self.__w_isFullScreen = value

    def set_window_maximized(self, value):
        self.__w_isMaximized = value

    def set_theme_button_checked(self, value):
        self.__theme_button_checked = value

    def set_last_book_path(self, value):
        self.__lasl_book_path = value

    def set_last_rec(self, value):
        self.__last_rec = value

class Document:
    __path = ''
    __parent = None

    def __init__(self, filePath, parent):
        self.__path = filePath  # путь к файлу
        self.__parent = parent  # класс книги
        logging.debug(f'создан документ по пути {self.__path}')

    def saveToFile(self, editor):
        ''' сохранение в файл '''
        with open(self.__path, 'w') as file:
            file.write(editor.toHtml())
        logging.debug('Документ сохранен')

    def loadFromFile(self, editor):
        ''' чтение из файла '''
        with open(self.__path, 'r') as file:
            editor.setHtml(file.read())
        logging.debug('Документ прочитан')

class DataSet:
    " книга "
    __file = ''
    __folder = ''
    __book_name = ''
    __materialBook = False
    __tags = []
    __materials = []
    __tools = []
    __group_template = ''
    __record_template = ''

    def __init__(self, **kwargs):
        if 'filename' in kwargs: self.__file = kwargs["filename"]
        if 'datadir' in kwargs: self.__folder = kwargs["datadir"]
        if self.__file == '':
            self.createDataSet()
            logging.info('создаем датасет')
        else:
            logging.info('читаем датасет')
            self.load()

    def __str__(self):
        return f"\tПуть: {self.__file}\n" \
               f"\tНазвание:{self.__book_name}\n" \
               f"\tПризнак:{self.__materialBook}\n" \
               f"\tТэги:{self.__tags}\n" \
               f"\tМатериалы:{self.__materials}\n" \
               f"\tИнструменты:{self.__tools}\n" \
               f"\tЗаготовка группы:{self.__group_template}\n" \
               f"\tЗаготовка записи:{self.__record_template}\n"\

    def createDataSet(self):
        logging.info(
            f"Первый запуск программы по пути, запуск мастера создания книги")

        self.__book_name = Path(self.__folder).parts[-1]
        self.__materialBook = False
        self.__file = f"{self.__folder}/.iQWorkBook"
        exec_book_CMD = Path(self.__folder) / Path(self.__book_name + '.desktop')
        #создадим desktop файл
        text = f'[Desktop Entry]\n'\
               f'Type=Application\n'\
               f'Name[ru]=iQWorkBook: {self.__book_name}\n'\
               f'Icon=iQWorkBook\n'\
               f'Exec= iQWorkBook "{str(Path(self.__folder))}"\n'
        exec_book_CMD.write_text(text)
        self.save()
        mess = f'Создана <strong>новая</strong> книга записей и применены настройки по-умолчанию!\n' \
                '<br>' \
               f'Изменить их можно в <strong>«Основное меню»→«Настройки книги»</strong>\n' \
                '<br>' \
               f'Настроенный значок для открытия книги в программе находится в корневом каталоге книги:\n' \
               f'<strong>{str(Path(self.__folder))}</strong>'
        QMessageBox.about(None,
                         'iQWorkBook: Сообщение',
                         mess
                          )



    def get_group_template(self):
        return self.__group_template

    def set_group_template(self,value):
        self.__group_template = value

    def get_record_template(self):
        return self.__record_template

    def set_record_template(self,value):
        self.__record_template = value

    def get_name(self):
        return self.__book_name

    def set_name(self, value):
        self.__book_name = value

    def get_materials(self):
        return self.__materials

    def get_tools(self):
        return self.__tools

    def set_materials(self, value):
        self.__materials = value

    def set_tools(self, value):
        self.__tools = value

    def get_path(self):
        return self.__path

    def get_tags(self):
        return self.__tags

    def set_tags(self, value):
        self.__tags = value

    def get_material_status(self):
        return self.__materialBook

    def set_material_status(self, value):
        self.__materialBook = value

    def save(self):
        ''' сохранение файла настроек книги'''
        settings = {}
        settings['name'] = self.__book_name
        settings['material_book'] = self.__materialBook
        settings['tags'] = self.__tags
        settings['tools'] = self.__tools
        settings['materials'] = self.__materials
        settings['group_template'] = self.__group_template
        settings['record_template'] = self.__record_template
        with open(self.__file, 'w') as file:
            json.dump(settings, file, indent=2, ensure_ascii='utf-8')
        logging.debug('Источник данных сохранен')

    def load(self):
        ''' чтение файла настроек книги'''
        with open(self.__file, 'r') as file:
            settings = json.load(file)
            self.__book_name = settings['name']
            self.__materialBook = settings['material_book']
            self.__tags = settings['tags']
            self.__tools = settings['tools']
            self.__materials = settings['materials']
            self.__group_template  = settings['group_template']
            self.__record_template  = settings['record_template']
        logging.debug('Источник данных прочитан')

# --- МОДЕЛИ -----------------------------------------------------------------
class ModelLine(QStandardItemModel):
    __folder = ''
    __selection = ''
    __tags = []
    __materials = []
    __tools = []
    __text  = ''

    def __init__(self, parent = None, **kwargs):
        super().__init__(parent)
        if 'folder' in kwargs:
            self.__folder = kwargs['folder']
            self.update_model()

    def update_model(self):
        def check_selection(name):
            return True if (self.__selection.lower() in name.lower()) else False

        def check_tag(text): # ищем один из списка
            if self.__tags==[]: return True
            for e in self.__tags:
                if e.lower() in text: return True
            return False

        def check_tool(text): # ищем один из списка
            if self.__tools==[]: return True
            for e in self.__tools:
                if e.lower() in text: return True
            return False

        def check_materials(text): # ищем один из списка
            if self.__materials==[]: return True
            for e in self.__materials:
                if e.lower() in text: return True
            return False

        def check_text(text):   # полное соответсвие вхождению
            if self.__text=='': return True
            if self.__text.lower() in text: return True
            return False

        self.clear()
        for curren_dir,dirs,files in os.walk(self.__folder):
            for f in files:
                path = Path(curren_dir)/Path(f)
                if path.suffix!='.html': continue
                name = path.stem
                if name[0]=='.': continue
                if check_selection(name):
                    if self.__tags != [] or self.__materials != [] or self.__tools != [] or self.__text != '':
                        text = path.read_text().lower()
                        if check_tag(text):
                            if check_materials(text):
                                if check_tool(text):
                                    if check_text(text):
                                        item = QStandardItem(name)
                                        item.path = path
                                        self.appendRow(item)
                    else:
                        item = QStandardItem(name)
                        item.path = path
                        self.appendRow(item)
        self.sort(0,Qt.AscendingOrder)
        logging.info('модель перестроена')

    def setFolder(self, bookPath):
        self.__folder = bookPath

    def set_selection(self, text):
        self.__selection = text
        self.update_model()

    def set_find_options(self, options):
        self.__tags = options['tags']
        self.__materials = options['materials']
        self.__tools = options['tools']
        self.__text = options['text']
        logging.info(f'параметры поиска:\n{options}')
        self.update_model()


class ModelTree(QFileSystemModel):
    __folder = ''

    def __init__(self, parent=None, **kwargs):
        class IconProvider(QFileIconProvider):
            def icon(self, fileInfo):
                if fileInfo.isDir():
                    return getImage('папка')
                if fileInfo.isFile():
                    return getImage('запись')

                return QFileIconProvider.icon(self, fileInfo)

        super().__init__(parent)
        if 'folder' in kwargs:
            self.__folder = kwargs['folder']
            self.setRootPath(self.__folder)
        self.setNameFilters(['*.html'])
        self.setNameFilterDisables(False)
        self.setIconProvider(IconProvider())

    def setFolder(self, bookPath):
        self.__folder = bookPath
        self.setRootPath(self.__folder)

    def getRootIndex(self):
        return self.index(self.__folder)

    def set_selection(self, text):
        self.setNameFilters([f'*{text}*.html'])

class NameDelegate(QStyledItemDelegate):

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if isinstance(index.model(), QFileSystemModel):
            if not index.model().isDir(index):
                option.text = index.model().fileInfo(index).baseName()

    def setEditorData(self, editor, index):
        if isinstance(index.model(), QFileSystemModel):
            if not index.model().isDir(index):
                editor.setText(index.model().fileInfo(index).baseName())
            else:
                super().setEditorData(editor, index)

import logging
import sys
from pathlib import Path

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolButton, QLabel, QLineEdit, \
    QPushButton, QTreeView, QHBoxLayout, QSpacerItem, QSizePolicy, QDialog, QFileSystemModel, QAbstractItemView, \
    QFileIconProvider, QMessageBox, QApplication
from iqEditors import iQNoteEditor

from iQWorkBook.actions import getImage
from iQWorkBook.commons import NameDelegate
from iQWorkBook.constants import SELECTION_SYMBOL, MENU_SYMBOL, \
    THEME_SYMBOL, VIEW_SYMBOL, ATTACHMENTS_SYMBOL


class ToolPanel(QWidget):
    """ панель инструментов """

    def __init__(self, parent=None):
        super().__init__(parent)
        # компоновка
        self.layer = QVBoxLayout(self)
        self.menuButton = QToolButton(self)
        self.themeButton = QToolButton(self)
        self.findButton = QToolButton(self)
        self.attachmentsButton = QToolButton(self)
        spacerItem = QtWidgets.QSpacerItem(20, 20,
                                           QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        self.layer.addWidget(self.menuButton)
        self.layer.addWidget(self.findButton)
        self.layer.addWidget(self.attachmentsButton)
        self.layer.addItem(spacerItem)
        self.layer.addWidget(self.themeButton)
        self.layer.setContentsMargins(0, 0, 0, 0)
        # настройки внешнего вида
        self.themeButton.setText(THEME_SYMBOL)
        self.menuButton.setText(MENU_SYMBOL)
        self.menuButton.setAutoRaise(True)
        self.themeButton.setAutoRaise(True)
        self.themeButton.setCheckable(True)
        self.menuButton.setMaximumSize(QtCore.QSize(27, 22))
        self.themeButton.setMaximumSize(QtCore.QSize(27, 22))
        self.findButton.setText(SELECTION_SYMBOL)
        self.findButton.setAutoRaise(True)
        self.findButton.setCheckable(True)
        self.findButton.setMaximumSize(QtCore.QSize(27, 22))
        self.attachmentsButton.setAutoRaise(True)
        self.attachmentsButton.setCheckable(True)
        self.attachmentsButton.setMaximumSize(QtCore.QSize(27, 22))
        self.attachmentsButton.setText(ATTACHMENTS_SYMBOL)
        self.menuButton.setToolTip('Вызов меню приложения')
        self.themeButton.setToolTip('Переключить визуальную тему приложения')
        self.findButton.setToolTip('Перейтив режим поиска с условиями')
        self.attachmentsButton.setToolTip('Показать браузер вложений')

        logging.debug('панель инструментов создана')

    def updateGUI(self, settings): pass


class HorToolPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layer = QHBoxLayout(self)
        self.layer.setContentsMargins(0, 0, 0, 0)
        self.layer.setSpacing(2)
        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.viewButton = QToolButton(self)
        self.viewButton.setText(VIEW_SYMBOL)
        self.viewButton.setAutoRaise(True)
        self.viewButton.setMaximumSize(QtCore.QSize(27, 22))
        self.viewButton.setCheckable(True)
        self.viewButton.setToolTip('Переключить режим отображения дерева записей')
        self.findButton = QToolButton(self)
        self.findButton.setText(SELECTION_SYMBOL)
        self.findButton.setAutoRaise(True)
        self.findButton.setMaximumSize(QtCore.QSize(27, 22))
        self.findButton.setCheckable(True)
        self.findButton.setToolTip('Развернуть (свернуть) панель поиска')
        # self.specialButton = QToolButton(self)
        # self.specialButton.setText(MOVE_SYMBOL)
        # self.specialButton.setAutoRaise(True)
        # self.specialButton.setMaximumSize(QtCore.QSize(27, 22))
        # self.specialButton.setToolTip('Показать отобранное в редакторе')
        self.layer.addWidget(self.viewButton)
        self.layer.addItem(spacer)
        self.layer.addWidget(self.findButton)
        # self.layer.addWidget(self.specialButton)


class FindPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layer = QVBoxLayout(self)
        self.layer.setContentsMargins(0, 0, 0, 0)
        self.layer.setSpacing(2)
        self.tagLabel = QLabel('Поиск по тэгу:')
        self.tagEdit = QLineEdit(self)
        self.tagEdit.setToolTip('Отбор по тэгу')
        self.materialLabel = QLabel('Поиск по материалу:')
        self.materialEdit = QLineEdit(self)
        self.toolsLabel = QLabel('Поиск по инструменту:')
        self.toolsEdit = QLineEdit(self)
        self.findLabel = QLabel('Поиск по вхождению:')
        self.findEdit = QLineEdit(self)
        self.findButton = QPushButton('Найти')
        self.findButton.setFlat(True)
        self.layer.addWidget(self.tagLabel)
        self.layer.addWidget(self.tagEdit)
        self.layer.addWidget(self.materialLabel)
        self.layer.addWidget(self.materialEdit)
        self.layer.addWidget(self.toolsLabel)
        self.layer.addWidget(self.toolsEdit)
        self.layer.addWidget(self.findLabel)
        self.layer.addWidget(self.findEdit)
        self.layer.addWidget(self.findButton)
        # Использование материалов
        self.__useMaterials = True  # по умолчанию не используются
        self.materialEdit.setVisible(False)
        self.materialLabel.setVisible(False)
        self.toolsEdit.setVisible(False)
        self.toolsLabel.setVisible(False)
        # внешний вид
        self.findTrigger(False)
        logging.debug("Панель поиска создана")

    def set_use_materials(self, value):
        self.__useMaterials = value

    def clearAll(self):
        '''очистка запросов поиска'''
        self.findEdit.setText('')
        self.tagEdit.setText('')
        self.materialEdit.setText('')
        self.toolsEdit.setText('')
        # todo отменить поиск и перезаполнить модель!
        logging.debug('Поиск очищен')

    def findTrigger(self, value):
        self.tagLabel.setVisible(value)
        self.tagEdit.setVisible(value)
        if self.__useMaterials:
            self.materialLabel.setVisible(value)
            self.materialEdit.setVisible(value)
            self.toolsLabel.setVisible(value)
            self.toolsEdit.setVisible(value)
        self.findLabel.setVisible(value)
        self.findEdit.setVisible(value)
        self.findButton.setVisible(value)
        if not value: self.clearAll()
        logging.debug(f'триггер панели поиска переключен на {value}')

    def isShowed(self):
        return self.findButton.isVisible()


class SidePanel(QWidget):
    """ боковая панель """

    def __init__(self, parent=None):
        super().__init__(parent)
        # компоновка
        self.layer = QVBoxLayout(self)
        self.layer.setContentsMargins(2, 0, 2, 0)
        self.layer.setSpacing(4)
        self.selectionEdit = QLineEdit(self)
        self.selectionEdit.setToolTip('Отобрать по названию или его части')
        self.findPanel = FindPanel(self)
        self.treeView = QTreeView(self)
        self.specialButton = QPushButton('Основная книга')
        # Пока скрою - попробую без нее, но удалять не буду
        self.layer.addWidget(self.selectionEdit)
        self.layer.addWidget(self.treeView)
        self.layer.addWidget(self.findPanel)

        logging.debug('Боковая панель создана')

# --- Браузер вложений ------------------------------------------------------
class Attachments(QTreeView):
    """ Браузер вложений """
    __model = QFileSystemModel()
    __folder = None
    __book_folder = ''
    __readOnly = False

    def __init__(self, parent=None, **kwargs):
        class IconProvider(QFileIconProvider):
            def icon(self, fileInfo):
                if fileInfo.isDir():
                    return getImage('папка')
                return QFileIconProvider.icon(self, fileInfo)

        super().__init__(parent)
        self.doubleClicked.connect(self.__itemClick)
        self.setModel(self.__model)
        self.__model.setIconProvider(IconProvider())
        self.setHeaderHidden(True)
        self.setRootIsDecorated(True)
        self.setItemsExpandable(True)
        self.setExpandsOnDoubleClick(True)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setIndentation(15)  # отступ у дочерних
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)
        self.setItemDelegate(NameDelegate())  # убрал расширения
        self.__updateFolder()

    def dragEnterEvent(self, e: QtGui.QDragEnterEvent) -> None:
        if not self.__readOnly:
            mime = e.mimeData()
            if mime.hasUrls():
                e.acceptProposedAction()

    def dropEvent(self, e: QtGui.QDropEvent) -> None:
        try:
            import shutil
            for url in e.mimeData().urls():
                file_name = url.toLocalFile()
                in_path = Path(file_name)
                name = in_path.name
                dest_path = Path(self.__model.filePath(self.rootIndex())) / Path(name)
                shutil.copyfile(in_path, dest_path)
            return super().dropEvent(e)
        except:
            QMessageBox.about(self, "Ошибка!", "Ошибка копирования файла неизвестной природы")

    def __updateFolder(self):
        if self.__folder == None:
            self.__model.setRootPath(str(self.__book_folder))
            self.setRootIndex(self.__model.index(str(self.__book_folder)))
        else:
            self.__model.setRootPath(str(self.__folder))
            self.setRootIndex(self.__model.index(str(self.__folder)))

    def __itemClick(self):
        import subprocess
        itemTree = self.currentIndex()
        path = Path(self.__model.filePath(itemTree))
        subprocess.Popen(['xdg-open', path])

    def setBookFolder(self, path):
        '''
        установка корневого каталога книги
        :param path: каталог
        :return: ничто
        '''
        path = path / Path('.Вложения')
        logging.debug(f'Установлен каталог вложений: {path}')
        if not path.exists():
            # создадим каталог вложений - даже если он потом будет висеть
            # пустым, пусть будет
            path.mkdir(parents=True, exist_ok=True)
        self.__book_folder = path
        self.__updateFolder()

    def setRootFolder(self, path=None):
        """
        Установить текущий каталог отображения вложений. Если передан none
        то сброс каталога и очистка содержимого
        :param path: путь к каталогу вложений текущей записи
        :return: ничто
        """
        if path is None:
            path = self.__book_folder
        else:
            path = path / Path('.Вложения')
        logging.debug(f'Установлен каталог вложений: {path}')
        if not path.exists():
            # создадим каталог вложений - даже если он потом будет висеть
            # пустым, пусть будет
            path.mkdir(parents=True, exist_ok=True)
        self.__folder = path
        self.__updateFolder()

    def setReadOnly(self,value):
        self.__readOnly = value


class BookSettingsDialog(QDialog):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.dataset = kwargs['data']
        materialBook = self.dataset.get_material_status()
        Dialog = self
        Dialog.resize(680, 488)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tab_1 = QtWidgets.QWidget()
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_1)
        self.label = QtWidgets.QLabel(self.tab_1)
        self.verticalLayout_7.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.tab_1)
        self.chackBox = QtWidgets.QCheckBox('Эта книга является вещественной', self.tab_1)
        self.verticalLayout_7.addWidget(self.lineEdit)
        self.verticalLayout_7.addWidget(self.chackBox)
        self.label_3 = QtWidgets.QLabel(self.tab_1)
        self.verticalLayout_7.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.tab_1)
        self.label_4.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.label_4.setWordWrap(True)
        self.verticalLayout_7.addWidget(self.label_4)
        spacerItem = QtWidgets.QSpacerItem(20, 147, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem)
        self.tabWidget.addTab(self.tab_1, "Главная")
        self.tab_2 = QtWidgets.QWidget()
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_2)
        self.tagEdit = QtWidgets.QTextEdit(self.tab_2)
        self.verticalLayout_6.addWidget(self.tagEdit)
        self.tabWidget.addTab(self.tab_2, "Тэги")
        self.tab_3 = QtWidgets.QWidget()
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_3)
        self.materialEdit = QtWidgets.QTextEdit(self.tab_3)
        self.verticalLayout_5.addWidget(self.materialEdit)
        self.tab_4 = QtWidgets.QWidget()
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_4)
        self.toolEdit = QtWidgets.QTextEdit(self.tab_4)
        self.verticalLayout_4.addWidget(self.toolEdit)
        if materialBook:
            self.tabWidget.addTab(self.tab_3, "Материалы")
            self.tabWidget.addTab(self.tab_4, "Инструменты")
        self.tab_5 = QtWidgets.QWidget()
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_5)
        self.recordTemplateEdit = iQNoteEditor(self.tab_5)
        self.verticalLayout_2.addWidget(self.recordTemplateEdit)
        self.tabWidget.addTab(self.tab_5, "Шаблон записи")
        self.tab_6 = QtWidgets.QWidget()
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_6)
        self.groupTemplateEdit = iQNoteEditor(self.tab_6)
        self.verticalLayout_3.addWidget(self.groupTemplateEdit)
        self.tabWidget.addTab(self.tab_6, "Шаблон группы")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)

        # внешний вид
        self.tabWidget.setCurrentIndex(0)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Параметры книги")
        self.label.setText("Название книги:")
        self.label_3.setText(" ")
        self.label_4.setText(
            "<html><head/><body><p>Признак вещественности определяет возможность поиска записей по критериям «материал» и «инструмент».</p><p>Так, книга записей о кулинарных рецептах или составе клеев — будет вещественной, а телефонный справочник - нет</p></body></html>")
        # Заглушка для будущей модернизации (подсветка в тексте тегов, материалов, инструментов — потом когда-то,
        # в планах было, но не сразу)
        self.tabWidget.setTabVisible(1, False)
        if materialBook:
            self.tabWidget.setTabVisible(2, False)
            self.tabWidget.setTabVisible(3, False)


        # загрузка данных
        self.lineEdit.setText(self.dataset.get_name())
        self.path = Path(kwargs['path'])
        logging.info(f' - материальный статус: {materialBook}')
        self.tagEdit.setPlainText("\n".join(self.dataset.get_tags()))
        self.materialEdit.setPlainText("\n".join(self.dataset.get_materials()))
        self.toolEdit.setPlainText("\n".join(self.dataset.get_tools()))
        self.groupTemplateEdit.setHtml(self.dataset.get_group_template())
        self.recordTemplateEdit.setHtml(self.dataset.get_record_template())
        self.chackBox.setChecked(self.dataset.get_material_status())

        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)

    def accepted(self):
        self.accept()
        self.result = {
            'name': self.lineEdit.text(),
            'tags': self.tagEdit.toPlainText().split(),
            'materials': self.materialEdit.toPlainText().split(),
            'tools': self.toolEdit.toPlainText().split(),
            'group_template': self.groupTemplateEdit.toHtml(),
            'record_template': self.recordTemplateEdit.toHtml(),
            'material_status': self.chackBox.isChecked(),
        }
        self.hide()

    def rejected(self):
        self.reject()
        self.hide()


class Editor(iQNoteEditor):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)

    def canInsertFromMimeData(self, source: QtCore.QMimeData) -> bool:
        if source.hasUrls():
            return True
        if source.hasHtml():
            return True
        if source.hasText():
            return True
        if source.hasImage():
            return True

    def insertFromMimeData(self, source: QtCore.QMimeData) -> None:
        try:
            import shutil
            import base64
            if source.hasUrls():
                res = QMessageBox.question(self,
                                           'iQWorkBook: запрос',
                                           'Буфер обмена содержит один или несколько файлов, вставить их как вложение и скопировать в книгу?',
                                           QMessageBox.Yes | QMessageBox.No)
                if res == QMessageBox.Yes:
                    for url in source.urls():
                        file_name = url.toLocalFile()
                        in_path = Path(file_name)
                        name = in_path.name
                        dest_path = Path(self.filename).parent / Path(".Вложения") / Path(name)
                        if dest_path.exists():
                            # спросить
                            res = QMessageBox.question(self,
                                                       'iQWorkBook: запрос',
                                                       f'Файл {name} существует! Заменить его?',
                                                       QMessageBox.Yes | QMessageBox.No)
                            if res == QMessageBox.Yes:
                                shutil.copyfile(in_path, dest_path)
                        else:
                            shutil.copyfile(in_path, dest_path)
                        cursor = self.textCursor()
                        logging.info(f"{in_path} — {name}")
                        cursor.insertHtml(f'{ATTACHMENTS_SYMBOL}: <a href="{str(dest_path)}">{name}</a>,')
                    return
            if source.hasImage():
                # вставляем картинку в формате base64
                img = source.imageData()
                size = [img.width(), img.height()]
                ba = QtCore.QByteArray()
                buffer = QtCore.QBuffer(ba)
                buffer.open(QtCore.QIODevice.WriteOnly)
                img.save(buffer, 'PNG')
                base64_data = ba.toBase64().data()
                res = base64_data.decode("utf-8")
                if size[0] <= 650:
                    htmltext = f'<center><img src="data:image/png;base64, {res}"></center>'
                else:
                    htmltext = f'<center><img width="650" src="data:image/png;base64, {res}"></center>'
                self.insertHtml(htmltext)
                return
            if source.hasHtml():
                super().insertFromMimeData(source)
                return
            if source.hasText():
                super().insertFromMimeData(source)
                return

        except:
            QMessageBox.about(self, "Ошибка!", "Ошибка вставки объекта или копирования файла неизвестной природы")

    # обработка клика по ссылке
    def mousePressEvent(self, e):
        super().mousePressEvent(e)  # выполнились действия в родителе (стандарт)
        # дообработка клика по ссылке
        self.anchor = self.anchorAt(e.pos())
        if self.anchor:
            QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent) -> None:
        # дообработка клика по ссылке
        if self.anchor:
            import subprocess
            link = self.anchor
            st_link = str(self.anchor)
            logging.info(st_link)
            subprocess.Popen(['xdg-open',link])
            self.anchor = None

    def mouseReleaseEvent(self, e): pass


if __name__ == "__main__":
    """тест создания виджетов"""
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s:  %(message)s'
                        )
    app = QtWidgets.QApplication(sys.argv)
    w3 = BookSettingsDialog()
    w3.show()
    app.exec_()

import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from UI.UI import Ui_MainWindow
from UI.addEditCoffeeForm import Ui_MainWindow as UI_2


class Form(UI_2, QMainWindow):
    def __init__(self, item=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.item = item
        self.bd = sqlite3.connect("Data/esspresso.sqlite")
        self.pushButton.clicked.connect(self.check_and_send)
        self.parent = parent
        if item is not None:
            self.title.setText(item[1])
            self.fire.setText(str(item[2]))
            self.drubling.setText(item[3])
            self.decribtion.setText(item[4])
            self.cost.setText(str(item[5]))
            self.liquid.setText(str(item[6]))

    def check_and_send(self):
        try:
            if self.item is not None:
                self.bd.cursor().execute(
                    f"""UPDATE esspreso
                    SET title = '{self.item[1]}', fire_category = {self.item[2]}, 
                        druuble_in_cheaps = '{self.item[3]}', discribtion = '{self.item[4]}',
                        cost = {self.item[5]}, liquid = {self.item[6]}
                    WHERE id = {self.item[0]}""")
            else:
                self.bd.cursor().execute(f"""INSERT INTO esspreso(title, fire_category, 
                                                                druuble_in_cheaps, 
                                                                discribtion, cost, liquid)
                                             VALUES {(self.title.text(), self.fire.text(),
                                                      self.drubling.text(), self.decribtion.text(),
                                                      self.cost.text(), self.liquid.text())}""")
            self.bd.commit()
            self.parent.update()
            self.close()
        except Exception as e:
            self.error_place.setText(str(e))


class TextBrowserSample(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.do_paint = False
        self.con = sqlite3.connect("Data/esspresso.sqlite")
        self.add_btn.clicked.connect(self.add_new_item)
        self.edit_btn.clicked.connect(self.edit_item)
        self.update()

    def update(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM esspreso").fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        titles = [description[0] for description in cur.description]
        self.tableWidget.setHorizontalHeaderLabels(titles)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def add_new_item(self):
        form = Form(parent=self)
        form.show()

    def edit_item(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        cur = self.con.cursor()
        result = cur.execute(f"SELECT * FROM esspreso WHERE id = {int(ids[0])}").fetchone()
        print(result)
        form = Form(parent=self, item=result)
        form.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextBrowserSample()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

import psycopg2
import sys
import datetime


from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox,
                             QAbstractButton, QButtonGroup)


def week():
    now_week = datetime.date.today().isocalendar().week
    if now_week % 2 == 0:
        return 'bottom'
    if now_week % 2 == 1:
        return 'top'


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()
        self.days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
        self.day_shorts = {i: j for i, j in zip(self.days, range(len(self.days)))}
        self.day_shorts_ = {i: j for i, j in zip(range(len(self.days)), self.days)}
        self.join_btns = []

        self.setWindowTitle("Shedule")

        self.tabs = QTabWidget(self)
        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.tabs)

        self._create_shedule_tab()
        self._create_subjects_tab()
        self._create_teacher_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="timetable",
                                     user="postgres",
                                     password="1073",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_subjects_tab(self):
        self.subjects_tab = Tabs("Subjects", 1, ["Subjects"], [self.tabs, self.vbox])

        self.cursor.execute(
            "SELECT * FROM timetable.subjects")
        records = self.cursor.fetchall()

        self.subjects_tab.table.setRowCount(len(records))
        for i, r in enumerate(records):
            r = list(r)
            self.subjects_tab.table.setItem(i, 0, QTableWidgetItem(str(r[0])))

        self.subjects_tab.show_tab()
        self.subjects_tab.upd_btn.clicked.connect(lambda: self._update_shedule())

    def _create_teacher_tab(self):
        self.teachers_tab = Tabs("Teachers", 2, ["Full Name", 'Subject'], [self.tabs, self.vbox])

        self.cursor.execute(
            "SELECT * FROM timetable.teachers")
        records = self.cursor.fetchall()

        self.teachers_tab.table.setRowCount(len(records))
        for i, r in enumerate(records):
            r = list(r)
            self.teachers_tab.table.setItem(i, 0, QTableWidgetItem(str(r[1])))
            self.teachers_tab.table.setItem(i, 1, QTableWidgetItem(str(r[2])))

        self.teachers_tab.show_tab()
        self.teachers_tab.upd_btn.clicked.connect(lambda: self._update_shedule())

    def _create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Shedule")

        self.svbox = QVBoxLayout()
        self.shbox1 = QVBoxLayout()

        self.table_gboxes = []
        self.update_btns = []

        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.buttonClicked[QAbstractButton].connect(
            lambda button=QAbstractButton: self._change_day_from_table(button))

        self.delbuttonGroup = QButtonGroup(self)
        self.delbuttonGroup.buttonClicked[QAbstractButton].connect(
            lambda button=QAbstractButton: self._del_row_table(button))

        for i in self.days:
            tmp = QGroupBox(i)
            self.shbox1.addWidget(tmp)
            self.table_gboxes.append((tmp, i))

        for i in self.table_gboxes:
            self._create_table(i)

        self.svbox.addLayout(self.shbox1)
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox2)

        self.upd_btn = QPushButton("Update")
        self.upd_btn.clicked.connect(lambda: self._update_shedule())
        self.shbox1.addWidget(self.upd_btn)

        self.ins_btn = QPushButton("Insert")
        self.ins_btn.clicked.connect(lambda: self._insert_row_table())
        self.shbox1.addWidget(self.ins_btn)

        self.shedule_tab.setLayout(self.svbox)

    def _create_table(self, table_gbox):
        self.table = QTableWidget()
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Subject", "Room_numb", "Time", "Even or Odd", "", ""])

        self._update_table(table_gbox[1])

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.table)
        table_gbox[0].setLayout(self.mvbox)

    def _update_table(self, table_gbox):
        tmp = "SELECT * FROM timetable.timetable WHERE day='{}' and (week='{}' OR week='both')".format(table_gbox,
                                                                                                       week())
        self.cursor.execute(tmp)
        records = list(self.cursor.fetchall())

        self.table.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join " + '{} {}'.format(i, self.day_shorts[table_gbox]))
            delButton = QPushButton("Delete " + '{} {}'.format(i, self.day_shorts[table_gbox]))
            self.table.setItem(i, 0, QTableWidgetItem(str(r[2])))
            self.table.setItem(i, 1, QTableWidgetItem(str(r[3])))
            self.table.setItem(i, 2, QTableWidgetItem(str(r[4])))
            self.table.setItem(i, 3, QTableWidgetItem(str(r[5])))
            self.table.setCellWidget(i, 4, joinButton)
            self.table.setCellWidget(i, 5, delButton)

            self.buttonGroup.addButton(joinButton)
            self.delbuttonGroup.addButton(delButton)  # rowNum , day

    def _change_day_from_table(self, button):
        print("Введите изменения:")
        get_from_button = button.text().split()[1:]
        com = (int(get_from_button[0]), self.day_shorts_[int(get_from_button[1])])
        row = list()

        for box in self.table_gboxes:
            if box[1] == com[1]:
                self._create_table(box)
                for i in range(self.table.columnCount()):
                    try:
                        row.append(self.table.item(com[0], i).text())
                    except:
                        row.append(None)

        try:

            to_replace = list(input().split(', '))
            to_replace.append(com[1])
            to_replace.extend([_ for _ in row if _ is not None])
            tmp = "UPDATE timetable.timetable SET subject='{0}', room_numb='{1}', start_time='{2}', week='{3}' " \
                  "WHERE day='{4}' and subject='{5}' and room_numb='{6}' and start_time='{7}' and week='{8}'".format(
                to_replace[0], to_replace[1], to_replace[2], to_replace[3], to_replace[4],
                to_replace[5], to_replace[6], to_replace[7], to_replace[8])
            self.cursor.execute(tmp)
            self.conn.commit()

        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _del_row_table(self, button):

        get_from_button = button.text().split()[1:]
        com = (int(get_from_button[0]), self.day_shorts_[int(get_from_button[1])])
        row = list()

        for box in self.table_gboxes:
            if box[1] == com[1]:
                self._create_table(box)
                for i in range(self.table.columnCount()):
                    try:
                        row.append(self.table.item(com[0], i).text())
                    except:
                        row.append(None)
        try:
            tmp = "DELETE FROM timetable.timetable WHERE day='{}' and subject='{}' " \
                  "and room_numb='{}' and start_time='{}' and week='{}'".format(
                com[1], row[0],
                row[1], row[2],
                row[3])

            self.cursor.execute(tmp)
            self.conn.commit()
            print("Успешно удалено.")
        except:
            QMessageBox.about(self, "Error", "Deletion error")

    def _insert_row_table(self):
        try:
            print("Введите данные: id, day, subject, room_numb, start_time, week")
            tmp = "INSERT INTO timetable.timetable (id,day, subject,room_numb,start_time,week) " \
                  "VALUES ('{}','{}','{}','{}','{}','{}')".format(*input().split(', '))

            self.cursor.execute(tmp)
            self.conn.commit()
            print("Успешно добавлено.")
        except:
            QMessageBox.about(self, "Error", "Insertion error")

    def _update_shedule(self):
        self._create_shedule_tab()
        self._create_subjects_tab()
        self._create_teacher_tab()
        self.tabs.removeTab(0)
        self.tabs.removeTab(0)
        self.tabs.removeTab(0)


class Tabs(QWidget):
    def __init__(self, name_tab, num_columns, name_columns, showtab):
        super(Tabs, self).__init__()

        self.tabs, self.vbox = showtab
        self.tab = QWidget()
        self.tabs.addTab(self.tab, name_tab)
        self.table = QTableWidget()
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.box = QGroupBox()
        self.table.setColumnCount(num_columns)
        self.table.setHorizontalHeaderLabels([*name_columns])

        self.upd_btn = QPushButton("Update")
        self.mvbox = QVBoxLayout()

    def show_tab(self):
        self.mvbox.addWidget(self.upd_btn)
        self.mvbox.addWidget(self.table)
        self.tab.setLayout(self.mvbox)


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())

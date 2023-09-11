
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox, QPushButton
from PyQt5.QtGui import QPainter, QPixmap, QTransform
from PyQt5.QtCore import Qt, QTimer


class CarRace(QWidget):
    def __init__(self):
        super().__init__()

        self.player1_position = 0
        self.player2_position = 0
        self.finished = False

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)  # Увеличиваем размер игрового поля в два раза
        self.setWindowTitle('Гонка')
        self.setFixedSize(800, 600)  # Задаем фиксированный размер окна игры

        self.label_player1 = QLabel(self)
        car1_img = QPixmap('car1.png')  # Путь к изображению машинки №1
        car1_img = car1_img.scaled(80, 100)  # Увеличиваем размер машинки №1
        car1_img = car1_img.transformed(QTransform().rotate(270))  # Поворачиваем машинку №1 на 90 градусов
        self.label_player1.setPixmap(car1_img)
        self.label_player1.move(self.player1_position, 100)

        self.label_player2 = QLabel(self)
        car2_img = QPixmap('car2.png')  # Путь к изображению машинки №2
        car2_img = car2_img.scaled(80, 100)  # Увеличиваем размер машинки №2
        car2_img = car2_img.transformed(QTransform().rotate(270))  # Поворачиваем машинку №2 на 90 градусов
        self.label_player2.setPixmap(car2_img)
        self.label_player2.move(self.player2_position, 350)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateGame)

        self.restart_button = QPushButton('Перезапуск', self)
        self.restart_button.move(400, 550)
        self.restart_button.clicked.connect(self.restartGame)
        self.restart_button.setFocusPolicy(Qt.NoFocus)  # Устанавливаем политику фокуса для кнопки "Перезапуск"

        self.rules_button = QPushButton('Правила', self)
        self.rules_button.move(300, 550)
        self.rules_button.clicked.connect(self.showRules)
        self.rules_button.setFocusPolicy(Qt.NoFocus)  # Устанавливаем политику фокуса для кнопки "Правила"

        self.show()

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Up]:
            if not self.finished:
                self.player1_position += 10
                self.label_player1.move(self.player1_position, 100)
                if self.player1_position >= 700:
                    self.finished = True
                    self.showWinner('Первый', 'Машинке №1')


        if event.key() == Qt.Key_Control:
            if not self.finished:
                self.player2_position += 10
                self.label_player2.move(self.player2_position, 350)
                if self.player2_position >= 700:
                    self.finished = True
                    self.showWinner('Второй', 'Машинке №2')

    def showWinner(self, player, car):
        self.timer.stop()
        msg_box = QMessageBox()
        msg_box.setText(f'Победил {player} игрок на {car} ')
        msg_box.setWindowTitle('Игра окончена')
        msg_box.setStandardButtons(QMessageBox.Ok)
        restart_button = msg_box.addButton('Перезапуск', QMessageBox.AcceptRole)
        msg_box.exec_()
        if msg_box.clickedButton() == restart_button:
            self.restartGame()

    def showRules(self):
        rules_text = """
        Правила игры:
        - Цель игры - переместить свою машинку вперед и первым достичь финишной линии.
        - Машинка №2 управляется только с помощью клавиши "Левый CTRL".
        - Машинка №1  управляется только с помощью клавиши "Стрелочка вверх".
        - Когда одна из машинок достигает финишной линии, игра останавливается, и отображается победитель.
        - Чтобы перезапустить игру, нажмите кнопку "Перезапуск".
        """
        msg_box = QMessageBox()
        msg_box.setText(rules_text)
        msg_box.setWindowTitle('Правила игры')
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def restartGame(self):
        self.player1_position = 0
        self.player2_position = 0
        self.finished = False
        self.label_player1.move(self.player1_position, 100)
        self.label_player2.move(self.player2_position, 350)
        self.timer.stop()  # Добавьте вызов метода stop() для остановки таймера
        self.update()  # Добавьте вызов метода update() для перерисовки игрового поля

    def updateGame(self):
        if self.player1_position < 700:
            self.player1_position += 5
            self.label_player1.move(self.player1_position, 100)
        else:
            self.finished = True
            self.showWinner('Второй', 'Машинке №2')

        if self.player2_position < 700:
            self.player2_position += 5
            self.label_player2.move(self.player2_position, 350)
        else:
            self.finished = True
            self.showWinner('Первый', 'Машинке №1')

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        self.drawRoad(qp)  # Рисуем дорогу
        self.drawFinishLine(qp)  # Рисуем финишную линию

        qp.end()

    def drawRoad(self, qp):
        road_img = QPixmap('road.png')  # Путь к изображению дороги
        road_img = road_img.scaled(self.width(), self.height())  # Масштабируем изображение дороги
        qp.drawPixmap(0, 0, road_img)

    def drawFinishLine(self, qp):
        road_img = QPixmap('road.png')  # Загружаем изображение дороги
        road_img = road_img.scaled(self.width(), self.height())  # Масштабируем изображение дороги

        finish_img = QPixmap('Finish.png')  # Загружаем изображение финишной линии
        finish_img = finish_img.scaled(1, self.height())  # Масштабируем изображение финишной линии


        qp.drawPixmap(0, 0, road_img)  # Рисуем дорогу

        # Рисуем финишную линию под машинками
        qp.drawPixmap(700, 57, 10, 235, finish_img)
        qp.drawPixmap(700, 305, 10, 240, finish_img)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = CarRace()
    sys.exit(app.exec_())
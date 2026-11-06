import sys
from PySide6.QtWidgets import QStackedWidget, QComboBox, QAbstractItemView,QPushButton, QWizard
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QParallelAnimationGroup, Property,Qt, QRect


class AnimatedStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.duration = 500
        self.curve = QEasingCurve.OutCubic
        self._is_animating = False

    def slide_to_index(self, index: int):
        """Anime la transition vers un index spécifique"""
        if self._is_animating or index == self.currentIndex():
            return
        
        # Déterminer la direction
        if index > self.currentIndex():
            self.slide_to_widget(self.widget(index), "right_to_left")
        else:
            self.slide_to_widget(self.widget(index), "left_to_right")

    def slide_to_widget(self, next_widget, direction="right_to_left"):
        if self._is_animating:
            return

        self._is_animating = True
        current_widget = self.currentWidget()
        width = self.width()

        # Calcul des positions de départ et d'arrivée
        if direction == "right_to_left":
            offset = width
        else:
            offset = -width

        # Positionner le widget suivant
        next_widget.setGeometry(0, 0, width, self.height())
        next_widget.move(QPoint(offset, 0))
        next_widget.show()
        next_widget.raise_()

        # Groupe d'animations
        self.group = QParallelAnimationGroup()

        # Animation du widget qui arrive
        self.anim_next = QPropertyAnimation(next_widget, b"pos")
        self.anim_next.setDuration(self.duration)
        self.anim_next.setEasingCurve(self.curve)
        self.anim_next.setStartValue(QPoint(offset, 0))
        self.anim_next.setEndValue(QPoint(0, 0))

        # Animation du widget qui sort
        self.anim_current = QPropertyAnimation(current_widget, b"pos")
        self.anim_current.setDuration(self.duration)
        self.anim_current.setEasingCurve(self.curve)
        self.anim_current.setStartValue(QPoint(0, 0))
        self.anim_current.setEndValue(QPoint(-offset, 0))

        self.group.addAnimation(self.anim_next)
        self.group.addAnimation(self.anim_current)

        # Nettoyage à la fin
        self.group.finished.connect(lambda: self.finalize_transition(next_widget, current_widget))
        
        self.group.start()

    def finalize_transition(self, next_widget, old_widget):
        # Définir l'index réel pour Qt
        self.setCurrentWidget(next_widget)
        # Remettre l'ancien widget à sa place (0,0) pour la prochaine fois
        old_widget.move(0, 0)
        self._is_animating = False
        


class SmoothComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Correction ici : On accède à ScrollPerPixel via QAbstractItemView
        self.view().setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        
        self.duration = 400
        self.curve = QEasingCurve.OutCubic

    def wheelEvent(self, event):
        scrollbar = self.view().verticalScrollBar()
        current_value = scrollbar.value()
        
        # On calcule la nouvelle position
        delta = event.angleDelta().y()
        target_value = current_value - delta
        
        # Animation de la barre de défilement
        self.anim = QPropertyAnimation(scrollbar, b"value")
        self.anim.setDuration(self.duration)
        self.anim.setStartValue(current_value)
        self.anim.setEndValue(target_value)
        self.anim.setEasingCurve(self.curve)
        self.anim.start()
        
        event.accept()

    def showPopup(self):
        super().showPopup()
        popup = self.view().window()
        rect = popup.geometry()
        
        # Animation d'ouverture du menu
        self.popup_anim = QPropertyAnimation(popup, b"geometry")
        self.popup_anim.setDuration(250)
        self.popup_anim.setStartValue(QRect(rect.x(), rect.y(), rect.width(), 0))
        self.popup_anim.setEndValue(rect)
        self.popup_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.popup_anim.start()
        
        
        


class AnimatedPushButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._initial_geo = None
        self.duration = 150
        
    def enterEvent(self, event):
        """Animation : Le bouton grossit au survol"""
        if not self._initial_geo:
            self._initial_geo = self.geometry()
            
        self.ani = QPropertyAnimation(self, b"geometry")
        self.ani.setDuration(self.duration)
        self.ani.setEasingCurve(QEasingCurve.OutCubic)
        
        # On calcule une zone légèrement plus grande (ex: +4 pixels de chaque côté)
        new_geo = self._initial_geo.adjusted(-4, -2, 4, 2)
        self.ani.setEndValue(new_geo)
        self.ani.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Animation : Le bouton revient à sa taille normale"""
        self.ani = QPropertyAnimation(self, b"geometry")
        self.ani.setDuration(self.duration)
        self.ani.setEasingCurve(QEasingCurve.OutCubic)
        self.ani.setEndValue(self._initial_geo)
        self.ani.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Animation : Effet d'enfoncement au clic"""
        if event.button() == Qt.LeftButton:
            self.press_ani = QPropertyAnimation(self, b"geometry")
            self.press_ani.setDuration(50)
            # On le réduit un peu pour l'effet "pressé"
            pressed_geo = self.geometry().adjusted(2, 2, -2, -2)
            self.press_ani.setEndValue(pressed_geo)
            self.press_ani.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Animation : Retour après le clic"""
        self.release_ani = QPropertyAnimation(self, b"geometry")
        self.release_ani.setDuration(100)
        self.release_ani.setEasingCurve(QEasingCurve.OutBack) # Petit effet ressort
        self.release_ani.setEndValue(self.geometry().adjusted(-2, -2, 2, 2))
        self.release_ani.start()
        super().mouseReleaseEvent(event)

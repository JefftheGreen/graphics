# /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore


class DraggableScene(QtGui.QGraphicsScene):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.click_event = None
        self.has_moved = False
        self.started_drag = False
        self.draggable_items = self

    def on_drag_start(self, click_event, move_event):
        pass

    def on_drag(self, click_event, move_event):
        pass

    def on_drag_end(self, click_event, release_event):
        pass

    def on_draggable(self, event):
        if self.draggable_items is self:
            return True
        else:
            for d in self.draggable_items:
                if d.contains(d.mapFromScene(event.scenePos())):
                    return True
        return False

    def mousePressEvent(self, event):
        self.has_moved = False
        self.started_drag = False
        self.click_event = event
        for view in self.views():
            if self.on_draggable(event):
                view.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            else:
                view.unsetCursor()

    def mouseMoveEvent(self, event):
        if self.click_event is not None:
            self.has_moved = True
            if not self.started_drag:
                self.on_drag_start(self.click_event, event)
                self.started_drag = True
            else:
                self.on_drag(self.click_event, event)
        else:
            for view in self.views():
                if self.on_draggable(event):
                    view.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
                else:
                    view.unsetCursor()


    def mouseReleaseEvent(self, event):
        if self.click_event is not None:
            self.on_drag_end(self.click_event, event)
            self.click_event = None
        for view in self.views():
            if self.on_draggable(event):
                view.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            else:
                view.unsetCursor()
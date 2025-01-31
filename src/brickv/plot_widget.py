# -*- coding: utf-8 -*-
"""
brickv (Brick Viewer)
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2014, 2016, 2018-2019 Matthias Bolte <matthias@tinkerforge.com>

plot_widget.py: Graph for simple value over time representation

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

import math
import functools
import bisect
from collections import namedtuple
import time

from PyQt5.QtCore import pyqtSignal, Qt, QObject, QTimer, QSize, QRectF, QLineF, QPoint, QPointF
from PyQt5.QtGui import QPainter, QFontMetrics, QPixmap, QIcon, QColor, \
                        QPainterPath, QTransform, QPen, QFont
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QToolButton, \
                            QSizePolicy, QLabel, QSpinBox

from brickv.utils import draw_rect
from brickv.fixed_size_label import FixedSizeLabel

CurveConfig = namedtuple('CurveConfig', 'title color value_wrapper value_formatter')
MovingAverageConfig = namedtuple('MovingAverageConfig', 'min_length max_length callback')

EPSILON = 0.000001
DEBUG = False
CURVE_Y_OFFSET_COMPENSATION = 0.5
CURVE_HEIGHT_COMPENSATION = 1.0

def istr(i):
    return str(int(i))

def fstr(f):
    s = ('%.10f' % f).rstrip('0')

    if s.endswith('.'):
        s += '0'

    return s

def fuzzy_eq(a, b):
    return abs(a - b) < EPSILON

def fuzzy_leq(a, b):
    return a < b or fuzzy_eq(a, b)

def fuzzy_geq(a, b):
    return a > b or fuzzy_eq(a, b)

class CurveValueWrapper:
    def __init__(self):
        self.locked = False
        self.history = []
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

        if self.locked:
            return

        self.history.append((time.monotonic(), value))

class Scale(QObject):
    def __init__(self, tick_text_font, title_text_font, parent):
        super().__init__(parent)

        self.axis_line_thickness = 1 # px, fixed

        self.tick_mark_thickness = 1 # px, fixed
        self.tick_mark_size_small = 5 # px, fixed
        self.tick_mark_size_medium = 7 # px, fixed
        self.tick_mark_size_large = 9 # px, fixed

        self.tick_text_font = tick_text_font
        self.tick_text_font_metrics = QFontMetrics(self.tick_text_font)
        self.tick_text_height = self.tick_text_font_metrics.boundingRect('0123456789').height()
        self.tick_text_height_half = int(round(self.tick_text_height / 2.0))
        self.tick_text_half_digit_width = int(round(self.tick_text_font_metrics.width('0123456789') / 20.0))

        self.tick_value_to_str = istr

        self.title_text_font = title_text_font
        self.title_text_font_metrics = QFontMetrics(self.title_text_font)

class XScale(Scale):
    def __init__(self, tick_text_font, title_text_font, title_text, tick_align_first, tick_skip_last, parent):
        super().__init__(tick_text_font, title_text_font, parent)

        self.tick_align_first = tick_align_first
        self.tick_skip_last = tick_skip_last

        self.step_size = None # set by update_tick_config
        self.step_subdivision_count = None # set by update_tick_config

        self.tick_mark_to_tick_text = 0 # px, fixed

        self.tick_text_to_title_text = 4 # px, fixed

        self.title_text = title_text
        self.title_text_height = self.title_text_font_metrics.boundingRect(self.title_text).height()
        self.title_text_to_border = 2 # px, fixed

        self.total_height = self.axis_line_thickness + \
                            self.tick_mark_size_large + \
                            self.tick_mark_to_tick_text + \
                            self.tick_text_height + \
                            self.tick_text_to_title_text + \
                            self.title_text_height + \
                            self.title_text_to_border # px, fixed

        self.update_tick_config(5.0, 5)

    def update_tick_config(self, step_size, step_subdivision_count):
        self.step_size = float(step_size)
        self.step_subdivision_count = int(step_subdivision_count)

        if fuzzy_geq(self.step_size, 1.0):
            self.tick_value_to_str = istr
        else:
            self.tick_value_to_str = fstr

    def draw(self, painter, width, factor, value_min, value_max):
        factor_int = int(factor)

        pen = QPen()
        pen.setCosmetic(True)
        pen.setWidth(0)
        pen.setColor(Qt.black)

        painter.setPen(pen)

        # axis line
        painter.drawLine(0, 0, width - 1, 0)

        # ticks
        painter.setFont(self.tick_text_font)

        tick_text_y = self.axis_line_thickness + \
                      self.tick_mark_size_large + \
                      self.tick_mark_to_tick_text
        tick_text_width = factor_int + self.tick_mark_thickness + factor_int
        tick_text_height = self.tick_text_height
        first = True
        value = value_min - (value_min % self.step_size)

        while fuzzy_leq(value, value_max):
            x = int((value - value_min) * factor)

            if width - x <= 2: # accept 2px jitter
                if self.tick_skip_last:
                    break

                tick_text_x = x + self.tick_text_half_digit_width
                tick_text_alignment = Qt.AlignRight
            elif first and self.tick_align_first == 'right':
                tick_text_x = x - self.tick_text_half_digit_width
                tick_text_alignment = Qt.AlignLeft
            else:
                tick_text_x = x - factor_int
                tick_text_alignment = Qt.AlignHCenter

            if x >= -2: # accept 2px jitter
                painter.drawLine(x, 0, x, self.tick_mark_size_large)

                if DEBUG:
                    painter.fillRect(tick_text_x, tick_text_y,
                                     tick_text_width, tick_text_height,
                                     Qt.yellow)

                painter.drawText(tick_text_x, tick_text_y,
                                 tick_text_width, tick_text_height,
                                 Qt.TextDontClip | Qt.AlignBottom | tick_text_alignment,
                                 self.tick_value_to_str(value))

            for i in range(1, self.step_subdivision_count):
                subvalue = value + (self.step_size * i / self.step_subdivision_count)

                if not fuzzy_leq(subvalue, value_max):
                    break

                subx = int((subvalue - value_min) * factor)

                if subx >= -2: # accept 2px jitter
                    if width - subx <= 2 and self.tick_skip_last: # accept 2px jitter
                        break

                    if i % 2 == 0 and self.step_subdivision_count % 2 == 0:
                        tick_mark_size = self.tick_mark_size_medium
                    else:
                        tick_mark_size = self.tick_mark_size_small

                    painter.drawLine(subx, 0, subx, tick_mark_size)

            first = False
            value += self.step_size

        # title
        title_text_x = 0
        title_text_y = self.axis_line_thickness + \
                       self.tick_mark_size_large + \
                       self.tick_mark_to_tick_text + \
                       self.tick_text_height + \
                       self.tick_text_to_title_text
        title_text_width = width
        title_text_height = self.title_text_height

        if DEBUG:
            painter.fillRect(title_text_x, title_text_y,
                             title_text_width, title_text_height,
                             Qt.yellow)

        painter.setFont(self.title_text_font)
        painter.drawText(title_text_x, title_text_y,
                         title_text_width, title_text_height,
                         Qt.TextDontClip | Qt.AlignHCenter | Qt.AlignBottom,
                         self.title_text)

class YScale(Scale):
    total_width_changed = pyqtSignal()

    def __init__(self, tick_text_font, title_text_font, title_text, parent):
        super().__init__(tick_text_font, title_text_font, parent)

        self.value_min = None # set by update_tick_config
        self.value_max = None # set by update_tick_config

        self.step_size = None # set by update_tick_config
        self.step_subdivision_count = None # set by update_tick_config

        self.tick_mark_to_tick_text = 3 # px, fixed

        self.tick_text_to_title_text = 7 # px, fixed
        self.tick_text_max_width = 10 # px, initial value, calculated in update_tick_config

        self.title_text = title_text
        self.title_text_to_border = 2 # px, fixed
        self.title_text_height = None # set by update_title_text_height
        self.title_text_pixmap = None
        self.title_text_padding = 0 # px, initial value, set by set_title_text_padding

        self.total_width = None # set by update_total_width
        self.total_unpadded_width = None # set by update_total_width

        self.update_title_text_height(1000)
        self.update_tick_config(-1.0, 1.0, 1.0, 5)

    def update_tick_config(self, value_min, value_max, step_size, step_subdivision_count):
        self.value_min = float(value_min)
        self.value_max = float(value_max)
        self.step_size = float(step_size)
        self.step_subdivision_count = int(step_subdivision_count)

        if fuzzy_geq(self.step_size, 1.0):
            self.tick_value_to_str = istr
        else:
            self.tick_value_to_str = fstr

        value = self.value_min
        tick_text_max_width = self.tick_text_font_metrics.width(self.tick_value_to_str(value))

        while fuzzy_leq(value, self.value_max):
            tick_text_max_width = max(tick_text_max_width, self.tick_text_font_metrics.width(self.tick_value_to_str(value)))
            value += self.step_size

        self.tick_text_max_width = tick_text_max_width

        self.update_total_width()

    def update_title_text_height(self, max_width):
        self.title_text_height = self.title_text_font_metrics.boundingRect(0, 0, max_width, 1000,
                                                                           Qt.TextWordWrap | Qt.AlignHCenter | Qt.AlignTop,
                                                                           self.title_text).height()

        self.update_total_width()

    def set_title_text_padding(self, padding):
        old_title_text_padding = self.title_text_padding

        self.title_text_padding = padding

        self.update_total_width()

        if old_title_text_padding != self.title_text_padding:
            self.total_width_changed.emit()

    def update_total_width(self):
        old_total_width = self.total_width

        self.total_unpadded_width = self.axis_line_thickness + \
                                    self.tick_mark_size_large + \
                                    self.tick_mark_to_tick_text + \
                                    self.tick_text_max_width + \
                                    self.tick_text_to_title_text + \
                                    self.title_text_height + \
                                    self.title_text_to_border

        self.total_width = self.total_unpadded_width + max(self.title_text_padding, 0)

        if old_total_width != self.total_width:
            self.total_width_changed.emit()

    def draw(self, painter, height, factor):
        painter.save()
        painter.translate(0, -CURVE_Y_OFFSET_COMPENSATION)
        painter.scale(1, -factor)
        painter.translate(0, -self.value_min)

        pen = QPen()
        pen.setCosmetic(True)
        pen.setWidth(0)
        pen.setColor(Qt.black)

        painter.setPen(pen)

        if DEBUG:
            painter.fillRect(QRectF(0, self.value_min,
                                    -self.axis_line_thickness - self.tick_mark_size_large, self.value_max - self.value_min),
                             Qt.cyan)

        # axis line
        painter.drawLine(QLineF(-self.axis_line_thickness, self.value_min,
                                -self.axis_line_thickness, self.value_max))

        # ticks
        tick_text_values = []
        value = self.value_min

        while fuzzy_leq(value, self.value_max):
            tick_text_values.append(value)

            painter.drawLine(QLineF(-self.axis_line_thickness, value,
                                    -self.axis_line_thickness - self.tick_mark_size_large, value))

            for i in range(1, self.step_subdivision_count):
                subvalue = value + (self.step_size * i / self.step_subdivision_count)

                if not fuzzy_leq(subvalue, self.value_max):
                    break

                if i % 2 == 0 and self.step_subdivision_count % 2 == 0:
                    tick_mark_size = self.tick_mark_size_medium
                else:
                    tick_mark_size = self.tick_mark_size_small

                painter.drawLine(QLineF(-self.axis_line_thickness, subvalue,
                                        -self.axis_line_thickness - tick_mark_size, subvalue))

            value += self.step_size

        painter.restore()

        painter.setFont(self.tick_text_font)

        tick_text_x = -self.axis_line_thickness - \
                      self.tick_mark_size_large - \
                      self.tick_mark_to_tick_text - \
                      self.tick_text_max_width
        tick_text_width = self.tick_text_max_width
        tick_text_height = self.tick_text_height_half * 2

        transform = QTransform()

        transform.translate(0, -CURVE_Y_OFFSET_COMPENSATION)
        transform.scale(1, -factor)
        transform.translate(0, -self.value_min)

        for value in tick_text_values:
            tick_text_point = transform.map(QPointF(tick_text_x, value))

            tick_text_x = tick_text_point.x()
            tick_text_y = tick_text_point.y() - self.tick_text_height_half

            if DEBUG:
                painter.fillRect(tick_text_x, tick_text_y,
                                 tick_text_width, tick_text_height,
                                 Qt.yellow)

            painter.drawText(tick_text_x, tick_text_y, tick_text_width, tick_text_height,
                             Qt.TextDontClip | Qt.AlignRight | Qt.AlignVCenter,
                             self.tick_value_to_str(value))

        # title
        title_width = height
        title_height = self.title_text_height

        if self.title_text_pixmap == None or self.title_text_pixmap.size() != QSize(title_width, title_height):
            # render title text scaled 2x into pixmap. then later draw pixmap scaled 0.5x
            # to get proper text rendering on macOS with retina display
            self.title_text_pixmap = QPixmap(title_width * 2 + 100, title_height * 2 + 100)
            self.title_text_pixmap.fill(QColor(0, 0, 0, 0))

            title_painter = QPainter(self.title_text_pixmap)

            if DEBUG:
                title_painter.fillRect(50, 50, title_width * 2, title_height * 2, Qt.yellow)

            title_text_font = QFont(self.title_text_font)
            title_text_font.setPointSizeF(title_text_font.pointSizeF() * 2)

            title_painter.setFont(title_text_font)
            title_painter.drawText(50, 50, title_width * 2, title_height * 2,
                                   Qt.TextWordWrap | Qt.TextDontClip | Qt.AlignHCenter | Qt.AlignTop,
                                   self.title_text)

            title_painter = None

        painter.save()
        painter.scale(0.5, 0.5)
        painter.rotate(-90)
        painter.translate(-50, -50)

        title_x = -1
        title_y = -self.axis_line_thickness - \
                  self.tick_mark_size_large - \
                  self.tick_mark_to_tick_text - \
                  self.tick_text_max_width - \
                  self.tick_text_to_title_text - \
                  max(self.title_text_padding, 0) - \
                  title_height

        painter.drawPixmap(title_x * 2, title_y * 2, self.title_text_pixmap)

        painter.restore()

class CurveArea(QWidget):
    def __init__(self, plot):
        super().__init__(plot)

        self.plot = plot

        self.max_points = None

        # FIXME: need to enable opaque painting to avoid that updates of other
        #        widgets trigger a full update of the curve
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)

    # override QWidget.paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        width = self.width()
        height = self.height()

        if DEBUG:
            painter.fillRect(0, 0, width, height, Qt.blue)
        else:
            painter.fillRect(event.rect(), self.plot.canvas_color)

        y_min_scale = self.plot.y_scale.value_min
        y_max_scale = self.plot.y_scale.value_max

        factor_x = width / self.plot.x_diff
        factor_y = (height - CURVE_HEIGHT_COMPENSATION) / max(y_max_scale - y_min_scale, EPSILON)

        if self.plot.x_min != None and self.plot.x_max != None:
            x_min = self.plot.x_min
            x_max = self.plot.x_max

            if self.plot.curve_start == 'left':
                curve_x_offset = int((x_min - int(x_min)) * factor_x)
            else:
                curve_x_offset = int((self.plot.x_diff - (x_max - x_min)) * factor_x)

            transform = QTransform()

            transform.translate(curve_x_offset, height - CURVE_Y_OFFSET_COMPENSATION)
            transform.scale(factor_x, -factor_y)
            transform.translate(-x_min, -y_min_scale)

            self.plot.partial_update_width = math.ceil(transform.map(QLineF(0, 0, 1.5, 0)).length())
            inverted_event_rect = transform.inverted()[0].mapRect(QRectF(event.rect()))

            painter.save()
            painter.setTransform(transform)

            pen = QPen()
            pen.setCosmetic(True)
            pen.setWidth(0)

            painter.setPen(pen)

            if False and self.plot.curves_visible[0]:
                # Currently unused support for bar graphs.
                # If we need this later on we should add an option to the
                # PlotWidget for it.
                # I tested this for the Sound Pressure Level Bricklet and it works,
                # but it didnt't look good.
                curve_x = self.plot.curves_x[0]
                curve_y = self.plot.curves_y[0]

                t = time.time()
                if self.max_points == None:
                    self.max_points = []
                    for y in curve_y:
                        self.max_points.append((t, y))
                else:
                    for i in range(len(curve_y)):
                        if (curve_y[i] > self.max_points[i][1]) or ((t - self.max_points[i][0]) > 5):
                            self.max_points[i] = (t, curve_y[i])

                for i in range(len(self.plot.curves_x[0])):
                    pen.setColor(self.plot.curve_configs[0].color)
                    painter.setPen(pen)
                    painter.drawLine(QPoint(curve_x[i], 0), QPoint(curve_x[i], curve_y[i]))
                    pen.setColor(Qt.white)
                    painter.setPen(pen)
                    painter.drawLine(QPoint(curve_x[i], curve_y[i]), QPoint(curve_x[i], y_max_scale))
                    pen.setColor(Qt.darkGreen)
                    painter.setPen(pen)
                    painter.drawPoint(QPoint(curve_x[i], self.max_points[i][1]))
            else:
                for c in range(len(self.plot.curves_x)):
                    if not self.plot.curves_visible[c]:
                        continue

                    curve_x = self.plot.curves_x[c]
                    curve_y = self.plot.curves_y[c]
                    curve_jump = self.plot.curves_jump[c]
                    path = QPainterPath()
                    lineTo = path.lineTo
                    moveTo = path.moveTo
                    start = max(min(bisect.bisect_left(curve_x, inverted_event_rect.left()), len(curve_x) - 1) - 1, 0)

                    if start >= len(curve_x):
                        continue

                    moveTo(curve_x[start], curve_y[start])

                    for i in range(start + 1, len(curve_x)):
                        if curve_jump[i]:
                            moveTo(curve_x[i], curve_y[i])
                        else:
                            lineTo(curve_x[i], curve_y[i])

                    pen.setColor(self.plot.curve_configs[c].color)
                    painter.setPen(pen)
                    painter.drawPath(path)

            painter.restore()

class Plot(QWidget):
    def __init__(self, parent, x_scale_title_text, y_scale_title_text, x_scale_skip_last_tick,
                 curve_configs, x_scale_visible, y_scale_visible, curve_outer_border_visible,
                 curve_motion, canvas_color, curve_start, x_diff, y_diff_min,
                 y_scale_shrinkable, update_interval):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.curve_configs = curve_configs
        self.x_scale_visible = x_scale_visible
        self.y_scale_visible = y_scale_visible
        self.update_interval = update_interval

        if curve_outer_border_visible:
            self.curve_outer_border = 5 # px, fixed
        else:
            self.curve_outer_border = 0 # px, fixed

        self.curve_motion = curve_motion
        self.curve_to_scale = 8 # px, fixed
        self.canvas_color = canvas_color
        self.curve_start = curve_start
        self.x_diff = x_diff
        self.y_diff_min = y_diff_min
        self.partial_update_width = 50 # px, initial value, calculated in update
        self.partial_update_enabled = False

        self.tick_text_font = self.font()

        self.title_text_font = self.font()
        self.title_text_font.setPointSize(round(self.title_text_font.pointSize() * 1.2))
        self.title_text_font.setBold(True)

        self.x_scale = XScale(self.tick_text_font, self.title_text_font, x_scale_title_text,
                              'center' if y_scale_visible else 'right', x_scale_skip_last_tick, self)

        self.y_scale = YScale(self.tick_text_font, self.title_text_font, y_scale_title_text, self)
        self.y_scale_fixed = False
        self.y_scale_shrinkable = y_scale_shrinkable
        self.y_scale_height_offset = max(self.curve_outer_border, self.y_scale.tick_text_height_half) # px, from top

        self.curve_area = CurveArea(self)
        self.y_scale.total_width_changed.connect(self.resize_curve_area)

        self.clear_graph()
        self.resize_curve_area()

    # override QWidget.sizeHint
    def sizeHint(self):
        return QSize(600, 300)

    # override QWidget.resizeEvent
    def resizeEvent(self, event):
        height = event.size().height()
        max_width = height - self.y_scale_height_offset - self.x_scale.total_height - self.curve_to_scale

        self.y_scale.update_title_text_height(max_width)

        QWidget.resizeEvent(self, event)

        self.resize_curve_area()

    # override QWidget.paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        width = self.width()
        height = self.height()

        if self.y_scale_visible:
            curve_width = width - self.y_scale.total_width - self.curve_to_scale - self.curve_outer_border
        else:
            curve_width = width - self.curve_outer_border - self.curve_outer_border

        curve_height = self.get_curve_height(height)

        if DEBUG:
            painter.fillRect(0, 0, width, height, Qt.green)

        # fill canvas
        if self.y_scale_visible:
            canvas_x = self.y_scale.total_width + self.curve_to_scale - self.curve_outer_border
            canvas_y = self.y_scale_height_offset - self.curve_outer_border
        else:
            canvas_x = 0
            canvas_y = 0

        canvas_width = self.curve_outer_border + curve_width + self.curve_outer_border
        canvas_height = self.curve_outer_border + curve_height + self.curve_outer_border

        painter.fillRect(canvas_x, canvas_y, canvas_width, canvas_height, self.canvas_color)

        # draw canvas border
        if self.curve_outer_border > 0:
            draw_rect(painter, canvas_x, canvas_y, canvas_width, canvas_height, 1, QColor(190, 190, 190))

        if DEBUG:
            painter.fillRect(canvas_x + self.curve_outer_border,
                             canvas_y + self.curve_outer_border,
                             curve_width,
                             curve_height,
                             Qt.cyan)

        # draw scales
        if self.x_scale_visible:
            factor_x = curve_width / self.x_diff

            self.draw_x_scale(painter, curve_width, factor_x)

        if self.y_scale_visible:
            y_min_scale = self.y_scale.value_min
            y_max_scale = self.y_scale.value_max

            factor_y = (curve_height - CURVE_HEIGHT_COMPENSATION) / max(y_max_scale - y_min_scale, EPSILON)

            self.draw_y_scale(painter, curve_height, factor_y)

    def resize_curve_area(self):
        if self.curve_area == None:
            return

        width = self.width()
        height = self.height()

        if self.y_scale_visible:
            curve_x = self.y_scale.total_width + self.curve_to_scale
            curve_y = self.y_scale_height_offset
            curve_width = width - self.y_scale.total_width - self.curve_to_scale - self.curve_outer_border
        else:
            curve_x = self.curve_outer_border
            curve_y = self.curve_outer_border
            curve_width = width - self.curve_outer_border - self.curve_outer_border

        curve_height = self.get_curve_height(height)

        self.curve_area.setGeometry(curve_x, curve_y, curve_width, curve_height)

    def set_x_scale(self, step_size, step_subdivision_count):
        self.x_scale.update_tick_config(step_size, step_subdivision_count)

    def set_fixed_y_scale(self, value_min, value_max, step_size, step_subdivision_count):
        self.y_scale_fixed = True
        self.y_scale.update_tick_config(value_min, value_max, step_size, step_subdivision_count)

    def get_legend_offset_y(self): # px, from top
        return max(self.y_scale.tick_text_height_half - self.curve_outer_border, 0)

    def get_curve_height(self, height):
        if self.x_scale_visible and self.y_scale_visible:
            curve_height = height - self.y_scale_height_offset - self.x_scale.total_height - self.curve_to_scale
        elif self.x_scale_visible:
            curve_height = height - self.curve_outer_border - self.x_scale.total_height - self.curve_to_scale
        elif self.y_scale_visible:
            curve_height = height - self.y_scale_height_offset - self.y_scale_height_offset
        else:
            curve_height = height - self.curve_outer_border - self.curve_outer_border

        return curve_height

    def draw_x_scale(self, painter, width, factor):
        if self.y_scale_visible:
            offset_x = self.y_scale.total_width + self.curve_to_scale
        else:
            offset_x = self.curve_outer_border

        offset_y = self.height() - self.x_scale.total_height

        if self.x_min != None:
            x_min = math.floor(self.x_min)
        else:
            x_min = 0.0

        painter.save()
        painter.translate(offset_x, offset_y)
        self.x_scale.draw(painter, width, factor, x_min, x_min + self.x_diff)
        painter.restore()

    def draw_y_scale(self, painter, height, factor):
        offset_x = self.y_scale.total_width

        if self.x_scale_visible:
            offset_y = self.height() - self.x_scale.total_height - self.curve_to_scale
        else:
            offset_y = self.height() - self.y_scale_height_offset

        painter.save()
        painter.translate(offset_x, offset_y)
        self.y_scale.draw(painter, height, factor)
        painter.restore()

    # NOTE: assumes that x constantly grows
    def add_data(self, c, x, y):
        if self.y_type == None:
            self.y_type = type(y)

        x = float(x)
        y = float(y)

        last_y_min = self.y_min
        last_y_max = self.y_max

        if self.x_min == None:
            self.x_min = x

        if self.x_max == None:
            self.x_max = x

        if self.curves_visible[c]:
            if self.y_min == None:
                self.y_min = y
            else:
                self.y_min = min(self.y_min, y)

            if self.y_max == None:
                self.y_max = y
            else:
                self.y_max = max(self.y_max, y)

        self.curves_x[c].append(x)
        self.curves_y[c].append(y)
        self.curves_jump[c].append(self.curves_jump_pending[c])
        self.curves_jump_pending[c] = False

        if self.curves_x_min[c] == None:
            self.curves_x_min[c] = x

        if self.curves_x_max[c] == None:
            self.curves_x_max[c] = x

        if self.curves_y_min[c] == None:
            self.curves_y_min[c] = y
        else:
            self.curves_y_min[c] = min(self.curves_y_min[c], y)

        if self.curves_y_max[c] == None:
            self.curves_y_max[c] = y
        else:
            self.curves_y_max[c] = max(self.curves_y_max[c], y)

        if len(self.curves_x[c]) > 0:
            if (self.curves_x[c][-1] - self.curves_x[c][0]) >= self.x_diff:
                if self.curve_motion == 'jump': # 1 second
                    k_motion = bisect.bisect_left(self.curves_x[c], int(self.x_min) + 1.0)
                else: # smooth
                    k_motion = 1

                self.curves_x[c] = self.curves_x[c][k_motion:]
                self.curves_y[c] = self.curves_y[c][k_motion:]
                self.curves_jump[c] = self.curves_jump[c][k_motion:]

                if len(self.curves_x[c]) > 0:
                    self.curves_x_min[c] = self.curves_x[c][0]
                    self.curves_x_max[c] = self.curves_x[c][-1]
                else:
                    self.curves_x_min[c] = None
                    self.curves_x_max[c] = None

                if len(self.curves_y[c]) > 0:
                    self.curves_y_min[c] = min(self.curves_y[c])
                    self.curves_y_max[c] = max(self.curves_y[c])
                else:
                    self.curves_y_min[c] = None
                    self.curves_y_max[c] = None

                self.update_x_min_max_y_min_max()

                self.partial_update_enabled = True
            else:
                self.curves_x_max[c] = self.curves_x[c][-1]
                self.x_max = max([curve_x_max for curve_x_max in self.curves_x_max if curve_x_max != None])

        if self.curves_visible[c] and (last_y_min != self.y_min or last_y_max != self.y_max):
            self.update_y_min_max_scale()

        if self.partial_update_enabled:
            self.curve_area.update(self.curve_area.width() - self.partial_update_width, 0, self.partial_update_width, self.curve_area.height())
        else:
            self.curve_area.update()

    def add_jump(self, c):
        self.curves_jump_pending[c] = True

    # NOTE: assumes that x and y are non-empty lists and that x is sorted ascendingly
    def set_data(self, c, x, y):
        if self.y_type == None:
            self.y_type = type(y[0])

        x = list(map(float, x)) # also makes a copy of x
        y = list(map(float, y)) # also makes a copy of y

        x_min = x[0]
        x_max = x[-1]

        y_min = min(y)
        y_max = max(y)

        last_y_min = self.y_min
        last_y_max = self.y_max

        self.curves_x[c] = x
        self.curves_y[c] = y
        self.curves_jump[c] = [False] * len(x)
        self.curves_jump_pending[c] = False

        self.curves_x_min[c] = x_min
        self.curves_x_max[c] = x_max

        self.curves_y_min[c] = y_min
        self.curves_y_max[c] = y_max

        self.update_x_min_max_y_min_max()

        if self.curves_visible[c] and (last_y_min != self.y_min or last_y_max != self.y_max):
            self.update_y_min_max_scale()

        self.curve_area.update()

    def update_x_min_max_y_min_max(self):
        last_x_min, last_x_max, last_y_min, last_y_max = self.x_min, self.x_max, self.y_min, self.y_max
        curves_x_min = [curve_x_min for curve_x_min in self.curves_x_min if curve_x_min != None]
        curves_x_max = [curve_x_max for curve_x_max in self.curves_x_max if curve_x_max != None]

        if len(curves_x_min) > 0:
            self.x_min = min(curves_x_min)
        else:
            self.x_min = None

        if len(curves_x_max) > 0:
            self.x_max = max(curves_x_max)
        else:
            self.x_max = None

        curves_y_min = [curve_y_min for c, curve_y_min in enumerate(self.curves_y_min) if self.curves_visible[c] and curve_y_min != None]
        curves_y_max = [curve_y_max for c, curve_y_max in enumerate(self.curves_y_max) if self.curves_visible[c] and curve_y_max != None]

        if len(curves_y_min) > 0:
            if self.y_scale_shrinkable or self.y_min == None:
                self.y_min = min(curves_y_min)
            else:
                self.y_min = min(min(curves_y_min), self.y_min)
        else:
            self.y_min = None

        if len(curves_y_max) > 0:
            if self.y_scale_shrinkable or self.y_max == None:
                self.y_max = max(curves_y_max)
            else:
                self.y_max = max(max(curves_y_max), self.y_max)
        else:
            self.y_max = None

        if (last_x_min, last_x_max, last_y_min, last_y_max) != (self.x_min, self.x_max, self.y_min, self.y_max):
            self.update()
            self.curve_area.update()

    def update_y_min_max_scale(self):
        if self.y_scale_fixed:
            return

        if self.y_min == None or self.y_max == None:
            y_min = 0.0
            y_max = 0.0
        else:
            y_min = self.y_min
            y_max = self.y_max

        y_diff = abs(y_max - y_min)

        # if y-diff if below minimum then force some to avoid over-emphasizing
        # minimal noise
        if self.y_diff_min == None and y_diff < EPSILON:
            y_min -= 0.5
            y_max += 0.5
            y_diff = abs(y_max - y_min)
        elif self.y_diff_min != None and y_diff < self.y_diff_min:
            y_avg = (y_min + y_max) / 2.0
            y_diff_min_half = self.y_diff_min / 2.0
            y_min = y_avg - y_diff_min_half
            y_max = y_avg + (self.y_diff_min - y_diff_min_half)
            y_diff = abs(y_max - y_min)

        # start with the biggest power of 10 that is smaller than y-diff
        step_size = 10.0 ** math.floor(math.log(y_diff, 10.0))
        step_subdivision_count = 5

        # the divisors are chosen in way to produce the sequence
        # 100.0, 50.0, 20.0, 10.0, 5.0, 2.0, 1.0, 0.5, 0.2, 0.1, 0.05 etc
        divisors = [2.0, 2.5, 2.0]
        subdivisions = [5, 4, 5]
        d = 0

        if self.y_type == int:
            step_size_min = 1.0
        else:
            step_size_min = EPSILON

        # decrease y-axis step-size until it divides y-diff in 4 or more parts
        while fuzzy_geq(step_size / divisors[d % len(divisors)], step_size_min) \
              and y_diff / step_size < 4.0:
            step_size /= divisors[d % len(divisors)]
            step_subdivision_count = subdivisions[d % len(subdivisions)]
            d += 1

        if d == 0:
            # if no division occurred in the first while loop then add 1
            # to d to counter the d -= 1 in the next while loop
            d += 1

        # increase y-axis step-size until it divides y-diff in 8 or less parts
        while y_diff / step_size > 8.0: # FIXME: this needs to be dynamically adjusted depending on widget height, see color bricklet
            step_subdivision_count = subdivisions[d % len(subdivisions)]
            d -= 1
            step_size *= divisors[d % len(divisors)]

        # ensure that the y-axis endpoints are multiple of the step-size
        y_min_scale = math.floor(y_min / step_size) * step_size
        y_max_scale = math.ceil(y_max / step_size) * step_size

        # fix rounding (?) errors from floor/ceil scaling
        # FIXME: this resuĺts in sometime more than 8 parts?
        while fuzzy_leq(y_min_scale + step_size, y_min):
            y_min_scale += step_size

        while fuzzy_geq(y_max_scale - step_size, y_max):
            y_max_scale -= step_size

        # if the y-axis endpoints are identical then force them 4 steps apart
        if fuzzy_eq(y_min_scale, y_max_scale):
            y_min_scale -= 2.0 * step_size
            y_max_scale += 2.0 * step_size

        self.y_scale.update_tick_config(y_min_scale, y_max_scale,
                                        step_size, step_subdivision_count)

        self.update()
        self.curve_area.update()

    def show_curve(self, c, show):
        if self.curves_visible[c] == show:
            return

        last_y_min = self.y_min
        last_y_max = self.y_max

        self.curves_visible[c] = show

        self.update_x_min_max_y_min_max()

        if last_y_min != self.y_min or last_y_max != self.y_max:
            self.update_y_min_max_scale()

        self.update()
        self.curve_area.update()

    def clear_graph(self):
        count = len(self.curve_configs)

        if not hasattr(self, 'curves_visible'):
            self.curves_visible = [True]*count # per curve visibility

        self.curves_x = [[] for i in range(count)] # per curve x values
        self.curves_y = [[] for i in range(count)] # per curve y values
        self.curves_jump = [[] for i in range(count)] # per curve jump values
        self.curves_jump_pending = [False] * count # per curve jump pending
        self.curves_x_min = [None] * count # per curve minimum x value
        self.curves_x_max = [None] * count # per curve maximum x value
        self.curves_y_min = [None] * count # per curve minimum y value
        self.curves_y_max = [None] * count # per curve maximum y value
        self.x_min = None # minimum x value over all curves
        self.x_max = None # maximum x value over all curves
        self.y_min = None # minimum y value over all curves
        self.y_max = None # maximum y value over all curves
        self.y_type = None
        self.partial_update_enabled = False

        self.update()
        self.curve_area.update()

class FixedSizeToolButton(QToolButton):
    maximum_size_hint = None

    def sizeHint(self):
        hint = QToolButton.sizeHint(self)

        if self.maximum_size_hint != None:
            hint = QSize(max(hint.width(), self.maximum_size_hint.width()),
                         max(hint.height(), self.maximum_size_hint.height()))

        self.maximum_size_hint = hint

        return hint

class PlotWidget(QWidget):
    def __init__(self,
                 y_scale_title_text,
                 curve_configs,
                 clear_button='default',
                 parent=None,
                 x_scale_visible=True,
                 y_scale_visible=True,
                 curve_outer_border_visible=True,
                 curve_motion='jump', # jump, smooth
                 canvas_color=QColor(245, 245, 245),
                 external_timer=None,
                 key='top-value', # top-value, right-no-icon
                 extra_key_widgets=None,
                 update_interval=0.1, # seconds
                 curve_start='left',
                 moving_average_config=None,
                 x_scale_title_text='Time [s]',
                 x_diff=20,
                 x_scale_skip_last_tick=True,
                 y_resolution=None,
                 y_scale_shrinkable=True):
        super().__init__(parent)

        assert update_interval < 0.5, update_interval

        self.setMinimumSize(300, 250)

        if y_resolution != None:
            y_diff_min = y_resolution * 20
        else:
            y_diff_min = None

        self._stop = True
        self.curve_configs = [CurveConfig(*curve_config) for curve_config in curve_configs]

        for curve_config in self.curve_configs:
            if curve_config.value_wrapper != None:
                assert isinstance(curve_config.value_wrapper, CurveValueWrapper)

        self.plot = Plot(self, x_scale_title_text, y_scale_title_text, x_scale_skip_last_tick,
                         self.curve_configs, x_scale_visible, y_scale_visible, curve_outer_border_visible,
                         curve_motion, canvas_color, curve_start, x_diff, y_diff_min,
                         y_scale_shrinkable, update_interval)
        self.set_x_scale = self.plot.set_x_scale
        self.set_fixed_y_scale = self.plot.set_fixed_y_scale
        self.key = key
        self.key_items = []
        self.key_has_values = key.endswith('-value') if key != None else False
        self.first_show = True
        self.plot_timestamp = 0 # seconds
        self.update_interval = update_interval # seconds
        self.last_timestamp = [None] * len(self.curve_configs)
        self.last_value = [None] * len(self.curve_configs)

        h1layout = QHBoxLayout()
        h1layout.setContentsMargins(0, 0, 0, 0)
        h1layout_empty = True

        if clear_button == 'default':
            self.clear_button = QToolButton()
            self.clear_button.setText('Clear Graph')

            h1layout.addWidget(self.clear_button)
            h1layout.addStretch(1)
            h1layout_empty = False
        else:
            self.clear_button = clear_button

        if self.clear_button != None:
            self.clear_button.clicked.connect(self.clear_clicked)

        v1layout = None

        if self.key != None:
            if len(self.curve_configs) == 1:
                label = FixedSizeLabel(self)
                label.setText(self.curve_configs[0].title)

                self.key_items.append(label)
            else:
                for i, curve_config in enumerate(self.curve_configs):

                    button = FixedSizeToolButton(self)
                    button.setText(curve_config.title)

                    if self.key.endswith('-no-icon'):
                        button.setStyleSheet('color: ' + QColor(curve_config.color).name())
                    else:
                        pixmap = QPixmap(10, 2)
                        QPainter(pixmap).fillRect(0, 0, 10, 2, curve_config.color)

                        button.setIcon(QIcon(pixmap))

                    button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
                    button.setCheckable(True)
                    button.setChecked(True)
                    button.toggled.connect(functools.partial(self.plot.show_curve, i))

                    self.key_items.append(button)

            if self.key.startswith('top-'):
                for key_item in self.key_items:
                    h1layout.addWidget(key_item)
                    h1layout_empty = False
            elif self.key.startswith('right-'):
                v1layout = QVBoxLayout()
                v1layout.setContentsMargins(0, 0, 0, 0)
                v1layout.addSpacing(self.plot.get_legend_offset_y())

                for key_item in self.key_items:
                    v1layout.addWidget(key_item)

                v1layout.addStretch(1)
            else:
                assert False, 'unknown key: ' + self.key

        if not h1layout_empty:
            h1layout.addStretch(1)

        if extra_key_widgets != None:
            if self.key == None or self.key.startswith('top'):
                for widget in extra_key_widgets:
                    h1layout.addWidget(widget)
                    h1layout_empty = False
            elif self.key.startswith('right'):
                if v1layout == None:
                    v1layout = QVBoxLayout()
                    v1layout.setContentsMargins(0, 0, 0, 0)
                    v1layout.addSpacing(self.plot.get_legend_offset_y())

                if self.key.startswith('top'):
                    for widget in extra_key_widgets:
                        v1layout.addWidget(widget)

        v2layout = QVBoxLayout(self)
        v2layout.setContentsMargins(0, 0, 0, 0)

        if not h1layout_empty:
            v2layout.addLayout(h1layout)

        if v1layout != None:
            h2layout = QHBoxLayout()
            h2layout.setContentsMargins(0, 0, 0, 0)

            h2layout.addWidget(self.plot)
            h2layout.addLayout(v1layout)

            v2layout.addLayout(h2layout)
        else:
            v2layout.addWidget(self.plot)

        self.moving_average_config = moving_average_config

        if moving_average_config != None:
            self.moving_average_label = QLabel('Moving Average Length:')
            self.moving_average_spinbox = QSpinBox()
            self.moving_average_spinbox.setMinimum(moving_average_config.min_length)
            self.moving_average_spinbox.setMaximum(moving_average_config.max_length)
            self.moving_average_spinbox.setSingleStep(1)

            self.moving_average_layout = QHBoxLayout()
            self.moving_average_layout.addStretch()
            self.moving_average_layout.addWidget(self.moving_average_label)
            self.moving_average_layout.addWidget(self.moving_average_spinbox)
            self.moving_average_layout.addStretch()

            self.moving_average_spinbox.valueChanged.connect(self.moving_average_spinbox_value_changed)

            v2layout.addLayout(self.moving_average_layout)

        if external_timer == None:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.add_new_data)
            self.timer.start(self.update_interval * 1000)
        else:
            # assuming that the external timer runs with the configured interval
            external_timer.timeout.connect(self.add_new_data)

    def update_y_scale_sibling(self, plot_widget): # internal
        total_unpadded_width_diff = plot_widget.plot.y_scale.total_unpadded_width - self.plot.y_scale.total_unpadded_width

        self.plot.y_scale.set_title_text_padding(total_unpadded_width_diff)

    def add_y_scale_sibling(self, plot_widget):
        plot_widget.plot.y_scale.total_width_changed.connect(functools.partial(self.update_y_scale_sibling, plot_widget))

    def set_moving_average_value(self, value):
        self.moving_average_spinbox.blockSignals(True)
        self.moving_average_spinbox.setValue(value)
        self.moving_average_spinbox.blockSignals(False)

    def get_moving_average_value(self):
        return self.moving_average_spinbox.value()

    def moving_average_spinbox_value_changed(self, value):
        if self.moving_average_config != None:
            if self.moving_average_config.callback != None:
                self.moving_average_config.callback(value)

    # overrides QWidget.showEvent
    def showEvent(self, event):
        QWidget.showEvent(self, event)

        if self.first_show:
            self.first_show = False

            if len(self.key_items) > 1 and self.key.startswith('right'):
                width = max([key_item.width() for key_item in self.key_items])

                for key_item in self.key_items:
                    size = key_item.minimumSize()

                    size.setWidth(width)

                    key_item.setMinimumSize(size)

    def get_key_item(self, i):
        return self.key_items[i]

    def set_data(self, i, x, y):
        # FIXME: how to set potential key items from this?
        self.plot.set_data(i, x, y)

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, stop):
        for i, curve_config in enumerate(self.curve_configs):
            if curve_config.value_wrapper == None:
                continue

            curve_config.value_wrapper.locked = stop
            curve_config.value_wrapper.history = []

            if stop:
                self.plot.add_jump(i)

        self._stop = stop

    # internal
    def add_new_data(self):
        if self.stop:
            return

        monotonic_timestamp = time.monotonic()

        for i, curve_config in enumerate(self.curve_configs):
            if curve_config.value_wrapper == None:
                continue

            history = curve_config.value_wrapper.history
            curve_config.value_wrapper.history = []

            for value_timestamp, value in history:
                assert value != None

                if len(self.key_items) > 0 and self.key_has_values:
                    if curve_config.title == '':
                        self.key_items[i].setText(curve_config.value_formatter(value))
                    else:
                        self.key_items[i].setText(curve_config.title + ': ' + curve_config.value_formatter(value))

                timestamp = self.plot_timestamp - (monotonic_timestamp - value_timestamp)

                if timestamp < 0:
                    continue

                self.plot.add_data(i, timestamp, value)

                self.last_timestamp[i] = timestamp
                self.last_value[i] = value

            # don't allow a gap of more than 0.5 seconds in the data to ensure proper curve motion
            while self.last_timestamp[i] != None and self.plot_timestamp - self.last_timestamp[i] > 0.5:
                self.last_timestamp[i] += self.update_interval

                # FIXME: maybe render this fake data in a different style/color
                self.plot.add_data(i, self.last_timestamp[i], self.last_value[i])

        self.plot_timestamp += self.update_interval

    # internal
    def clear_clicked(self):
        self.plot.clear_graph()
        self.last_timestamp = [None] * len(self.curve_configs)
        self.last_value = [None] * len(self.curve_configs)
        self.plot_timestamp = 0

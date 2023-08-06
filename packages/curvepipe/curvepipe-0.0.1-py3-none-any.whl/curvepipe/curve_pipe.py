from typing import Iterable

import numpy as np


class CurvePipe:
    def __init__(self, x: Iterable, y: Iterable):
        """
        constructor

        :param x: An iterable containing int or float type numbers. Must be of same length as y.
        :param y: An iterable containing int or float type numbers. Must be of same length as x.
        :return: CurvePipe object
        """
        self._x=np.array(x)
        self._y=np.array(y)

    def scale_x(self, factor: float):
        """
        multiplies x values by specified scaling factor

        :param factor: float or int the value
        :return: CurvePipe object
        """
        self._x = self._x*factor
        return self

    def get_x(self):
        """
        :return: x values in a list
        """
        return [round(x, 8) for x in self._x.tolist()]

    def offset_x(self, offset: float):
        """
        :param offset: int or float
        :return: CurvePipe object
        """
        self._x= self._x+offset
        return self

    def transform_x(self, func):
        """
        Applies the func on all x values.

        :param func: lambda function
        :return: CurvePipe object
        """
        self._x = func(self._x)
        return self

    def scale_y(self, factor: float):
        """
        multiplies y values by specified scaling factor
        :param factor: float or int
        :return: CurvePipe object
        """
        self._y = self._y*factor
        return self

    def get_y(self):
        """
        :return: y values in a list
        """
        return [round(y, 8) for y in self._y.tolist()]

    def offset_y(self, offset):
        """
        :param offset: int or float
        :return: CurvePipe object
        """
        self._y= self._y+offset
        return self

    def transform_y(self, func):
        """
        Applies the func on all x values.

        :param func: lambda function
        :return: CurvePipe object
        """
        self._y = func(self._y)
        return self
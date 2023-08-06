#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc:
"""
from rest_framework.response import Response


def make_data(code=200, msg='', **kwargs):
    """

    :param msg:
    :param code: 200(成功), 101(参数错误), 199(其他)
    :return: dict
    """
    if "data" not in kwargs:
        kwargs["data"] = dict()

    if "lists" not in kwargs:
        kwargs["lists"] = list()
    resp = dict(
        code=code,
        msg=msg,
        **kwargs
    )
    return resp


def make_response(code=200, msg='成功', **kwargs):
    """

    :param msg:
    :param code: 200(成功), 101(参数错误), 199(其他),
    :return: Response
    """
    data = make_data(code=code, msg=msg, **kwargs)
    return Response(data)


def done(code=200, msg='成功', **kwargs):
    """

    :param code:
    :param msg:
    :param kwargs:
    :return: Response
    """
    data = make_response(
        code=code,
        msg=msg,
        **kwargs
    )
    return data

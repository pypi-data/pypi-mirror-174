#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""


                   _  _              _
                  | || |            | |
  ___ __   __ ___ | || |_  ___  ___ | |_
 / __|\ \ / // _ \| || __|/ _ \/ __|| __|
 \__ \ \ V /|  __/| || |_|  __/\__ \| |_
 |___/  \_/  \___||_| \__|\___||___/ \__|



"""
from sveltest.components.network.main import RequestBase

class BaseAuth:
    """
    所有认证器都需要基础这个类
    """

    def authenticate(self,):
        """
        进行重写该方法来实现认证
        """
        raise NotImplementedError(".authenticate() must be overridden.")

    def authenticate_header(self,):
        """
        """
        pass


class UserAuth(BaseAuth):

    def authenticate(self):
        """必须重新该 authenticate方法"""
        ret = RequestBase()
        response_ = ret.post(router="http://127.0.0.1:8666/api/v1/login",
                             data={
                              "username": "13453001",
                              "password": "123456"
                            },
                             env_control=False)

        # 直接将整个返回值返回，但不建议怎么做
        # return response_.json
        return {"token":response_.json["token"]}

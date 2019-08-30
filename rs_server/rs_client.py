# -*- encoding: utf-8 -*-

import json
import socket
import thread
import Queue

from elog import *
import dos

RS_TIMEOUT_DEFAULT = 200 #默认超时时间，单位秒
RS_SERVER_PORT = 60021

# 返回码定义
class RS_CODE:
    (OK, UNKONWM, ERR_SERVER, ERR_CMD, ERR_SCRIPT, ) = range(0,-5, -1)

class RSSocketBase:
    def __init__(self,addr_info, log_level=DEBUG):
        self.addr_info = addr_info
        self.sock = None #客户端socket连接
        self.status = False #连接状态
        self._msgpool_recv = Queue.Queue() #消息接收缓冲队列
        self._msgpool_send = Queue.Queue() #消息发送缓冲队列

    def _LogRS(self, text, level=DEBUG):
        try:
            text = text.decode('utf-8')
        except Exception as e:
            pass
        # 统一打印日志格式，以区别不同的client，为了去冗余日志，不显示IP的前两个数据
        addr_info = '%s;%d' % self.addr_info
        client_str = Regexp('\d+\.\d+:\d+$', addr_info)
        if level >= self.log_level:
            Log(level, u'[RS %s]%s' % (client_str, text))

    def _ConnectionSocket(self,sock=None, timeout = 5):
        """
        连接socket，并设置通用的连接参数
        :param sock: socket对象，默认None，会发起新的连接
        :param timeout: socket相应时间，单位秒
        :return: None
        """
        if sock:
            self.sock = sock #客户端socket连接
        else:

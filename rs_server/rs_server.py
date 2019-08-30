# -*- encoding: utf-8 -*-

import json
import socket
import thread
import Queue
import sys

#以下操作用于支持执行该文件
# root_path = __file__.split(r'\%s' % PROKECT_DIR_RESOURSE)
# sys.path.append(root_path[0])

#以下引用用于rs_client直接执行远程脚本
from rs_client import  RS_CODE , RSSocketBase , RS_SERVER_PORT
from elog import *
from dos import *
from data_tran import *
from tshark import *

# RS服务端，用于接收和处理来自客户端的消息，支持多用户同时连接
class RemoteshellServer:
    def __init__(self,host_info = None):
        """
        初始化server信息，默认自动采用本地大网IP
        :param host_info: 有效格式（host,port）
        """
        # 默认自动获取本地大网IP
        if not host_info:
            local_big_ip = aw_GetNetWorkIpAddress('100.|10.')
            host_info = (local_big_ip , RS_SERVER_PORT)
        self.host_addr = host_info #(host,port)
        self.svr_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.svr_status = None
        self.clients = {} #{addr: [sock,status , ...]},支持多客户端并发

    def StartServerListen(self):
        # 开启RS服务端监听
        self.svr_sock.bind(self.host_addr)
        self.svr_sock.listen(1)
        self.svr_status = True
        LogInfo('RS server %s is working...' % str(self.host_addr))
        while self.svr_status:
            try:
                _sock , _addr = self.svr_sock.accept()
            except Exception as ex:
                LogHint('RS server is stop!%s' %str(ex))
                self.svr_sock.close()
                break
            #释放无用缓存
            self._ReleaseBuff()
            # 按客户端IP：port分别起子线程，以支持多客户端并发
            client_info = '%s:%d' % _addr
            client = _ClientSocket(_addr)
            thread.start_new_thread(client.HandleClientMsg,(_sock,))

            #打印客户端连接情况，辅助定位
            client_keys = self.clients.keys()
            LogHint(client_keys)
            # LogHint(client_keys)

    def StopServer(self):
        self.svr_status = False
        # 释放socket资源
        for a in self.clients.keys():
            self.clients[a].CloseSocket()
        self.svr_sock.close()

    def _ReleaseBuff(self):
        # 释放无用内存
        for a in self.clients.keys():
            if not self.clients[a].status: #client的socket连接状态
                self.clients.pop(a)

    # RS server的底层客户端socket消息收发处理类
    class _ClientSocket(RSSocketBase):
        def __init__(self , addr_info):
            RSSocketBase.__init__(self , addr_info , log_level=HINT)

        def HandleClientMsg(self,sock):
            # 收发、处理客户端的socket消息
            self._ConnectSocket(sock)
            # 主线程顺序处理消息
            while self.status:
                try:
                    msg_req = self._msgpool_recv.get_nowait() # 从队列提取消息
                    # 处理接受的消息，并返回相应信息
                    msg_req = self.ExecuteMsg(msg_req)
                except Exception as e:
                    Sleep(0.2)
                    continue
            self._CloseSocket()

        def ExecuteMsg(self,msg_req):
            """
            处理接收到的消息，并发送响应消息给客户端
            :param msg_req: 客户端发来的消息
            :return: None
            """
            ret_code = RS_CODE.OK
            mtype = msg_req['msgtype']
            try:
                # 关闭socke
                if mtype == 'closesocket':
                    self.status = False
                    ret_info = ''
                # 执行DOS命令
                elif mtype == 'cmd':
                    doscmd = msg_req['msgdata']
                    # timeout = msg_req['timeout']
                    try:
                        ret_info = aw_RunDosCmd(doscmd)
                    except Exception as e:
                        ret_code = RS_CODE.ERR_CMD
                        ret_info = 'Fall: %s' % str(e)
                # 直接调用本工程的python脚本，支持多行模式
                elif mtype == 'script':
                    script = msg_req['msgdata']
                    #如果是单行、多行脚本模式
                    if isinstance(script,(unicode, str)):
                        scripts = [script]
                    else:
                        scripts = script
                    ret_info = 'OK'
                    try:
                        for line in scripts:
                            exec line
                    except Exception as e:
                        ret_code = RS_CODE.ERR_SCRIPT
                        ret_info = 'FALL: %s' % str(e) #str(unicode(e).encode('gbk'))
                else:
                    ret_code = RS_CODE.UNKNOWN
                    ret_info = 'unknown'
            except Exception as ex :
                ret_code = RS_CODE.ERR_SERVER
                ret_info = 'ERROR: ' + str(ex)
            #构造RS响应消息结构
            msg_centext = {
                'msgtype':mtype,
                'retcode':ret_code，
                'retinfo':ret_info
            }
            return msg_centext

if __name__ == '__main__':
    host_info = None
    portSrv = RS_SERVER_PORT
    #支持传参网段IP/网段、端口，示例1：‘python rs_server.py "151."60023'表示151.网段，60023端口
    if len(sys.argv) > 2:
        portSrv = int(sys.argv[2])
    if len(sys.argv)>1:
        addrSeg = sys.argv[1]
        ipLocal = aw_GetNetWorkIpAddress(addrSeg)
        host_info = (ipLocal , portSrv)

    # 关闭已经打开的RS Server或占用端口的进程
    aw_KillAllPidByPort(portSrv)

    # 启动RS Server
    rss = RemoteshellServer(host_info)
    rss.StartServerListen()

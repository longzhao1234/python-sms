#!/usr/bin/python
#encoding=utf-8
import urllib2
import urllib
import cookielib
import getpass
from optparse import OptionParser
from operator import itemgetter
import re,datetime,time
import json,traceback,re

def sasBrower(message,ismyself = True):
    loginurl = "http://f.10086.cn/huc/user/space/login.do?m=submit&fr=space"
    sendurl = "http://f.10086.cn/im/chat/toinputMsg.action?touserid=(your friend id)&amp;type=all"
    sendapiurl = "http://f.10086.cn/im/chat/sendShortMsg.action?touserid=(your friend id)"
    #sendapiurl = "http://f.10086.cn/im/chat/sendMsg.action?touserid=(your friend id)" #send message to fetion,not sms.
    indexurl = "http://f.10086.cn/im/index/index.action"
    sendmyselfapiurl = "http://f.10086.cn/im/user/sendMsgToMyselfs.action"
    try:
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        #opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
        data = urllib.urlencode({"mobilenum":"(your fetion account)","password":"(your fetion password)","m":"submit","fr":"space","backurl":"http://f.10086.cn/"})
        opener.open(loginurl,data)
        result = None
        if ismyself:
            opener.open(indexurl)
            msg = urllib.urlencode({"msg":message})
            result = opener.open(sendmyselfapiurl, msg).read()
            if "短信发送成功" in result:
                print "给自己发送短信成功！"
            else:
                print "遇到未知错误！"
        else:
            sendpage = opener.open(sendurl).read()
            csrftoken_value = re.findall(r'name="csrfToken"\s*?value="(.*?)"',sendpage,re.M)[0]
            data = urllib.urlencode({"backUrl":"","touchTitle":"","touchTextLength":"","msg":message,"csrfToken":csrftoken_value})
            result = opener.open(sendapiurl,data).read()
            if "发送消息成功" in result:
                print "给好友发送短信成功！"
            else:
                print "遇到未知错误！"
        return
    except Exception,e:
        print str(e)


def main():
    usage = "usage: %prog [ options ] arg"
    parser = OptionParser(usage)
    #aparser.add_option("-u","--user",dest="username",help="your sas username")
    #parser.add_option("-p","--pass",dest="password",help="your sas password")
    parser.add_option("-m","--message",dest="message",help="your message")
    (options, args) = parser.parse_args()
    if options.message:
        print "Waiting..."
        message = options.message
    else:
        print "Please input message."
        message = raw_input("message: ")
        #username = raw_input("username: ")
        #password = getpass.getpass("password: ")
        print "Thanks.Please Waiting..."
    html = sasBrower(message)
    
if __name__ == "__main__":
    main()

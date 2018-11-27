#coding:utf-8
from ..models import User

def authenticate(request,u,p):
    # 查询user表，失败返回试过
    # 成功，添加session，返回:用户类型,用户名
    try:
        user = User.objects.get(username=u)
        if user.password != p:
            return -1,'密码错误'
        # 放入session
        request.session['name'] = user.name
        request.session['username'] = user.username
        request.session['type'] =user.type
        return user.type,user.username
    except:
        #print("用户名不存在")
        return -1,'用户名不存在'

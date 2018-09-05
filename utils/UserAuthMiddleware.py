from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from backweb.models import User


class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        path = request.path
        if path == '/backweb/my_login/':
            return None
        if 'app' in path :
            return None
        if path == '/backweb/my_register/':
            return None

        session_id = request.COOKIES.get('session_id')
        #cookie中没有session说明没有登录



        if not session_id:
            return HttpResponseRedirect(reverse('backweb:my_login'))
        #获取同样sessions_id 的对象
        user = User.objects.filter(session_id=session_id).first()
        if not user:
            return HttpResponseRedirect(reverse('backweb:my_login'))
        try:
            pres = [pre.p_name for pre in user.r_u.r_p.all()]
            user.pres = pres
        except:
            pass
        request.user = user


        return None



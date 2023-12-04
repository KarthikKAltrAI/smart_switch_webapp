from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime

#apis

#register
class RegisterView(APIView):
    def post(self,request):
        serializor=UserSerializer(data=request.data)
        serializor.is_valid(raise_exception=True)
        serializor.save()
        return Response(serializor.data)
    

#Login
class LoginView(APIView):
    def post(self,request):
        email=request.data['email']
        password=request.data['password']

        user= User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User Not Found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        

        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()

        }

        token=jwt.encode(payload,'secret',algorithm='HS256')
        decode=jwt.decode(token, "secret", algorithms=["HS256"])

        response=Response()
        
        return Response({
            'jwt':token
        })
    



class UserView(APIView):
    def get(self,request):
        token=request.COOKIES.get('jwt')

        return Response(token)

        





    
    

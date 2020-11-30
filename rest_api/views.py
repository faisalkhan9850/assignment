from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from assignment.AuthBackend import AuthBackend
# Create your views here.


class SignupViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            if User.objects.filter(email=data.get('email')).exists():
                return Response({"detail": "Email already used"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = UserSerializer(data=data, many=False, context={"request": request})
            if serializer.is_valid():
                user = serializer.save()
                if user:
                    login(request, user, backend='assignment.AuthBackend.AuthBackend')
                    return Response(UserSerializer(user, many=False, context={"request": request}).data,
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    auth_obj = AuthBackend()

    def post(self, request):
        data = request.data
        if 'social_id' in data:
            social_id = data.get('social_id')
            queryset = User.objects.filter(social_id=social_id)
            # IF USER FOUND
            if queryset:
                queryset = User.objects.get(social_id=data.get('social_id'))
                queryset.is_active = True
                queryset.device_token = data.get('device_token')
                queryset.device_type = data.get('device_type')
                queryset.login_type = data.get('login_type')
                queryset.save()
                login(request, queryset, backend='assignment.AuthBackend.AuthBackend')
                return Response(UserSerializer(queryset, many=False, context={"request": request}).data,
                                status=status.HTTP_200_OK)
            else:
                if not data.get('email'):
                    return Response({"detail": "Email Required"}, status=status.HTTP_400_BAD_REQUEST)
                if User.objects.filter(email=data.get('email')).exists():
                    obj = User.objects.get(email=data.get('email'))
                    if obj.login_type == 'Gmail':
                        return Response({"detail": "You are already login with 'gmail' using this email. "
                                                   "Please try again with other account."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    elif obj.login_type == "Facebook":
                        return Response({"detail": "You are already login with 'facebook' using this email. "
                                                   "Please try again with other account."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"detail": "You are already login with this email. "
                                                   "Please try again with other account."},
                                        status=status.HTTP_400_BAD_REQUEST)
                serializer = UserSerializer(data=data, context={"request": request})
                if serializer.is_valid():
                    queryset = serializer.save()
                    queryset.device_token = data.get('device_token')
                    queryset.device_type = data.get('device_type')
                    queryset.login_type = data.get('login_type')
                    queryset.save()
                    login(request, queryset, backend='assignment.AuthBackend.AuthBackend')
                    return Response(UserSerializer(queryset, many=False,context={"request": request}).data,
                                    status=status.HTTP_200_OK)
                return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = User.objects.filter(email=request.data.get('email'))
            if queryset:
                queryset = self.auth_obj.authenticate(username=request.data.get('email'),
                                                      password=request.data.get('password'))
                if queryset:
                    login(request, queryset, backend='assignment.AuthBackend.AuthBackend')
                    # login(request, queryset)
                    queryset.device_type = request.data.get('device_type')
                    queryset.device_token = request.data.get('device_token')
                    queryset.login_type = "Email"
                    queryset.save()
                    return Response(UserSerializer(queryset, many=False, context={"request": request}).data,
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Incorrect Password'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Email not register'}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, pk,  *args, **kwargs):
        user = User.objects.get(id=pk)
        user.first_name = request.data.get("first_name")
        user.lastname = request.data.get("lastname")
        user.address = request.data.get("address")
        user.email = request.data.get("email")
        user.dob = request.data.get("dob")
        user.company = request.data.get("company")
        user.save()
        return Response(UserSerializer(user, many=False, context={"request": request}).data,
                        status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        user_obj = User.objects.all().exclude(role="Manager").order_by('-id')
        if user_obj:
            return Response(UserSerializer(user_obj, many=True, context={'request': request}).data,
                            status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No detail found'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, *args, **kwargs):
        user_obj = User.objects.get(id=pk)
        if user_obj:
            user_obj.delete()
            return Response({'detail': 'Successfully Deleted.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No detail found'}, status=status.HTTP_400_BAD_REQUEST)


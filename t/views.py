from rest_framework import viewsets

from t.models import User
from t.serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import time
import random
from django.shortcuts import render
import json
from t.genpassw import generate_random_password
from django.http import JsonResponse
import string
from .forms import UserForm
from rest_framework.decorators import action
from rest_framework.schemas import AutoSchema
from drf_yasg.utils import swagger_auto_schema
from drf_spectacular.utils import OpenApiParameter, extend_schema
from drf_yasg import openapi
from t.serializers import UserPhoneNameSerializer

user = User.objects.all()  
class UserViewSet(viewsets.ModelViewSet):

 queryset = User.objects.all()
 serializer_class = UserSerializer

 phone = openapi.Parameter('phone', openapi.IN_QUERY, description="Телефон", type=openapi.TYPE_INTEGER)
 password = openapi.Parameter('password', openapi.IN_QUERY, description="Пароль", type=openapi.TYPE_STRING)
 user_response = openapi.Response('response description', UserSerializer)
 userphone_response=openapi.Response('Ответ', openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Телефон'),
        'statusp': openapi.Schema(type=openapi.TYPE_INTEGER, description='Статус'),
        'random': openapi.Schema(type=openapi.TYPE_INTEGER, description='Код'),
        'text': openapi.Schema(type=openapi.TYPE_STRING, description='Ответ'),
    }
 ))
 userpass_response=openapi.Response('Ответ', openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Телефон'),
        'statusp': openapi.Schema(type=openapi.TYPE_INTEGER, description='Статус'),
        'text': openapi.Schema(type=openapi.TYPE_STRING, description='Ответ'),
    }
 ))

 @action(methods=['get','post'], detail=False) 
 def autorizpass(self,request):

    if request.method == "POST":
        
        ###
     
      
      
     phone1 = request.POST.get("phone").strip()
     name1 = request.POST.get("name")

     fl1 = user.filter(phone = phone1).exists()

     if fl1==False : 

      if len(phone1)!=10 :
       data = {'error': 'В номере телефона должно быть 10 цифр!'}
       
       data = {
            
                    'phone': phone1 ,
                    'name': name1,
                    'text': 'В номере телефона должно быть 10 цифр!'
                     }
        
       return render(request, "indexautor.html", context=data)

      if request.method == "POST":
         
           
         userform = UserForm(request.POST)
           
         if userform.is_valid():
            
            # получаем все объекты
            # user = User.objects.all()
            print(user.query)  
            fl = user.filter(phone = phone1).exists()
            print(fl)
            data={"phone": phone1}

            time.sleep(2)
            random_number = random.randint(1000, 9999)
            data={"phone": phone1,"statusp":1,"random": random_number,"text":"Телефон отсутствует в базе данных. Введите код:"}
            u1=User.objects.create(phone=phone1,name=name1, password=random_number, status=1)
            if u1.id>0 :
                
                data = {
                 'id': u1.id,
                 'phone': u1.phone ,
                 'code': u1.password,
                 'text': 'Введите код переданый в смс! (Для примера сейчас он в коде)'
                }
                
    
                return render(request, "indexcode.html", context=data)
            
            else:
                    
                    data = {
            
                    'phone': phone1 ,
                    'name': name1,
                    'text': 'Нельзя сохранить код в базу данных!'
                     }
        
                    return render(request, "indexautor.html", context=data)
        
                
    
            


            

         else:
            
            
            data = {
            
                    'phone': phone1 ,
                    'name': name1,
                    'text': 'В поле номер должны быть только цифры!'
                     }
        
            return render(request, "indexautor.html", context=data)
        ###
     else:
      
      u1 = user.filter(phone = phone1)

      if u1[0].status==2 :
    
        data = {
            'id': u1[0].id,
            'phone': u1[0].phone ,
            'password': u1[0].password,
            'name': u1[0].name
        }
    
        return render(request, "profileuserpassw.html", context=data)
      else:

        time.sleep(2)
        random_number = random.randint(1000, 9999)        
        u1[0].password = random_number
        u1[0].save(update_fields=["password"])

        data = {
            'id': u1[0].id,
            'phone': u1[0].phone ,
            'code': u1[0].password,
            'text': 'Введите код переданый в смс! (Для примера сейчас он в коде)'
        }
        
                
    
        return render(request, "indexcode.html", context=data)     
    else:    
        return render(request, "indexautor.html")

 @action(methods=['post'], detail=False) 
 def postupdatepass(self,request):
  
    phone1 = request.POST.get("phone")
    password1 = request.POST.get("password")
    name1 = request.POST.get("name1")
    newpassword1 = request.POST.get("newpassword").strip() 
    print(name1)

    if len(newpassword1)<6 :
       
        data = {
            
            'phone': phone1 ,
            'password': password1,
            'name1': name1,
            'text': 'Пароль не может быть меньше 6 символов!'
        }
        
        return render(request, "updatepassw.html", context=data)

    fl1 = user.filter(phone = phone1).exists()
    if fl1==False :
        
        data = {
            
            'phone': phone1 ,
            'password': password1,
            'name1': name1,
            'text': 'Нет такого телефона!'
        }
        
        return render(request, "updatepassw.html", context=data)
    
    fl1 = user.filter(phone = phone1,password=password1).exists()
    if fl1==False :
        
        data = {
            
            'phone': phone1 ,
            'password': password1,
            'name1': name1,
            'text': 'Нет такого пароля старого!'
        }
        
        return render(request, "updatepassw.html", context=data)
    
    u1 = user.filter(phone = phone1,password=password1)

    is_digit_present = any(character.isdigit() for character in newpassword1)
    if is_digit_present==False :
        
        data = {
            
            'phone': phone1 ,
            'password': password1,
            'name1': name1,
            'text': 'В пароле должно быть число!'
        }
        
        return render(request, "updatepassw.html", context=data)
    
    is_alpha_present = any(character.isalpha() for character in newpassword1)
    if is_alpha_present==False :
        
        data = {
            
            'phone': phone1 ,
            'password': password1,
            'name1': name1,
            'text': 'В пароле должна быть буква!'
        }
        
        return render(request, "updatepassw.html", context=data)
    
    is_spec=any(char in ".,:;!_*-+()/#¤%&@$^" for char in newpassword1)
    if is_spec==False :
        
        data = {
            
            'phone': phone1 ,
            'password': password1,
            'name1': name1,
            'text': 'В пароле должен быть спецсимвол!'
        }
        
        return render(request, "updatepassw.html", context=data)

    u2 = User.objects.get(phone=phone1)
    u2.password = newpassword1
    u2.save(update_fields=["password"])
    if u2.id>0 :
        data = {
            
            'phone': phone1 ,
            'password': password1,
            'name': name1,
            'text': 'Новый пароль успешно сохранён!'
        }
        
        return render(request, "profileuserpassw.html", context=data)
    else:
        
        data = {
            
            'phone': phone1 ,
            'password': password1,
            'name1': name1,
            'text': 'Нельзя сохранить пароль в базу данных!'
        }
        
        return render(request, "updatepassw.html", context=data)
    

 @action(methods=['post'], detail=False) 
 def updatepass(self,request):
  
    
  
  phone1 = request.POST.get("phone")
  password1 = request.POST.get("password")
  name1 = request.POST.get("name1")
  print(name1)
  if 'update' in request.POST:  
    data = {
            'id': request.POST.get("id"),
            'phone': phone1 ,
            'password': password1,
            'name1': name1
    }
    # print(data)
        
    return render(request, "updatepassw.html", context=data)
  else: 

    u1 = user.filter(password=password1)
    ua = []
   
    for obj in u1:
        ua += [obj.name]
        
    

    data = {
            'id': request.POST.get("id"),
            'phone': phone1 ,
            'password': password1,
            'name': name1,
            "users": ua
    }
    
        
    return render(request, "profileuserpassw.html", context=data)
    

 @action(methods=['post'], detail=False) 
 def autoriz(self,request):
  
    
    phone1 = request.POST.get("phone")
    password1 = request.POST.get("code")
    
    fl1 = user.filter(phone = phone1,status=1).exists()
    if fl1==False :
        
        data = {
            'id': 0,
            'phone': phone1 ,
            'code': password1,
            'text': 'Нет такого телефона! Пройдите авторизацию!'
        }
        
        return render(request, "indexcode.html", context=data)
    
    fl1 = user.filter(phone = phone1,password=password1,status=1).exists()
    if fl1==False :
        
        data = {
            'id': 0,
            'phone': phone1 ,
            'code': password1,
            'text': 'Нет такого кода для заданного телефона!'
        }
        return render(request, "indexcode.html", context=data)
      

    random_number =generate_random_password(6,3,2,1)
    u2 = User.objects.get(phone=phone1)
    u2.password = random_number
    u2.status=2
    u2.save(update_fields=["password","status"])
    if u2.id>0 :
        
        data = {
            'id': u2.id,
            'phone': u2.phone ,
            'password': u2.password,
            'name': u2.name,
            'text': 'Получен пароль для входа. Авторизация закончена!'
        }
    
        return render(request, "index.html", context=data)
    else:
           
        data = {
            'id': 0,
            'phone': phone1 ,
            'code': password1,
            'text': 'Нельзя сохранить пароль в базу данных!'
        }
        return render(request, "indexcode.html", context=data)
    
    
    
        
 
 @action(methods=['post'], detail=False) 
 def profilepost(self,request):
  
  if 'reset' in request.POST:  
    data = {
            'id': 0,
            'phone': '' ,
            'password': '',
            'text': ''
        }
    return render(request, "index.html", context=data)
  else:
    
    phone1 = request.POST.get("phone")
    password1 = request.POST.get("password")
    
    fl1 = user.filter(phone = phone1).exists()
    if fl1==False :
        
        data = {
            'id': 0,
            'phone': phone1 ,
            'password': password1,
            'text': 'Нет такого телефона! Пройдите авторизацию!'
        }
        
        return render(request, "index.html", context=data)
    
    fl1 = user.filter(phone = phone1,password=password1).exists()
    if fl1==False :
        
        data = {
            'id': 0,
            'phone': phone1 ,
            'password': password1,
            'text': 'Нет такого пароля!'
        }
        return render(request, "index.html", context=data)
    u1 = user.filter(phone = phone1,password=password1)

    if u1[0].status==2 :
    
        data = {
            'id': u1[0].id,
            'phone': u1[0].phone ,
            'password': u1[0].password,
            'name': u1[0].name
        }
    
        return render(request, "profileuserpassw.html", context=data)
    else:

        time.sleep(2)
        random_number = random.randint(1000, 9999)        
        u1[0].password = random_number
        u1[0].save(update_fields=["password"])

        data = {
            'id': u1[0].id,
            'phone': u1[0].phone ,
            'code': u1[0].password,
            'text': 'Введите код переданый в смс! (Для примера сейчас он в коде)'
        }
        
                
    
        return render(request, "indexcode.html", context=data)
        

 
 @action(methods=['get','post'], detail=False) 
 def index(self,request):

    if request.method == "POST":
        
        phone1 = request.POST.get("phone", "-1")

        # получаем все объекты
        user = User.objects.all()
        print(user.query)  
        fl = user.filter(phone = phone1).exists()
        print(fl)
        data={"phone": phone1}

        if fl :
            return HttpResponse(f"<h2>Телефон: {phone1}  найден</h2>") 
            return HttpResponse("Произошла ошибка", status=400, reason="В номере телефона должны быть только цифры ")
        else:
            time.sleep(2)
            random_number = random.randint(1000, 9999)
            data={"phone": phone1,"fl":1,"random": random_number}
            return render(request, "index.html", context=data)
    else:    
        return render(request, "index.html")
        

 @swagger_auto_schema(request_body=openapi.Schema( 
    type=openapi.TYPE_OBJECT, 
    properties={
        'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Телефон'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Старый пароль'),
        'newpassword': openapi.Schema(type=openapi.TYPE_STRING, description='Новый пароль'),
    }),responses={200:userpass_response})
 @action(methods=['post'], detail=False) 
 @csrf_exempt
 def postupdatepassword(self,request): 

    if len(request.body) == 0 :
        phone1 = request.POST.get("phone")
        password1 = request.POST.get("password")
        newpassword1 = request.POST.get("newpassword").strip()
    else :
      
      body = request.body
      data1 = json.loads(body)
      
      phone1 = data1['phone'].strip()
      password1 = data1['password']
      newpassword1 = data1['newpassword']

    if len(newpassword1)<6 :
       data = {'error': 'Пароль не может быть меньше 6 символов!'}
       return JsonResponse(data, status=400)
    fl1 = user.filter(phone = phone1).exists()
    if fl1==False :
        data = {'error': 'Нет такого телефона!'}
        return JsonResponse(data, status=400)
    fl1 = user.filter(phone = phone1,password=password1).exists()
    if fl1==False :
        data = {'error': 'Нет такого пароля старого!'}
        return JsonResponse(data, status=400)
    u1 = user.filter(phone = phone1,password=password1)

    is_digit_present = any(character.isdigit() for character in newpassword1)
    if is_digit_present==False :
        data = {'error': 'В пароле должно быть число!'}
        return JsonResponse(data, status=400)
    
    is_alpha_present = any(character.isalpha() for character in newpassword1)
    if is_alpha_present==False :
        data = {'error': 'В пароле должна быть буква!'}
        return JsonResponse(data, status=400)
    
    is_spec=any(char in ".,:;!_*-+()/#¤%&@$^" for char in newpassword1)
    if is_spec==False :
        data = {'error': 'В пароле должен быть спецсимвол!'}
        return JsonResponse(data, status=400)

    u2 = User.objects.get(phone=phone1)
    u2.password = newpassword1
    u2.save(update_fields=["password"])
    if u2.id>0 :
        data={"phone": phone1,"statusp":4,"text":"Пароль у телефона заменён успешно!"}
        return JsonResponse(data, status=200)
    else:
        data = {'error': 'Нельзя сохранить пароль в базу данных!'}
        return JsonResponse(data, status=400)

 @swagger_auto_schema(method='get', manual_parameters=[password])     
 @action(methods=['get'], detail=False)
 def getuserpassw(self,request): 
    password1 = request.GET.get("password")
    fl1 = user.filter(password=password1).exists()
    if fl1==False :
        data = {'error': 'Нет такого пароля!'}

    u1 = user.filter(password=password1)
    ua = []
   
    for obj in u1:
        ua += [{
            'id': obj.id,
            'phone': obj.phone ,
            'password': obj.password,
            'name': obj.name
        }]
    data = {"user": ua}
    return JsonResponse(data)    

 @swagger_auto_schema(method='get', manual_parameters=[phone,password])
 @action(methods=['get'], detail=False)
 def profileuserpassw(self,request):    
    phone1 = request.GET.get("phone")
    password1 = request.GET.get("password")
    fl1 = user.filter(phone = phone1).exists()
    if fl1==False :
        data = {'error': 'Нет такого телефона!'}
        return JsonResponse(data, status=400)
    fl1 = user.filter(phone = phone1,password=password1).exists()
    if fl1==False :
        data = {'error': 'Нет такого пароля!'}
        return JsonResponse(data, status=400)
    u1 = user.filter(phone = phone1,password=password1)
    
    data = {"user": {
            'id': u1[0].id,
            'phone': u1[0].phone ,
            'password': u1[0].password,
            'name': u1[0].name
        }}
    print(data)
    return JsonResponse(data, status=200)


 @swagger_auto_schema(method='get', manual_parameters=[phone])  
 @action(methods=['get'], detail=False)
 def profileuser(self,request):   
  
    phone1 = request.GET.get("phone")
    fl1 = user.filter(phone = phone1).exists()
    if fl1==False :
        data = {'error': 'Нет такого телефона!'}
        return JsonResponse(data, status=400)
    u1 = user.filter(phone = phone1)
    data = {"user": {
            'id': u1[0].id,
            'phone': u1[0].phone ,
            'password': u1[0].password,
            'name': u1[0].name
        }}
    
    return JsonResponse(data)

 @swagger_auto_schema(request_body=openapi.Schema( 
    type=openapi.TYPE_OBJECT, 
    properties={
        'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Телефон'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль'),
    }),responses={200:userpass_response})
 @action(methods=['post'], detail=False) 
 @csrf_exempt    
 def postafterpassword(self,request):    

    if len(request.body) == 0 :
        phone1 = request.POST.get("phone")
        password1 = request.POST.get("password")
    else :
      
      body = request.body
      data1 = json.loads(body)
      
      phone1 = data1['phone'].strip()
      password1 = data1['password']

    fl1 = user.filter(phone = phone1).exists()
    if fl1==False :
        data = {'error': 'Нет такого телефона!'}
        return JsonResponse(data, status=400)
    
    # Мгновенная проверка
    is_digit_present = any(character.isdigit() for character in password1)
    if is_digit_present==False :
        data = {'error': 'В пароле должно быть число!'}
        return JsonResponse(data, status=400)
    
    is_alpha_present = any(character.isalpha() for character in password1)
    if is_alpha_present==False :
        data = {'error': 'В пароле должна быть буква!'}
        return JsonResponse(data, status=400)
    
    is_spec=any(char in ".,:;!_*-+()/#¤%&@$^" for char in password1)
    if is_spec==False :
        data = {'error': 'В пароле должен быть спецсимвол!'}
        return JsonResponse(data, status=400)

    u2 = User.objects.get(phone=phone1)
    u2.password = password1
    u2.save(update_fields=["password"])
    if u2.id>0 :
        data={"phone": phone1,"statusp":4,"text":"Пароль у телефона введён успешно!"}
        return JsonResponse(data, status=200)
    else:
        data = {'error': 'Нельзя сохранить пароль в базу данных!'}
        return JsonResponse(data, status=400)

 @swagger_auto_schema(request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Телефон'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль'),
    }),responses={200:userpass_response})
 @action(methods=['post'], detail=False) 
 @csrf_exempt    
 def postpassword(self,request):    

    if len(request.body) == 0 :
        phone1 = request.POST.get("phone")
        password1 = request.POST.get("password")
    else :
      
      body = request.body
      data1 = json.loads(body)
      
      phone1 = data1['phone'].strip()
      password1 = data1['password']

    fl1 = user.filter(phone = phone1).exists()
    if fl1==False :
        data = {'error': 'Нет такого телефона!'}
        return JsonResponse(data, status=400)
    fl = user.filter(phone = phone1,password=password1,status=2).exists()
    if fl :
        data={"phone": phone1,"statusp":3,"text":"Телефон есть в базе данных. Регистрация прошла успешно!"}
        return JsonResponse(data, status=200)
    else:
        data = {'error': 'Нет такого пароля для заданного телефона!'}
        return JsonResponse(data, status=400)

 def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password 
        
 @swagger_auto_schema(request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Телефон'),
        'code': openapi.Schema(type=openapi.TYPE_STRING, description='Код'),
    }),responses={200:userphone_response})
 @action(methods=['post'], detail=False) 
 @csrf_exempt
 def postcode(self,request):

    if len(request.body) == 0 :
        phone1 = request.POST.get("phone")
        code = request.POST.get("code")
    else :
      
      body = request.body
      data1 = json.loads(body)
      
      phone1 = data1['phone'].strip()
      code = data1['code']    

    fl1 = user.filter(phone = phone1).exists()
    if fl1==False :
        data = {'error': 'Нет такого телефона!'}
        return JsonResponse(data, status=400)
    fl = user.filter(phone = phone1,password=code,status=1).exists()
    if fl :
        # random_number = generate_password(6)
        random_number =generate_random_password(6,3,2,1)
        data={"phone": phone1,"statusp":2,"random": random_number,"text":"Телефон есть в базе данных. Введите пароль:"}
        u2 = User.objects.get(phone=phone1)
        u2.password = random_number
        u2.status=2
        u2.save(update_fields=["password","status"])
        if u2.id>0 :
            return JsonResponse(data, status=200)
        else:
            data = {'error': 'Нельзя сохранить пароль в базу данных!'}
            return JsonResponse(data, status=400)
    else:
        data = {'error': 'Нет такого кода для заданного телефона!'}
        return JsonResponse(data, status=400)    

 

 
 @swagger_auto_schema(methods=['post'],request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Телефон'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользователя'),
    }),responses={200:userphone_response})
 @action(methods=['post'], detail=False)    
 @csrf_exempt 
 def postphone(self,request):
    # получаем из данных запроса POST отправленные через форму данные

    
    
    if len(request.body) == 0 :
      
      
      phone1 = request.POST.get("phone").strip()
      name1 = request.POST.get("name")
    else :
      

      body = request.body
      data1 = json.loads(body)
      
      phone1 = data1['phone'].strip()
      name1 = data1['name']    

    if len(phone1)!=10 :
       data = {'error': 'В номере телефона должно быть 10 цифр!'}
       return JsonResponse(data, status=400)

    if request.method == "POST":
        if len(request.body) == 0 :
           
           userform = UserForm(request.POST)
        else :
           
           body = request.body
           data1 = json.loads(body)
           userform = UserForm(data1)     
        if userform.is_valid():
            
            # получаем все объекты
            # user = User.objects.all()
            print(user.query)  
            fl = user.filter(phone = phone1).exists()
            print(fl)
            data={"phone": phone1}

            if fl :

                fl1 = user.filter(phone = phone1,status=1).exists()
                u1 = user.filter(phone = phone1)
                if fl1 :
                                        
                    #Здесь посылается смс на телефон, random передаю, для теста, чтобы знать какой код вводить, а так не надо его здесь возвращать
                    data={"phone": phone1,"statusp":1,"random": u1[0].password,"text":"Телефон есть в базе данных. Регистрация до конца не прошла. Введите код:"}
                    
                else :
                    
                    #Здесь пользователь должен после этого ввести пароль, random передаю, для теста, чтобы знать какой пароль вводить, а так не надо его здесь возвращать
                   data={"phone": phone1,"statusp":2,"random": u1[0].password,"text":"Телефон есть в базе данных. Введите пароль:"}
                
                return JsonResponse(data, status=200) 
        
            else:
                time.sleep(2)
                random_number = random.randint(1000, 9999)
                data={"phone": phone1,"statusp":1,"random": random_number,"text":"Телефон отсутствует в базе данных. Введите код:"}
                u1=User.objects.create(phone=phone1,name=name1, password=random_number, status=1)
                if u1.id>0 :
                    return JsonResponse(data, status=200)
                else:
                    data = {'error': 'Нельзя сохранить код в базу данных!'}
                    return JsonResponse(data, status=400)

        else:
            
            data = {'error': 'В поле номер должны быть только цифры!'}
            return JsonResponse(data, status=400)

    

     


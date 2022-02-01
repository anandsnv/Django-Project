import json
import os
import shutil
import datetime


from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from facedectapi.maskdetection.face import embedding, train, face_match
from facedectapi.maskdetection.yolov5.main import out
from facedectapi.models import User, Log

basedir = os.path.abspath(os.path.dirname(__file__))

@csrf_exempt
def valid(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode("utf-8"))
            eid = data.get('eid')
            mob = data.get('mob')
            userexist = False
            if mob or eid:
                if User.objects.filter(mob=mob).exists():
                    userexist = True
                else:
                    userexist = False
            return JsonResponse({'userExist': userexist})
    except:
        return JsonResponse('Format not valid')

@csrf_exempt
def insert(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.POST.get('data'))
            mob = data.get('mob')
            eid = data.get('eid')
            name = data.get('name')
            email = data.get('email')
            image_file = request.FILES.getlist('imgs')
            filedest = os.path.join(basedir, 'Images')
            tempdest = os.path.join(basedir, 'Embed')
            new_dir = os.path.join(filedest, mob)
            embed_dir = os.path.join(tempdest, mob)
            registrationsuccess = False
            if image_file[0] and image_file[1]:
                new_user = User(mob=mob, eid=eid, name=name, email=email)
                new_user.save()
                os.mkdir(new_dir)
                shutil.rmtree(tempdest)
                default_storage.save(os.path.join(new_dir, "image1.jpg"), ContentFile(image_file[0].read()))
                default_storage.save(os.path.join(new_dir, "image2.jpg"), ContentFile(image_file[1].read()))
                shutil.copytree(new_dir, embed_dir)
                embedding(tempdest)
                registrationsuccess = True
            return JsonResponse({'registrationSuccess': registrationsuccess})
        except:
            return JsonResponse({'registrationSuccess': False})


@csrf_exempt
def identify(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.POST.get('data'))
            mask = data.get('mask')
            sid = data.get('sid')
            image_file = request.FILES.get('imagefile')
            result = {}
            currentDT = datetime.datetime.now()
            DTstring = currentDT.strftime("%Y%m%d%H%M%S")
            # try:
            filedest = os.path.join(basedir, 'temp')
            image_location = os.path.join(filedest, DTstring+".jpg")
            default_storage.save(image_location, ContentFile(image_file.read()))
            facedetectresult = face_match(image_location, "facedectapi/maskdetection/data.pt")
            if mask:
                maskdetectresult = out(image_location)
                maskresultlist = maskdetectresult.split(' ')
                if maskresultlist[0] == 'mask':
                    mask_dict = {"maskPresent": True, "MDConfidence": maskresultlist[1]}
                elif maskresultlist[0] == 'nomask':
                    mask_dict = {"maskPresent": False, "MDConfidence": maskresultlist[1]}
                result.update(mask_dict)
            row = User.objects.get(mob=facedetectresult[0])
            user_dict = {"User": {"name": row.name, "empId": row.eid, "email": row.email, "phoneNo": row.mob}}
            face_dict = {"FIDDistance": facedetectresult[1]}
            sentid = {"sid": sid}
            result.update(sentid)
            result.update(user_dict)
            result.update(face_dict)
            new_image_location = os.path.join(filedest, "%s_%1.3f_%s.jpg" % (DTstring, facedetectresult[1], row.mob))
            os.rename(image_location, new_image_location)
            return JsonResponse(result)
        except:
          return JsonResponse({'IsUser': False})


@csrf_exempt
def log(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
            mob = data.get('mob')
            mask = data.get('mask')
            temp = data.get('temp')
            access = data.get('access')
            date = data.get('date')
            person = User.objects.get(mob=mob)
            log_time = datetime.datetime.strptime(date,'%d/%m/%Y %H:%M:%S')
            new_log = Log(person=person, mask=mask, temp=temp, access=access, logtime=log_time)
            new_log.save()
            return JsonResponse({'transactionSuccess': True})
        except:
             return JsonResponse({'transactionSuccess': False})

@csrf_exempt
def traine(request):
    try:
        if request.method == 'POST':
            filedest = os.path.join(basedir, 'images')
            train(filedest)
            return JsonResponse({'transactionSuccess': True})
    except:
        return JsonResponse({'transactionSuccess': False})
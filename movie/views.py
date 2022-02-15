from django.shortcuts import render,redirect
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import ExtendedUser,Suggestion,Group,GroupMember
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# Create your views here.

def index(request):
    dict={'fresh':True}
    return render(request,'Filmatopedia/index.html',dict)

def about(request):
    dict = {'fresh': True}
    return render(request,'Filmatopedia/about.html',dict)

#@login_required(login_url='/index')
def news(request):
    if request.user.is_authenticated:
        pass
    else:
        return HttpResponse("<h1>Bad Request for a Page with out Login</h1>")
    url = 'https://indianexpress.com/section/entertainment/hollywood/'
    r = requests.get(url)
    htmlcontent = r.content

    soup = BeautifulSoup(htmlcontent, 'html.parser')
    params=[]
    heading = soup.find_all('div', class_='articles')
    for item in heading:
        tt=[]
        temp = item.find('div', class_='title')
        title = temp.find('a')
        tt.append(str(title.get_text()))

        temp1 = item.find('div', class_='snaps').find('a')
        link = temp1.get('href')
        tt.append(str(link))

        temp2 = item.find('div', class_='snaps').find('a')
        img = temp2.find('img').get('data-lazy-src')
        tt.append(str(img))

        summary = item.find('p')
        tt.append(str(summary.get_text()))

        params.append(tt)

    dict={'params':params}
    return render(request,'Filmatopedia/filmnews.html',dict)

def signup(request):
    if request.method=='POST':
        username=request.POST['susername']


        val=User.objects.filter(username=username)
        if val.count()==0:
            username=str(username).lower()
            name = request.POST['name']
            password = request.POST['spassword']
            phone = request.POST['phone']
            image = request.FILES['imggg']
            user=User.objects.create_user(username=username,password=password)
            newuser=ExtendedUser(name=name,profile_pic=image,phone=phone,user=user)
            newuser.save()
            messages.success(request,'Congratulations!! Your Account in Filmatopedia has been created Succesfully')
            return redirect('/')
        else:
            messages.error(request,'Username Already Taken. Please use another Username')
            return redirect('/')
    else:
        return HttpResponse("<h1>Page Not Found.</h1>")

    return render(request,'Filmatopedia/about.html')

def login_req(request):
    if request.method=='POST':
        username=request.POST['lusername']
        username=str(username).lower()
        password=request.POST['lpassword']

        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Successfully logged In')
            return redirect('/')

        else:
            messages.error(request,'Username or password is wrong')
            return redirect('/')
    else:
        return HttpResponse("<h1>Page Not Found.</h1>")


@login_required(login_url='/')
def logout_req(request):
    logout(request)
    messages.success(request,'Successfully Logged Out')
    return redirect('/')

def postsuggestion(request):
    if request.user.is_authenticated:
        extndusr = ExtendedUser.objects.filter(user=request.user).first()
        grpmem = GroupMember.objects.filter(user=extndusr)
        grpmems = []

        for j in grpmem:
            grpmems.append(j.group)
        return render(request, 'Filmatopedia/postsuggestion.html', {'suggestion': True,'param2': grpmems})
    else:
        return HttpResponse('<h1>Page not Found</h1>')

def addsuggestion(request):
    if request.user.is_authenticated and request.method=='POST':
        title=request.POST['title']
        language=request.POST['language']
        type=request.POST['type']
        group=request.POST['grp']
        lst=group.split(',')
        grp_name=lst[0]
        admin_user=lst[1]
        date=timezone.now()
        req=0

        user=User.objects.get(username=admin_user)
        myextndusradmin = ExtendedUser.objects.filter(user=user).first()
        gr=Group.objects.filter(admin_user=myextndusradmin,group_name=grp_name).first()

        myextndusr=ExtendedUser.objects.filter(user=request.user).first()
        sugg=Suggestion(user=myextndusr,title=title,language=language,type=type,date=date,req=req,group=gr)
        sugg.save()
        messages.success(request,'Suggestion Posted Successfully')
        return redirect('/')
    else:
        messages.error(request,'Please Log in First')
        return HttpResponse("<h1>Page Not Found</h1>")


def reqsuggestion(request):
    if request.user.is_authenticated and request.method == 'POST':
        type=request.POST['type']
        language=request.POST['lang']
        title='***'
        group = request.POST['grp1']
        lst = group.split(',')
        grp_name = lst[0]
        admin_user = lst[1]
        date = timezone.now()
        req = 1

        user = User.objects.get(username=admin_user)
        myextndusradmin = ExtendedUser.objects.filter(user=user).first()
        gr = Group.objects.filter(admin_user=myextndusradmin, group_name=grp_name).first()

        myextndusr = ExtendedUser.objects.filter(user=request.user).first()
        sugg = Suggestion(user=myextndusr, title=title, language=language, type=type, date=date, req=req, group=gr)
        sugg.save()

        messages.success(request,'Request Submitted Succesfully')
        return redirect('/')

    else:
        return HttpResponse("<h1>Bad Request to the Server</h1>")

def getsuggestion(request):
    if request.user.is_authenticated and request.method=='POST':
        group = request.POST['grp3']
        lst = group.split(',')
        grp_name = lst[0]
        admin_user = lst[1]

        myextndusr = ExtendedUser.objects.filter(user=User.objects.get(username=admin_user)).first()
        grp=Group.objects.filter(admin_user=myextndusr,group_name=grp_name).first()

        val=[]
        data=Suggestion.objects.filter(group=grp)
        num=Suggestion.objects.filter(group=grp).count()
        index=-1
        print(num)
        while( (index+2)<=(num-1) ):
            temp=[]
            index+=1
            temp.append(data[index])
            index+=1
            temp.append(data[index])
            val.append(temp)

        if num%2!=0:
            odd=True
            temp=data[num-1]
            d={'value':val,'odd':odd,'temp':temp,'name':grp_name}
            return render(request,'Filmatopedia/getsuggestion.html',d)
        else:
            odd=False
            d={'value':val,'odd':odd,'name':grp_name}
            return render(request, 'Filmatopedia/getsuggestion.html', d)


    else:
        return HttpResponse('<h1> Page Not Found</h1>')


# Editing Stuffs
def profile(request):
    if request.user.is_authenticated:
        extnduser=ExtendedUser.objects.filter(user=request.user).first()
        username=request.user.username
        name=extnduser.name
        phone=extnduser.phone
        img=extnduser.profile_pic

        dict={'username':username,'name':name,'profile':True,'phone':phone,'img':img}
        return render(request, 'Filmatopedia/profile.html', dict)
    else:
        return HttpResponse('<h1>Page not Found</h1>')


def editprofile(request):
    if request.user.is_authenticated:
        extnduser = ExtendedUser.objects.filter(user=request.user).first()
        name = extnduser.name
        phone = extnduser.phone
        img=extnduser.profile_pic

        dict = {'name': name, 'editprofile': True, 'phone': phone,'img':img}
        return render(request, 'Filmatopedia/profile.html',dict)
    else:
        return HttpResponse('<h1>Page not Found</h1>')

def editpassword(request):
    if request.user.is_authenticated:
        extnduser = ExtendedUser.objects.filter(user=request.user).first()
        img = extnduser.profile_pic
        return render(request, 'Filmatopedia/profile.html',{'editpassword':True,'img':img})
    else:
        return HttpResponse('<h1>Page not Found</h1>')

def editpic(request):
    if request.user.is_authenticated:
        extnduser = ExtendedUser.objects.filter(user=request.user).first()
        img = extnduser.profile_pic
        return render(request, 'Filmatopedia/profile.html', {'editpic': True,'img':img})
    else:
        return HttpResponse('<h1>Page not Found</h1>')

def changeprofile(request):
    if request.user.is_authenticated:
        name=request.POST['name']
        phone=request.POST['phone']

        extndusr=ExtendedUser.objects.filter(user=request.user).update(name=name,phone=phone)
        return redirect('/profile')
    else:
        return HttpResponse('<h1>Page Not Found</h1>')

def changepic(request):
    if request.user.is_authenticated and request.method=='POST':
        pic=request.FILES['picss']
        print(pic)

        extndusr=ExtendedUser.objects.filter(user=request.user).first()
        extndusr.profile_pic=pic
        extndusr.save()

        return redirect('/profile')
    else:
        return HttpResponse('<h1>Page Not Found</h1>')

def changepassword(request):
    if request.user.is_authenticated and request.method=='POST':
        current=request.POST['op']
        np=request.POST['np']

        user=User.objects.get(username=request.user.username)
        check=user.check_password(current)
        if check:
            user.set_password(np)
            user.save()
            messages.success(request,'Password Updated Succesfully')
            return redirect('/')
        else:
            messages.error(request,"Old password did't match")
            return redirect('/editpassword')
    else:
        return HttpResponse('<h1>Page Not Found</h1>')


# Group Stufs
def suggestion(request):
    if request.user.is_authenticated:
        extndusr = ExtendedUser.objects.filter(user=request.user).first()
        grp=Group.objects.filter(admin_user=extndusr)
        grpmem=GroupMember.objects.filter(user=extndusr)
        groups=[]
        grpmems=[]
        for i in grp:
            groups.append(i.group_name)
        for j in grpmem:
            grpmems.append(j.group)
        return render(request,'Filmatopedia/index.html',{'suggestion':True,'param':groups,'param2':grpmems})
    else:
        return HttpResponse('<h1>Page not Found</h1>')

def creategroup(request):
    if request.user.is_authenticated and request.method=='POST':
        grpname=request.POST['grpname']
        extndusr = ExtendedUser.objects.filter(user=request.user).first()
        if Group.objects.filter(admin_user=extndusr,group_name=grpname).exists():
            messages.error(request,'The same Group Name already exists, please choose another one.')
            return redirect('/suggestion')
        else:
            grp=Group(admin_user=extndusr,group_name=grpname,date=timezone.now())
            grp.save()
            grpmember=GroupMember(user=extndusr,group=grp)
            grpmember.save()
            messages.success(request,'Group created Succesfully.')
            return redirect('/suggestion')
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

def addmember(request):
    if request.user.is_authenticated and request.method=='POST':
        usrname=request.POST['username']
        usrname=str(usrname).lower()
        grpname=request.POST['grp']

        #Check usrname present or not in Extended USER
        try:
            usr = User.objects.get(username=usrname)
        except Exception as e:
            messages.error(request, 'Cannot add member because Invalid Username')
            return redirect('/suggestion')
        n = User.objects.filter(username=usrname).count()
        grpss=Group.objects.filter(admin_user=ExtendedUser.objects.filter(user=request.user).first(),group_name=grpname).first()
        gm=GroupMember.objects.filter(user=ExtendedUser.objects.filter(user=User.objects.get(username=usrname)).first(),group=grpss).first()


        if n!=0:
            if gm is not None:
                messages.error(request, 'Member Already Present')
                return redirect('/suggestion')
            else:

                extndusr = ExtendedUser.objects.filter(user=usr).first()
                extndusr2 = ExtendedUser.objects.filter(user=request.user).first()
                grpmembr=GroupMember(user=extndusr,group=Group.objects.filter(admin_user=extndusr2,group_name=grpname).first())
                grpmembr.save()
                messages.success(request,'Member added Successfully.')
                return redirect('/suggestion')
        else:
            messages.error(request,'Cannot add member because Invalid Username')
            return redirect('/suggestion')
    else:
        return HttpResponse('<h1>Page not Found</h1>')

def groups(request):
    if request.user.is_authenticated:
        extndusr=ExtendedUser.objects.filter(user=request.user).first()
        grpmember=GroupMember.objects.filter(user=extndusr)

        extndusr = ExtendedUser.objects.filter(user=request.user).first()
        grp = Group.objects.filter(admin_user=extndusr)
        grpmem = GroupMember.objects.filter(user=extndusr)
        group = []
        grpmems = []
        for i in grp:
            group.append(i.group_name)
        for j in grpmem:
            grpmems.append(j.group)

        dict={'suggestion':True,'param':group,'param2':grpmems,'grps':grpmember}

        return render(request,'Filmatopedia/groups.html',dict)
    else:
        return HttpResponse("<h1>Page Not Found</h1>")

def groupinfo(request):
    if request.user.is_authenticated and request.method=='POST':
        admin_user,group_name=request.POST['group'].split(',')

        extndsusr1=ExtendedUser.objects.filter(user=User.objects.get(username=admin_user)).first()

        group=Group.objects.filter( admin_user=extndsusr1,group_name=group_name ).first()
        grpmem1=GroupMember.objects.filter(group=group)

        extndusr = ExtendedUser.objects.filter(user=request.user).first()
        grp = Group.objects.filter(admin_user=extndusr)
        grpmem = GroupMember.objects.filter(user=extndusr)
        groups = []
        grpmems = []
        for i in grp:
            groups.append(i.group_name)
        for j in grpmem:
            grpmems.append(j.group)

        dict={'suggestion':True,'grp':grpmem1,'name':admin_user,'param':groups,'param2':grpmems,'grpname':group_name}

        return render(request,'Filmatopedia/groupinfo.html',dict)
    else:
        return HttpResponse('<h1>Page not Found</h1>')











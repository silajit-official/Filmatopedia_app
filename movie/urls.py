from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name='index'),
    path('index/', views.index,name='index'),
    path('about/', views.about,name='about'),
    path('news/', views.news,name='news'),
    path('signup/', views.signup,name='signup'),
    path('login_req/', views.login_req,name='login_req'),
    path('logout_req/', views.logout_req,name='logout_req'),


    #Profile Editing stuffs
    path('profile/', views.profile,name='profile'),
    path('editprofile/', views.editprofile,name='editprofile'),
    path('editpassword/', views.editpassword,name='editpassword'),
    path('editpic/', views.editpic,name='editpic'),
    path('changeprofile/', views.changeprofile,name='changeprofile'),
    path('changepic/', views.changepic,name='changepic'),
    path('changepassword/', views.changepassword,name='changepassword'),

    #Group Creation
    path('suggestion/', views.suggestion,name='suggestion'),
    path('postsuggestion/', views.postsuggestion,name='postsuggestion'),
    path('addsuggestion/', views.addsuggestion,name='addsuggestion'),
    path('reqsuggestion/', views.reqsuggestion,name='reqsuggestion'),
    path('getsuggestion/', views.getsuggestion,name='getsuggestion'),
    path('creategroup/', views.creategroup,name='creategroup'),
    path('addmember/', views.addmember,name='addmember'),
    path('groups/', views.groups,name='groups'),
    path('groupinfo/', views.groupinfo,name='groupinfo'),


]
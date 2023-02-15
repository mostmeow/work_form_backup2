from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('classroom/<int:coursecode>', views.classroom, name='classroom'),
         
    # path('registerform/<str:coursecode>', views.registerform, name='registerform'),
    path('registerform/<int:classcode>', views.registerform, name='registerform'),

    path('checkouttransfer/<str:data>', views.checkouttransfer, name='checkouttransfer'),
    path('qrtransfer/<str:data>', views.qrtransfer, name='qrtransfer'),
    path('checkoutcredit/<str:data>', views.checkoutcredit, name='checkoutcredit'),

    path('checkoutvouchertransfer/<str:data>', views.checkoutvouchertransfer, name='checkoutvouchertransfer'),
    path('checkoutvouchercredit/<str:data>', views.checkoutvouchercredit, name='checkoutvouchercredit'),

    path('checkoutredirect', views.checkoutredirect, name='checkoutredirect'),

    path('signup/<str:regisid>', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
]
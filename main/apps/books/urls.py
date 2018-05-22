from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.books),
    url(r'^logout$', views.logout),
    url(r'^books/add$', views.add),
    url(r'^addbook$', views.addbook),
    url(r'^books/(?P<id>\d+)$', views.showbook),
    url(r'^getuser$', views.getuser),
    url(r'^users/(?P<id>\d+)$', views.showusers),
    url(r'^books/(?P<id>\d+)/addreview$', views.addreview),
    url(r'^books/(?P<bookid>\d+)/delete/(?P<reviewid>\d+)$', views.delete)

]
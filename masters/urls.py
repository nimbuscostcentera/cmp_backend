from django.urls import path



from . import views
from .views import   Layout10List, Layout1List, Layout9List,SpcpmasterList,Layout2List,Layout3List,Layout4List,Layout5List,Layout6List,Layout7List,Layout8List, UnitMasterDetail, UnitMasterList
from .views import HelloAPI
urlpatterns = [
    path('', views.home_view, name='home'),  # root URL
    path('hello/', HelloAPI.as_view(), name='hello_api'),
    path('unitmaster/', UnitMasterList.as_view(),name='unitmaster-list'),
    path('unitmaster/<int:pk>/',UnitMasterDetail.as_view(),name='unitmaster-detail'),
    path("layout1/", Layout1List.as_view()),          # list + create
    path("layout1/<int:pk>/", Layout1List.as_view()), # detail + update + delete
    path("layout2/", Layout2List.as_view()),
    path("layout2/<int:pk>/", Layout2List.as_view()),
    path("layout3/", Layout3List.as_view()),
    path("layout3/<int:pk>/", Layout3List.as_view()),
    path("layout4/", Layout4List.as_view()),
    path("layout4/<int:pk>/", Layout4List.as_view()),
    path("layout5/", Layout5List.as_view()),
    path("layout5/<int:pk>/", Layout5List.as_view()),
    path("layout6/", Layout6List.as_view()),
    path("layout6/<int:pk>/", Layout6List.as_view()),
    path("layout7/", Layout7List.as_view()),
    path("layout7/<int:pk>/", Layout7List.as_view()),
    path("layout8/", Layout8List.as_view()),
    path("layout8/<int:pk>/", Layout8List.as_view()),
    path("SpcpmasterList/", SpcpmasterList.as_view()),
    path("SpcpmasterList/<int:pk>/", SpcpmasterList.as_view()),
    path("DesignMasterList/", Layout9List.as_view()),
    path("DesignMasterList/<int:pk>/", Layout9List.as_view()),
    # path("layout9/", Layout9List.as_view()),
    # path("layout9/<int:pk>/", Layout9List.as_view()),
    path("layout10/", Layout10List.as_view()),
    path("layout10/<int:pk>/", Layout10List.as_view()),
    # path("layout11/", Layout11List.as_view()),
    # path("layout11/<int:pk>/", Layout11List.as_view()),
    # path("layout13/",Layout13List.as_view()),
    # path("layout13/<int:pk>/",Layout13List.as_view())
]

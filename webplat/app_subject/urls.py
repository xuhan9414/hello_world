from django.conf.urls import url
from django.views.static import serve

from app_subject import views_emf
from app_subject import views_channel_coverage
from app_subject import emf_data_analyse, emf_cal, emf_history

urlpatterns = [

    url(r'^emf/' ,views_emf.emf_analyse),
    url(r'^analyse_emf/' ,emf_data_analyse.analyse_emf),
    url(r'^emf_ajax/' ,emf_cal.emf_ajax),
    url(r'^emf_add/' ,emf_cal.emf_add),
    url(r'^emf_time_searching/' ,emf_history.emf_time_searching),
    url(r'^emf_result_searching/' ,emf_history.emf_result_searching),
    url(r'^emf_date_searching/' ,emf_history.date_searching),
    url(r'^emf_download/' ,emf_history.emf_download , name="emf_download"),
    url(r'^channel_coverage/' ,views_channel_coverage.channel_coverage),



    url(r'^Medias1/(?P<path>.*)$', serve,  #设置根目录
        {'document_root': 'D:\emf_history_data/output_data'}),

]
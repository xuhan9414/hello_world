from django.conf.urls import url
from django.views.static import serve

from app_assist import view_csv

urlpatterns = [

    url(r'^csv/', view_csv.csv_merge_searching),
    url(r'^csv_merge_load/', view_csv.csv_merge_load),
    url(r'^medias2/(?P<path>.*)$',serve,
        {'document_root':'D:/merge_data/output_data'}),
    url(r'^merge_date_searching/',view_csv.csv_merge_date_searching),
    url(r'^merge_time_searching/',view_csv.csv_merge_time_searching),

]
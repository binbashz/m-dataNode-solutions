from django.urls import path
from . import views
from .views import management_view
from .views import generar_pdf_recomendaciones
from .views import recomendar_cultivo_view
from django.contrib.auth import views as auth_views
from .views import (
    VariedadListView,
    VariedadCreateView,
    VariedadUpdateView,
    VariedadDeleteView,
)

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.exit, name='exit'),
    path('products/', views.products, name='products'),

    path('variedad/create/', views.variedad_create, name='variedad_create'),
    path('variedad/<int:pk>/update/', views.variedad_update, name='variedad_update'),
    path('variedad/<int:pk>/delete/', views.variedad_delete, name='variedad_delete'),

    path('condiciones/', views.todas_condiciones_cultivo, name='todas_condiciones_cultivo'),
    path('variedad/<int:variedad_id>/condiciones/', views.condiciones_cultivo_list, name='condiciones_cultivo_list'),
    path('variedad/<int:variedad_id>/condiciones/create/', views.condiciones_cultivo_create, name='condiciones_cultivo_create'),
    path('variedad/<int:variedad_id>/condiciones/<int:pk>/update/', views.condiciones_cultivo_update, name='condiciones_cultivo_update'),
    path('variedad/<int:variedad_id>/condiciones/<int:pk>/delete/', views.condiciones_cultivo_delete, name='condiciones_cultivo_delete'),

    path('variedad/<int:variedad_id>/tratamientos/', views.tratamiento_list, name='tratamiento_list'),
    path('variedad/<int:variedad_id>/tratamientos/create/', views.tratamiento_create, name='tratamiento_create'),
    path('variedad/<int:variedad_id>/tratamientos/<int:pk>/update/', views.tratamiento_update, name='tratamiento_update'),
    path('variedad/<int:variedad_id>/tratamientos/<int:pk>/delete/', views.tratamiento_delete, name='tratamiento_delete'),

    path('variedad/<int:variedad_id>/analisis/', views.analisis_list, name='analisis_list'),
    path('variedad/<int:variedad_id>/analisis/create/', views.analisis_create, name='analisis_create'),
    path('variedad/<int:variedad_id>/analisis/<int:pk>/update/', views.analisis_update, name='analisis_update'),
    path('variedad/<int:variedad_id>/analisis/<int:pk>/delete/', views.analisis_delete, name='analisis_delete'),

    path('analisis/<int:pk>/', views.analisis_detail, name='analisis_detail'),
    path('variedad/<int:variedad_id>/analisis/<int:analisis_id>/', views.analisis_detail, name='analisis_detail'),

    path('variedad/list/', VariedadListView.as_view(), name='variedad_list'),
    path('variedad/create/', VariedadCreateView.as_view(), name='variedad_create_view'),
    path('variedad/<int:pk>/update/', VariedadUpdateView.as_view(), name='variedad_update_view'),
    path('variedad/<int:pk>/delete/', VariedadDeleteView.as_view(), name='variedad_delete_view'),

    path('mi_vista/', views.mi_vista, name='mi_vista'),
    
    path('features/', management_view, name='management-view'),

    path('recomendar_cultivo/', views.recomendar_cultivo_view, name='recomendar_cultivo'),
    path('recomendaciones/', views.recomendaciones_view, name='recomendaciones'), 
    
    path('generar_pdf_recomendaciones/', generar_pdf_recomendaciones, name='generar_pdf_recomendaciones'),
    
    path('simulacion/', views.simular_rendimiento, name='simulacion_rendimiento'),
    
    path('analizar-costos-presupuestos/', views.analizar_costos_presupuestos, name='analizar_costos_presupuestos'),
    
    path('clientes/', views.clientes, name='clientes'),
    path('cliente-nuevo/', views.cliente_nuevo, name='cliente_nuevo'),
    path('recepcion-muestra/', views.recepcion_muestra, name='recepcion_muestra'),
    path('programar-analisis/', views.programar_analisis, name='programar_analisis'),
    path('registro-resultados/', views.registro_resultados, name='registro_resultados'),
    path('ver-informes/', views.ver_informes, name='ver_informes'),
    
    path('barcodes/', views.barcodes_view, name='barcodes'),
    path('barcode/', views.barcode_form, name='barcode_form'),
    path('barcode2/', views.barcode_form2, name='barcode_form2'),
    path('decode_barcode/', views.decode_barcode_view, name='decode_barcode'),
        
    path('error/<str:error_message>/', views.error_page, name='error_page'),
    path('error/404/', views.error_404, name='error_404'),
    path('error/500/', views.error_500, name='error_500'),
]

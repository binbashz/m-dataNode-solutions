from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import management_view
from .views import generar_pdf_recomendaciones
from .views import recomendar_cultivo_view
from .views import graficar_datos
#from .tasks import iniciar_scheduler
from django.contrib.auth import views as auth_views
from .views import (
    VariedadListView,
    VariedadCreateView,
    VariedadUpdateView,
    VariedadDeleteView,
)

from rest_framework.routers import DefaultRouter
from .views import CondicionesCultivoViewSet

# iniciar_scheduler()

router = DefaultRouter()
router.register(r'condiciones-cultivo', CondicionesCultivoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.home, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
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
    path('editar_cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar_cliente/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    
    path('recepcion-muestra/', views.recepcion_muestra, name='recepcion_muestra'),
    
    path('programar-analisis/', views.programar_analisis, name='programar_analisis'),
    path('programar-analisis/<int:muestra_id>/', views.programar_analisis, name='programar_analisis'),
    
    path('registro-resultados/', views.registro_resultados, name='registro_resultados'),
    path('ver-informes/', views.ver_informes, name='ver_informes'),
    
    path('barcodes/', views.barcodes_view, name='barcodes'),
    path('barcode/', views.barcode_form, name='barcode_form'),
    path('barcode2/', views.barcode_form2, name='barcode_form2'),
    path('decode_barcode/', views.decode_barcode_view, name='decode_barcode'),
    path('favorite-barcodes/', views.favorite_barcodes, name='favorite_barcodes'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-venta/', views.add_venta, name='add_venta'),
    path('graficar-datos/', views.graficar_datos, name='graficar_datos'),
    path('borrar_gasto/<int:gasto_id>/', views.borrar_gasto, name='borrar_gasto'),
    path('borrar_venta/<int:venta_id>/', views.borrar_venta, name='borrar_venta'),
    path('actualizar-estado-pedido/<int:pedido_id>/', views.actualizar_estado_pedido, name='actualizar_estado_pedido'),
    
    path('notificaciones/', views.listar_notificaciones, name='listar_notificaciones'),
    path('obtener-notificaciones/', views.obtener_notificaciones, name='obtener_notificaciones'),
    path('marcar-leida/<int:notificacion_id>/', views.marcar_leida, name='marcar_leida'),
    
    path('borrar_pedido/<int:pedido_id>/', views.borrar_pedido, name='borrar_pedido'),
    
    path('search/', views.search_results, name='search_results'),
    
    path('graficos/', views.visualizacion_graficos, name='graficos'),
    
    path('panel/', views.panel_de_control, name='panel_de_control'),
    path('planes-produccion/', views.lista_planes_produccion, name='lista_planes_produccion'),
    path('planes-produccion/<int:pk>/', views.detalle_plan_produccion, name='detalle_plan_produccion'),
    path('planes-produccion/nuevo/', views.crear_plan_produccion, name='crear_plan_produccion'),
    path('planes/<int:pk>/eliminar/', views.eliminar_plan_produccion, name='eliminar_plan_produccion'),
    path('bom/', views.lista_bom, name='lista_bom'),
    path('bom/<int:pk>/', views.detalle_bom, name='detalle_bom'),
    path('bom/nuevo/', views.crear_bom, name='crear_bom'),
    path('bom/<int:pk>/eliminar/', views.eliminar_bom, name='eliminar_bom'),
    
    path('miembros/', views.lista_miembros, name='lista_miembros'),
    path('miembro/registrar/', views.registrar_miembro, name='registrar_miembro'),
    path('miembro/<int:miembro_id>/', views.detalle_miembro, name='detalle_miembro'),
    path('detalle_miembro/<int:miembro_id>/', views.detalle_miembro, name='detalle_miembro'),
    path('miembro/<int:miembro_id>/editar/', views.editar_miembro, name='editar_miembro'),
    path('miembro/<int:miembro_id>/eliminar/', views.eliminar_miembro, name='eliminar_miembro'),
    path('reporte-cuotas/', views.reporte_cuotas, name='reporte_cuotas'), 
    path('eliminar_cuota/<int:cuota_id>/', views.eliminar_cuota, name='eliminar_cuota'),
    path('eliminar_todas_cuotas/<int:miembro_id>/', views.eliminar_todas_cuotas, name='eliminar_todas_cuotas'),
    path('marcar_pagado/<int:cuota_id>/', views.marcar_pagado, name='marcar_pagado'),
    path('historial_pagos/', views.historial_pagos, name='historial_pagos'),
    path('historial_pagos/<int:miembro_id>/', views.historial_pagos, name='historial_pagos'),
    path('historial-cuotas-todos-miembros/', views.historial_cuotas_todos_miembros, name='historial_cuotas_todos_miembros'),
    
    path('stock/<int:product_id>/', views.stock_detail, name='stock_detail'),
    path('stock/', views.lista_stock, name='lista_stock'),
    path('add-product-to-stock/', views.add_product_to_stock, name='add_product_to_stock'),
    path('stock/<int:product_id>/eliminar/', views.eliminar_stock, name='eliminar_stock'),
    
    path('plants/', views.plant_list, name='plant_list'),
        
    path('error/<str:error_message>/', views.error_page, name='error_page'),
    path('error/404/', views.error_404, name='error_404'),
    path('error/500/', views.error_500, name='error_500'),
    
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
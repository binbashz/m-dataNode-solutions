# simulacion.py
def calcular_rendimiento(cultivo):
    rendimiento_base = 100  # Rendimiento base en gramos (ejemplo)
    
    # Ajuste por intensidad de luz
    if cultivo.luz_intensidad > 20000:
        rendimiento_base *= 1.2
    elif cultivo.luz_intensidad < 10000:
        rendimiento_base *= 0.8

    # Ajuste por horas de luz
    if cultivo.luz_horas >= 18:
        rendimiento_base *= 1.1
    elif cultivo.luz_horas < 12:
        rendimiento_base *= 0.9

    # Ajuste por temperatura
    if 20 <= cultivo.temperatura_dia <= 30:
        rendimiento_base *= 1.1
    else:
        rendimiento_base *= 0.9

    # Ajuste por humedad
    if 40 <= cultivo.humedad <= 70:
        rendimiento_base *= 1.1
    else:
        rendimiento_base *= 0.9

    # Ajuste por pH
    if 5.5 <= cultivo.ph <= 7.0:
        rendimiento_base *= 1.1
    else:
        rendimiento_base *= 0.9

    return rendimiento_base

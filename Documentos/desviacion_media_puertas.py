# El almacén puertas automaticas fabrica y comercializa diferentes productos para la industria. 
# La siguiente lista indica el número de minutos que se requieren para instalar una muestra de 10 puertas automáticas: 
# 45, 47, 34, 31, 33, 52, 45, 33, 50 y 44

# Cálculo de la desviación media usando la fórmula: Dm = Σ|xi - x̄|/n

def calcular_desviacion_media():
    # Datos de la muestra
    datos = [45, 47, 34, 31, 33, 52, 45, 33, 50, 44]
    n = len(datos)
    
    print("CÁLCULO DE LA DESVIACIÓN MEDIA")
    print("="*50)
    print(f"Datos: {datos}")
    print(f"Tamaño de la muestra (n): {n}")
    
    # Paso 1: Calcular la media aritmética (x̄)
    suma_datos = sum(datos)
    media = suma_datos / n
    print(f"\nPaso 1: Calcular la media (x̄)")
    print(f"x̄ = Σxi / n = {suma_datos} / {n} = {media:.4f}")
    
    # Paso 2: Calcular |xi - x̄| para cada dato
    print(f"\nPaso 2: Calcular |xi - x̄| para cada valor")
    print(f"{'i':<3} {'xi':<6} {'xi - x̄':<10} {'|xi - x̄|':<10}")
    print("-" * 35)
    
    desviaciones_absolutas = []
    suma_desviaciones = 0
    
    for i, valor in enumerate(datos, 1):
        diferencia = valor - media
        desviacion_absoluta = abs(diferencia)
        desviaciones_absolutas.append(desviacion_absoluta)
        suma_desviaciones += desviacion_absoluta
        
        print(f"{i:<3} {valor:<6} {diferencia:<10.4f} {desviacion_absoluta:<10.4f}")
    
    print("-" * 35)
    print(f"{'':>3} {'':>6} {'Σ|xi - x̄| =':<10} {suma_desviaciones:<10.4f}")
    
    # Paso 3: Aplicar la fórmula de desviación media
    desviacion_media = suma_desviaciones / n
    
    print(f"\nPaso 3: Aplicar la fórmula de desviación media")
    print(f"Dm = Σ|xi - x̄| / n")
    print(f"Dm = {suma_desviaciones:.4f} / {n}")
    print(f"Dm = {desviacion_media:.4f} minutos")
    
    # Verificación con 4 decimales
    print(f"\nVERIFICACIÓN:")
    print(f"Desviación media calculada: {desviacion_media:.4f} minutos")
    print(f"Respuesta esperada: 6.8000 minutos")
    if abs(desviacion_media - 6.8) < 0.1:
        print("✓ El resultado coincide con la respuesta esperada")
    else:
        print(f"Diferencia: {abs(desviacion_media - 6.8):.4f}")
    
    return desviacion_media, media, desviaciones_absolutas

# Ejecutar el cálculo
if __name__ == "__main__":
    dm, media, desviaciones = calcular_desviacion_media()
    
    print(f"\n{'='*50}")
    print(f"RESULTADO FINAL:")
    print(f"La desviación media de esta muestra es: {dm:.4f} minutos")
    print(f"{'='*50}")

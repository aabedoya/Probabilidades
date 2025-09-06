import statistics
import math

contaduria=(3.4,4.5,3.9,2.8,3.7,3.5,3,3.4,4.2)
admin=(3.3,5.7,4.9,4.0,4.4,4.5,3.8,4.1,5.4,3.7,4.9)

def calcular_estadisticas(datos, nombre_grupo):
    print(f"\n--- ESTADÍSTICAS DE {nombre_grupo.upper()} ---")
    
    # Promedio (media aritmética)
    promedio = sum(datos) / len(datos)
    print(f"Promedio: {promedio:.4f}")
    
    # Varianza (usando la fórmula de la población)
    varianza = sum((x - promedio)**2 for x in datos) / len(datos)
    print(f"Varianza: {varianza:.4f}")
    
    # Desviación estándar
    desviacion_estandar = math.sqrt(varianza)
    print(f"Desviación estándar: {desviacion_estandar:.4f}")
    
    # Rango
    rango = max(datos) - min(datos)
    print(f"Rango: {rango:.4f}")
    print(f"  Valor mínimo: {min(datos):.1f}")
    print(f"  Valor máximo: {max(datos):.1f}")
    
    # Dispersión relativa (coeficiente de variación)
    dispersion_relativa = (desviacion_estandar / promedio) * 100
    print(f"Dispersión relativa (CV): {dispersion_relativa:.2f}%")
    
    return {
        'promedio': promedio,
        'varianza': varianza,
        'desviacion_estandar': desviacion_estandar,
        'rango': rango,
        'dispersion_relativa': dispersion_relativa
    }

# Calcular estadísticas para ambos grupos
print("ANÁLISIS ESTADÍSTICO DE SALARIOS")
print("="*40)

stats_contaduria = calcular_estadisticas(contaduria, "CONTADURÍA")
stats_admin = calcular_estadisticas(admin, "ADMINISTRACIÓN")

# Comparación entre grupos
print(f"\n--- COMPARACIÓN ---")
print(f"Diferencia de promedios: {abs(stats_admin['promedio'] - stats_contaduria['promedio']):.4f}")
print(f"Grupo con mayor promedio: {'Administración' if stats_admin['promedio'] > stats_contaduria['promedio'] else 'Contaduría'}")
print(f"Grupo con mayor variabilidad: {'Administración' if stats_admin['dispersion_relativa'] > stats_contaduria['dispersion_relativa'] else 'Contaduría'}")
print(f"Grupo más homogéneo: {'Administración' if stats_admin['dispersion_relativa'] < stats_contaduria['dispersion_relativa'] else 'Contaduría'}")

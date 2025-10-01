"""
Problema de Probabilidades - Banco y Cuentas de Clientes

Un banco determina que:
- 50% de sus clientes tienen cuenta corriente
- 75% tienen cuenta de ahorros  
- 45% tienen cuenta corriente Y cuenta de ahorros

Pregunta: ¿Cuál es la probabilidad de que un cliente elegido al azar 
solamente tenga cuenta de ahorros?
"""

def resolver_problema_banco():
    print("=" * 60)
    print("PROBLEMA DE PROBABILIDADES - CUENTAS BANCARIAS")
    print("=" * 60)
    
    # Definir eventos
    print("\n1️⃣ DEFINICIÓN DE EVENTOS:")
    print("   CC = Cliente tiene cuenta corriente")
    print("   CA = Cliente tiene cuenta de ahorros")
    print("   CC ∩ CA = Cliente tiene ambas cuentas")
    
    # Probabilidades dadas
    P_CC = 0.50      # 50% tienen cuenta corriente
    P_CA = 0.75      # 75% tienen cuenta de ahorros
    P_CC_y_CA = 0.45 # 45% tienen ambas cuentas
    
    print(f"\n2️⃣ PROBABILIDADES DADAS:")
    print(f"   P(CC) = {P_CC}")
    print(f"   P(CA) = {P_CA}")
    print(f"   P(CC ∩ CA) = {P_CC_y_CA}")
    
    # Lo que buscamos: P(solo cuenta de ahorros)
    print(f"\n3️⃣ LO QUE BUSCAMOS:")
    print(f"   P(solo CA) = P(CA y NO CC)")
    print(f"   P(solo CA) = P(CA) - P(CA ∩ CC)")
    print(f"   P(solo CA) = P(CA) - P(CC ∩ CA)")
    
    # Cálculo
    P_solo_CA = P_CA - P_CC_y_CA
    
    print(f"\n4️⃣ CÁLCULO:")
    print(f"   P(solo CA) = {P_CA} - {P_CC_y_CA}")
    print(f"   P(solo CA) = {P_solo_CA}")
    
    # Verificación con 4 decimales
    resultado = round(P_solo_CA, 4)
    
    print(f"\n5️⃣ RESULTADO FINAL:")
    print(f"   P(solo cuenta de ahorros) = {resultado}")
    
    # Verificación adicional
    print(f"\n6️⃣ VERIFICACIÓN:")
    P_solo_CC = P_CC - P_CC_y_CA
    P_ambas = P_CC_y_CA
    P_ninguna = 1 - P_CC - P_CA + P_CC_y_CA
    
    print(f"   P(solo CC) = {P_CC} - {P_CC_y_CA} = {P_solo_CC}")
    print(f"   P(ambas) = {P_ambas}")
    print(f"   P(solo CA) = {resultado}")
    print(f"   P(ninguna) = 1 - {P_CC} - {P_CA} + {P_CC_y_CA} = {P_ninguna}")
    print(f"   Suma total = {P_solo_CC + P_ambas + resultado + P_ninguna}")
    
    return resultado

if __name__ == "__main__":
    resultado = resolver_problema_banco()
    print(f"\n🎯 RESPUESTA: {resultado}")
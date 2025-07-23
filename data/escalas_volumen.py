# escalas_volumen.py

escalas_volumen = {
    "BANCO GUAYAQUIL S.A.": 70000,  # Aumentado desde 63000
    "CORPORACION FAVORITA C.A.": 110000,  # Aumentado desde 100000
    "BANCO DE LA PRODUCCION S.A . PRODUBANCO": 220000,  # Aumentado desde 200000
    "CERVECERIA NACIONAL CN S A": 660,  # Aumentado desde 600
    "HOLCIM ECUADOR S.A.": 2300,  # Aumentado desde 2100
    "BRIKAPITAL SA": 28,  # Aumentado desde 25
    "BANCO PICHINCHA C.A.": 950,  # Aumentado desde 860
    "INVERSANCARLOS": 60000,  # Aumentado desde 370000
    "SAN CARLOS SOC. AGR. IND.": 120000,  # Aumentado desde 65000
    "BANCO BOLIVARIANO C.A.": 130000,  # Aumentado desde 120000
    "BOLSA DE VALORES DE GUAYAQUIL": 70000,  # Aumentado desde 65000
    "BOLSA DE VALORES DE QUITO": 70000,  # Aumentado desde 25000
    "CONTINENTAL TIRE ANDINA S A": 5500,  # Aumentado desde 5000
    "BEVERAGE BRAND PATENTS SA": 1200,  # Aumentado desde 1100
    "INDUSTRIAS ALES": 20000, 
    "CONCLINA C A  CIA CONJU CLINICO NACIONAL": 30000,
    "CONTINENTAL TIRE ANDINA S A": 22500,
    "BANCO DEL AUSTRO": 650, 
}

def obtener_escala_volumen(nombre_empresa):
    return escalas_volumen.get(nombre_empresa, 1000)  # Valor predeterminado de 1000 si la empresa no está en el diccionario

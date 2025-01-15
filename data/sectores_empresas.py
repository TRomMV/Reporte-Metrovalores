# sectores_empresas.py

sectores_empresas = {
    "BANCO GUAYAQUIL S.A.": "Financiero",
    "CORPORACION FAVORITA C.A.": "Bienes de consumo",
    "BANCO DE LA PRODUCCION S.A . PRODUBANCO": "Financiero",
    "CERVECERIA NACIONAL CN S A": "Bebidas alcohólicas",
    "HOLCIM ECUADOR S.A.": "Construcción",
    "BRIKAPITAL SA": "Inmobiliaria",
    "BANCO PICHINCHA C.A.": "Financiero",
    "INVERSANCARLOS": "Industrial",
    "SAN CARLOS SOC. AGR. IND.": "Agricultura",
    "BANCO BOLIVARIANO C.A.": "Financiero",
    "BOLSA DE VALORES DE GUAYAQUIL": "Mercado de valores",
    "BOLSA DE VALORES DE QUITO": "Mercado de valores",
    "CONTINENTAL TIRE ANDINA S A": "Automotriz",
    "BEVERAGE BRAND PATENTS SA": "Propiedad intelectual/Bebidas",
    "INDUSTRIAS ALES": "Consumo masivo"
}


def obtener_sector_empresa(nombre_empresa):
    return sectores_empresas.get(nombre_empresa, "Sector no disponible")

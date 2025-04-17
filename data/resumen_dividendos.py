def obtener_resumen_dividendos(empresa):
    resúmenes = {
        "BANCO GUAYAQUIL S.A.": "Aunque el rendimiento del dividendo (yield) disminuyó de 9.27% en 2023 a 7.60% en 2024, sigue siendo un rendimiento atractivo en comparación con otras opciones de inversión. La distribución constante de dividendos demuestra la estabilidad financiera del banco y su compromiso con los accionistas. El precio de la acción experimentó un aumento de $1.10 en 2023 a $1.20 en 2024, lo que indica una tendencia positiva en el valor de la institución. El aumento en el precio de la acción es un indicativo de la confianza del mercado en Banco Guayaquil. Si bien hubo una ligera disminución en el dividendo en efectivo por acción de $0.1020 en 2023 a $0.0912 en 2024, el banco mantiene su política de entrega de dividendos. Se mantiene un buen porcentaje de aumento de capital por acción. Banco Guayaquil S.A., representa una opción atractiva para inversores que buscan ingresos por dividendos y potencial de apreciación del capital a largo plazo.",
        "CORPORACION FAVORITA C.A.": "El capital se mantuvo estable en $900,000.00 tanto en 2023 como en 2024, mientras que la utilidad neta mostró una ligera disminución, pasando de $165,233.00 en 2023 a $157,778.00 en 2024. Cabe mencionar que la junta correspondiente al ejercicio fiscal 2024 aún no se ha llevado a cabo, y se espera que los resultados y detalles sean divulgados durante el presente mes de abril, proporcionando así una base más completa para el análisis.",
        "BANCO DE LA PRODUCCION S.A . PRODUBANCO": "Produbanco presentó un capital incrementado de $478,820.00 en 2023 a $520,460.00 en 2024, reflejando un crecimiento en su estructura de financiación. Sin embargo, la utilidad neta registró una contracción significativa, disminuyendo de $65,751.00 en 2023 a $42,900.00 en 2024. Además, el dividendo en efectivo disminuyó de $17,753.00 en 2023 a $11,583.00 en 2024, con una baja en el dividendo por acción de $0.0371 a $0.02. Pese a estos descensos, el fortalecimiento del capital sugiere un enfoque estratégico en la sustentabilidad a largo plazo.",
        "CERVECERIA NACIONAL CN S A": "CERVECERÍA NACIONAL mantuvo su capital en $20,490.47 tanto en 2023 como en 2024, mientras que su utilidad neta reflejó un crecimiento positivo, aumentando de $66,780.00 en 2023 a $70,575.00 en 2024. De forma alineada, el dividendo en efectivo incrementó de $66,780.00 a $70,575.00, así como el dividendo por acción, que pasó de $3.26 a $3.44. Aunque el rendimiento del dividendo disminuyó de 8.15% a 7.48%, el último precio de la acción creció significativamente, de $40.00 a $46.00, lo que demuestra una valoración fortalecida.",
        "HOLCIM ECUADOR S.A.": "HOLCIM mantuvo su capital estable en $61,420.00 en 2023 y 2024, mientras que su utilidad neta mostró una disminución significativa, pasando de $95,322.00 en 2023 a $77,872.00 en 2024. Asimismo, el dividendo en efectivo decreció de $28,596.00 a $23,361.00, reflejando una baja en el dividendo por acción de $1.40 a $1.14. A pesar de la contracción en las cifras financieras clave, la empresa continúa mostrando solidez en su estructura de capital.",
        "BANCO PICHINCHA C.A.": "El precio de la acción se ha mantenido constante en $80.00 en los últimos dos años, lo que sugiere una estabilidad en el mercado. En cuanto a la dinámica de los dividendos, se evidencia disminución en los dividendos totales y por acción, así como en el rendimiento del dividendo, lo cual se explicaría básicamente por la menor rentabilidad del banco en el 2024 respecto al año anterior. Lo que repercute, también, en una disminución del aumento de capital por acción. Sin embargo, del comportamiento de las acciones, Banco Pichincha es una institución financiera sólida, con excelente trayectoria en el mercado.",
        "SAN CARLOS SOC. AGR. IND.": "SAN CARLOS SA mantuvo su capital estable en $158,800.00 tanto en 2023 como en 2024. La utilidad neta mostró un ligero aumento, pasando de $10,742.00 en 2023 a $10,829.00 en 2024. Los dividendos en efectivo permanecieron constantes en $5,000.00, con un dividendo por acción de $0.03 en ambos años. El precio de la acción subió de $0.60 en 2023 a $0.65 en 2024, lo que provocó una ligera reducción en el rendimiento del dividendo de 5.25% a 4.84%. Este comportamiento refleja estabilidad en la estructura de capital, con un moderado fortalecimiento en la valoración de las acciones.",
        "BANCO BOLIVARIANO C.A.": "El rendimiento del dividendo se mantiene relativamente estable, con un ligero descenso en el 2024. Esto sugiere una política de dividendos consistente. El precio de la acción experimentó una ligera disminución de $1.03 en 2023 a $0.95 en 2024. Por su parte, Los dividendos en efectivo totales aumentaron ligeramente de 2023 a 2024, aunque el dividendo por acción disminuyó levemente, mientras que el aumento de capital por acción se mantiene en un porcentaje similar al del año 2023.",
        "BOLSA DE VALORES DE GUAYAQUIL": "La Bolsa de Valores de Guayaquil mantuvo su capital constante en $5,009.00 durante 2023 y 2024. La utilidad neta mostró un crecimiento positivo, pasando de $578.11 miles en 2023 a $804.00 miles en 2024. En línea con esto, el dividendo en efectivo incrementó de $426.59 miles a $686.94 miles, mientras que el dividendo por acción pasó de $0.0852 a $0.14. Sin embargo, el último precio de la acción disminuyó ligeramente, de $1.00 en 2023 a $0.96 en 2024. Esto resultó en un aumento del rendimiento del dividendo, pasando de 8.52% a 14.29%, destacando un mayor retorno relativo para los accionistas, pese a la ligera baja en el precio de la acción.",
        "BEVERAGE BRAND PATENTS SA": "BEVERAGE BRAND & PATENTS SA mantuvo su capital constante en $20,490.47 durante 2023 y 2024. La utilidad neta presentó una disminución, pasando de $74,117.56 en 2023 a $70,441.00 en 2024. En línea con esta reducción, el dividendo en efectivo disminuyó de $74,117.56 a $70,441.00, mientras que el dividendo por acción pasó de $3.62 a $3.44. No se registraron aumentos de capital en ninguno de los dos años. Sin embargo, el último precio de la acción mostró un incremento notable, subiendo de $22.00 en 2023 a $35.05 en 2024, lo que implicó una reducción en el rendimiento del dividendo de 16.44% a 9.81%. Este comportamiento resalta un fortalecimiento en la valoración del precio de la acción.",
        "BOLSA DE VALORES DE QUITO": "La Bolsa de Valores de Quito presentó un capital constante de $5,393.00 tanto en 2023 como en 2024. La utilidad neta tuvo un ligero descenso, pasando de $1,824.00 en 2023 a $1,682.00 en 2024. Asimismo, el dividendo en efectivo disminuyó de $1,642.00 a $1,513.00, mientras que el dividendo por acción se redujo de $0.30 a $0.28. A pesar de estas reducciones, el último precio de la acción aumentó de $2.35 en 2023 a $2.90 en 2024, reflejando un incremento en la valoración de las acciones. Esto resultó en una disminución del rendimiento del dividendo, que pasó de 12.96% a 9.67%, señalando un ajuste en el retorno relativo para los inversionistas.",
        "CONCLINA C A  CIA CONJU CLINICO NACIONAL": "CONCLINA C.A. mantuvo un capital constante de $22,985.00 en 2023 y 2024, mientras que la utilidad neta registró una disminución, pasando de $5,531.00 en 2023 a $4,754.00 en 2024. El último precio de la acción mostró una notable revalorización, aumentando de $1.08 en 2023 a $1.33 en 2024, lo que refleja un fortalecimiento en la percepción del mercado hacia las acciones de la empresa. Actualmente, no se dispone de información adicional sobre dividendos, rendimientos u otros indicadores financieros relacionados, ya que se espera que estos datos sean proporcionados tras la junta de accionistas programada para el próximo 22 de abril de 2025.",
        
    
    }


    return resúmenes.get(empresa, "Resumen de dividendos no disponible para esta empresa.")

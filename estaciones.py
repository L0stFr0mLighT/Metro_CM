from common.estacion import Estacion, Linea

l_7 = Linea(7)
l_7.set_color(229, 129, 38)
l_9 = Linea(9)
l_9.set_color(119, 66, 52)
l_1 = Linea(1)
l_1.set_color(194, 60, 127)
l_12 = Linea(12)
l_12.set_color(168, 140, 57)
l_3 = Linea(3)
l_3.set_color(141, 137, 38)

# Linea 7
est_polanco = Estacion("Polanco")
est_polanco.set_pos_mapa((float(152 / 536), float(26/603)))
est_auditorio = Estacion("Auditorio")
est_auditorio.set_pos_mapa((float(152 / 536), float(94 / 603)))
est_constituyentes = Estacion("Constituyentes")
est_constituyentes.set_pos_mapa((float(152 / 536), float(156 / 603)))
est_tacubaya = Estacion("Tacubaya")
est_tacubaya.set_pos_mapa((float(152 / 536), float(216 / 603)))
est_san_pedro = Estacion("San Pedro de los Pinos")
est_san_pedro.set_pos_mapa((float(152 / 536), float(278 / 603)))
est_san_antonio = Estacion("San Antonio")
est_san_antonio.set_pos_mapa((float(152 / 536), float(311 / 603)))
est_mixcoac = Estacion("Mixcoac")
est_mixcoac.set_pos_mapa((float(152 / 536), float(357 / 603)))
est_barranca = Estacion("Barranca dek Muerto")
est_barranca.set_pos_mapa((float(152 / 536), float(414 / 603)))

# Linea 1
est_observatorio = Estacion("Observatorio")
est_observatorio.set_pos_mapa((float(114 / 536), float(256 / 603)))
est_juanacatlan = Estacion("Juanacatlan")
est_juanacatlan.set_pos_mapa((float(189 / 536), float(181 / 603)))
est_chapultepec = Estacion("Chapultepec")
est_chapultepec.set_pos_mapa((float(223 / 536), float(147 / 603)))
est_sevilla = Estacion("Sevilla")
est_sevilla.set_pos_mapa((float(257 / 536), float(112 / 603)))
est_insurgentes = Estacion("Insurgentes")
est_insurgentes.set_pos_mapa((float(291 / 536), float(77 / 603)))
est_cuauhtemoc = Estacion("Cuauhtemoc")
est_cuauhtemoc.set_pos_mapa((float(336 / 536), float(77 / 603)))
est_balderas = Estacion("Balderas")
est_balderas.set_pos_mapa((float(379 / 536), float((77 / 603))))

# Linea 9
est_patriotismo = Estacion("Patriotismo")
est_patriotismo.set_pos_mapa((float(232 / 536), float(217 / 603)))
est_chilpancingo = Estacion("Chilpancingo")
est_chilpancingo.set_pos_mapa((float(322 / 536), float(217 / 603)))
est_centro_medico = Estacion("Centro Medico")
est_centro_medico.set_pos_mapa((float(379 / 536), float(217 / 603)))
est_lazaro = Estacion("Lazaro Cardenas")
est_lazaro.set_pos_mapa((float(473 / 536), float(217 / 603)))

# Linea 12
est_insurgentes_sur = Estacion("Insurgentes sur")
est_insurgentes_sur.set_pos_mapa((float(217 / 536), float(357 / 603)))
est_hospital_20 = Estacion("Hospital 20 de Noviembre")
est_hospital_20.set_pos_mapa((float(290 / 536), float(357 / 603)))
est_zapata = Estacion("Zapata")
est_zapata.set_pos_mapa((float(379 / 536), float(357 / 603)))
est_parque_venados = Estacion("Parque de los Venados")
est_parque_venados.set_pos_mapa((float(467 / 536), float(357 / 603)))
est_eje_central = Estacion("Eje Central")
est_eje_central.set_pos_mapa((float(520 / 536), float(437 / 603)))

# Linea 3
est_juarez = Estacion("Juarez")
est_juarez.set_pos_mapa((float(379 / 536), float(18 / 603)))
est_ninos_heroes = Estacion("Niños Heroes")
est_ninos_heroes.set_pos_mapa((float(379 / 536), float(114 / 603)))
est_hospital_general = Estacion("Hospital General")
est_hospital_general.set_pos_mapa((float(379 / 536), float(151 / 603)))
est_etiopia = Estacion("Etiopia")
est_etiopia.set_pos_mapa((float(379 / 536), float(252 / 603)))
est_eugenia = Estacion("Eugenia")
est_eugenia.set_pos_mapa((float(379 / 536), float(287 / 603)))
est_division = Estacion("Division del Norte")
est_division.set_pos_mapa((float(379 / 536), float(321 / 603)))
est_coyoacan = Estacion("Coyoacan")
est_coyoacan.set_pos_mapa((float(379 / 536), float(391 / 603)))
est_viveros = Estacion("Viveros")
est_viveros.set_pos_mapa((float(379 / 536), float(426 / 603)))
est_ma_quevedo = Estacion("M. A. De Quevedo")
est_ma_quevedo.set_pos_mapa((float(379 / 536), float(460 / 603)))
est_copilco = Estacion("Copilco")
est_copilco.set_pos_mapa((float(379 / 536), float(495 / 603)))
est_universidad = Estacion("Universidad")
est_universidad.set_pos_mapa((float(379 / 536), float(529 / 603)))

# Vecinos L7
est_polanco.add_unico_vecino(est_auditorio, l_7)
est_auditorio.add_vecinos(est_polanco, est_constituyentes, l_7)
est_constituyentes.add_vecinos(est_auditorio, est_tacubaya, l_7)
est_tacubaya.add_vecinos(est_constituyentes, est_san_pedro, l_7)
est_san_pedro.add_vecinos(est_tacubaya, est_san_antonio, l_7)
est_san_antonio.add_vecinos(est_san_pedro, est_mixcoac, l_7)
est_mixcoac.add_vecinos(est_san_antonio, est_barranca, l_7)
est_barranca.add_unico_vecino(est_mixcoac, l_7)
# Vecinos L9
est_tacubaya.add_unico_vecino(est_patriotismo, l_9)
est_patriotismo.add_vecinos(est_tacubaya, est_chilpancingo, l_9)
est_chilpancingo.add_vecinos(est_patriotismo, est_centro_medico, l_9)
est_centro_medico.add_vecinos(est_chilpancingo, est_lazaro, l_9)
est_lazaro.add_unico_vecino(est_centro_medico, l_9)

# Vecinos L1
est_observatorio.add_unico_vecino(est_tacubaya, l_1)
est_tacubaya.add_vecinos(est_observatorio, est_juanacatlan, l_1)
est_juanacatlan.add_vecinos(est_tacubaya, est_chapultepec, l_1)
est_chapultepec.add_vecinos(est_juanacatlan, est_sevilla, l_1)
est_sevilla.add_vecinos(est_chapultepec, est_insurgentes, l_1)
est_insurgentes.add_vecinos(est_sevilla, est_cuauhtemoc, l_1)
est_cuauhtemoc.add_vecinos(est_insurgentes, est_balderas, l_1)

# Vecinos L12
est_mixcoac.add_unico_vecino(est_insurgentes_sur, l_12)
est_insurgentes_sur.add_vecinos(est_mixcoac, est_hospital_20, l_12)
est_hospital_20.add_vecinos(est_insurgentes_sur, est_zapata, l_12)
est_zapata.add_vecinos(est_hospital_20, est_parque_venados, l_12)
est_parque_venados.add_vecinos(est_zapata, est_eje_central, l_12)
est_eje_central.add_unico_vecino(est_parque_venados, l_12)

# Vecinos L3
est_juarez.add_unico_vecino(est_balderas, l_3)
est_balderas.add_vecinos(est_juarez, est_ninos_heroes, l_3)
est_ninos_heroes.add_vecinos(est_balderas, est_hospital_general, l_3)
est_hospital_general.add_vecinos(est_ninos_heroes, est_centro_medico, l_3)
est_centro_medico.add_vecinos(est_hospital_general, est_etiopia, l_3)
est_etiopia.add_vecinos(est_centro_medico, est_division, l_3)
est_division.add_vecinos(est_etiopia, est_zapata, l_3)
est_zapata.add_vecinos(est_division, est_coyoacan, l_3)
est_coyoacan.add_vecinos(est_zapata, est_viveros, l_3)
est_viveros.add_vecinos(est_coyoacan, est_ma_quevedo, l_3)
est_ma_quevedo.add_vecinos(est_viveros, est_copilco, l_3)
est_copilco.add_vecinos(est_ma_quevedo, est_universidad, l_3)
est_universidad.add_unico_vecino(est_copilco, l_3)

# Cabeceras
l_1.set_cabeceras((est_observatorio, est_balderas))
l_12.set_cabeceras((est_mixcoac, est_eje_central))
l_3.set_cabeceras((est_universidad, est_juarez))
l_7.set_cabeceras((est_barranca, est_polanco))
l_9.set_cabeceras((est_tacubaya, est_lazaro))

ESTACIONES = [ est_polanco, est_auditorio, est_constituyentes, est_tacubaya, 
              est_san_pedro, est_san_antonio, est_mixcoac, est_barranca, est_observatorio, 
              est_juanacatlan, est_chapultepec, est_sevilla, est_insurgentes, est_cuauhtemoc, 
              est_balderas, est_patriotismo, est_chilpancingo, est_centro_medico, est_lazaro, 
              est_insurgentes_sur, est_hospital_20, est_zapata, est_parque_venados, est_eje_central, 
              est_juarez, est_ninos_heroes, est_hospital_general, est_etiopia, est_eugenia, 
              est_division, est_coyoacan, est_viveros, est_ma_quevedo, est_copilco, est_universidad
              ]

LINEAS = [l_1, l_12, l_3, l_7, l_9]

from common.estacion import Estacion, Linea, Conexion, Transbordo

# Linea 7
est_polanco = Estacion("Polanco", (float(152 / 536), float(26/603)), localizacion=(0, 0))
est_auditorio = Estacion("Auditorio", (float(152 / 536), float(94 / 603)), localizacion=(0, 0))
est_constituyentes = Estacion("Constituyentes", (float(152 / 536), float(156 / 603)), localizacion=(0, 0))
est_tacubaya = Estacion("Tacubaya", (float(152 / 536), float(216 / 603)), localizacion=(0, 0))
est_san_pedro = Estacion("San Pedro de los Pinos", (float(152 / 536), float(278 / 603)), localizacion=(0, 0))
est_san_antonio = Estacion("San Antonio", (float(152 / 536), float(311 / 603)), localizacion=(0, 0))
est_mixcoac = Estacion("Mixcoac", (float(152 / 536), float(357 / 603)), localizacion=(0, 0))
est_barranca = Estacion("Barranca del Muerto", (float(152 / 536), float(414 / 603)), localizacion=(0, 0))

# Linea 1
est_observatorio = Estacion("Observatorio", (float(114 / 536), float(256 / 603)), localizacion=(0, 0))
est_juanacatlan = Estacion("Juanacatlan", (float(189 / 536), float(181 / 603)), localizacion=(0, 0))
est_chapultepec = Estacion("Chapultepec", (float(223 / 536), float(147 / 603)), localizacion=(0, 0))
est_sevilla = Estacion("Sevilla", (float(257 / 536), float(112 / 603)), localizacion=(0, 0))
est_insurgentes = Estacion("Insurgentes", (float(291 / 536), float(77 / 603)), localizacion=(0, 0))
est_cuauhtemoc = Estacion("Cuauhtemoc", (float(336 / 536), float(77 / 603)), localizacion=(0, 0))
est_balderas = Estacion("Balderas", (float(379 / 536), float((77 / 603))), localizacion=(0, 0))

# Linea 9
est_patriotismo = Estacion("Patriotismo", (float(232 / 536), float(217 / 603)), localizacion=(0, 0))
est_chilpancingo = Estacion("Chilpancingo", (float(322 / 536), float(217 / 603)), localizacion=(0, 0))
est_centro_medico = Estacion("Centro Medico", (float(379 / 536), float(217 / 603)), localizacion=(0, 0))
est_lazaro = Estacion("Lazaro Cardenas", (float(473 / 536), float(217 / 603)), localizacion=(0, 0))

# Linea 12
est_insurgentes_sur = Estacion("Insurgentes sur", (float(217 / 536), float(357 / 603)), localizacion=(0, 0))
est_hospital_20 = Estacion("Hospital 20 de Noviembre", (float(290 / 536), float(357 / 603)), localizacion=(0, 0))
est_zapata = Estacion("Zapata", (float(379 / 536), float(357 / 603)), localizacion=(0, 0))
est_parque_venados = Estacion("Parque de los Venados", (float(467 / 536), float(357 / 603)), localizacion=(0, 0))
est_eje_central = Estacion("Eje Central", (float(520 / 536), float(437 / 603)), localizacion=(0, 0))

# Linea 3
est_juarez = Estacion("Juarez", (float(379 / 536), float(18 / 603)), localizacion=(0, 0))
est_ninos_heroes = Estacion("Niños Heroes", (float(379 / 536), float(114 / 603)), localizacion=(0, 0))
est_hospital_general = Estacion("Hospital General", (float(379 / 536), float(151 / 603)), localizacion=(0, 0))
est_etiopia = Estacion("Etiopia", (float(379 / 536), float(252 / 603)), localizacion=(0, 0))
est_eugenia = Estacion("Eugenia", (float(379 / 536), float(287 / 603)), localizacion=(0, 0))
est_division = Estacion("Division del Norte", (float(379 / 536), float(321 / 603)), localizacion=(0, 0))
est_coyoacan = Estacion("Coyoacan", (float(379 / 536), float(391 / 603)), localizacion=(0, 0))
est_viveros = Estacion("Viveros", (float(379 / 536), float(426 / 603)), localizacion=(0, 0))
est_ma_quevedo = Estacion("M. A. De Quevedo", (float(379 / 536), float(460 / 603)), localizacion=(0, 0))
est_copilco = Estacion("Copilco", (float(379 / 536), float(495 / 603)), localizacion=(0, 0))
est_universidad = Estacion("Universidad", (float(379 / 536), float(529 / 603)), localizacion=(0, 0))

# Lineas y Cabeceras
l_7 = Linea.crear_linea(7, (est_barranca, est_polanco), (229, 129, 38))
l_9 = Linea.crear_linea(9, (est_tacubaya, est_lazaro), (119, 66, 52))
l_1 = Linea.crear_linea(1, (est_observatorio, est_balderas), (194, 60, 127))
l_12 = Linea.crear_linea(12, (est_mixcoac, est_eje_central), (168, 140, 38))
l_3 = Linea.crear_linea(3, (est_universidad, est_juarez), (141, 137, 38))

# Transbordos
tacubaya_l7_l1 = Transbordo(est_tacubaya, l_7, l_1, 0)
tacubaya_l7_l9 = Transbordo(est_tacubaya, l_7, l_9, 0)
tacubaya_l9_l1 = Transbordo(est_tacubaya, l_9, l_1, 0)
mixcoac_l7_l12 = Transbordo(est_mixcoac, l_7, l_12, 0)
balderas_l3_l1 = Transbordo(est_balderas, l_3, l_1, 0)
centro_medico_l9_l3 = Transbordo(est_centro_medico, l_9, l_3, 0)
zapata_l12_l3 = Transbordo(est_zapata, l_12, l_3, 0)

# Vecinos L7
polanco_auditorio = Conexion(est_polanco, est_auditorio, l_7, 2)
auditorio_polanco = polanco_auditorio.simetrico()
auditorio_constituyentes = Conexion(est_auditorio, est_constituyentes, l_7, 3)
constituyentes_auditorio = auditorio_constituyentes.simetrico()
constituyentes_tacubaya = Conexion(est_constituyentes, est_tacubaya, l_7, 1)
tacubaya_constituyentes = constituyentes_tacubaya.simetrico()
tacubaya_san_pedro = Conexion(est_tacubaya, est_san_pedro, l_7, 2)
san_pedro_tacubaya = tacubaya_san_pedro.simetrico()
san_pedro_san_antonio = Conexion(est_san_pedro, est_san_antonio, l_7, 2)
san_antonio_san_pedro = san_pedro_san_antonio.simetrico()
san_antonio_mixcoac = Conexion(est_san_antonio, est_mixcoac, l_7, 2)
mixcoac_san_antonio = san_antonio_mixcoac.simetrico()
mixcoac_barranca = Conexion(est_mixcoac, est_barranca, l_7, 3)
barranca_mixcoac = mixcoac_barranca.simetrico()

# Vecinos L9
tacubaya_patriotismo = Conexion(est_tacubaya, est_patriotismo, l_9, 2)
patriotismo_tacubaya = tacubaya_patriotismo.simetrico()
patriotismo_chilpancingo = Conexion(est_patriotismo, est_chilpancingo, l_9, 2)
chilpancingo_patriotismo = patriotismo_chilpancingo.simetrico()
chilpancingo_centro_medico = Conexion(est_chilpancingo, est_centro_medico, l_9, 2)
centro_medico_chilpancingo = chilpancingo_centro_medico.simetrico()
centro_medico_lazaro = Conexion(est_centro_medico, est_lazaro, l_9, 2)
lazaro_centro_medico = centro_medico_lazaro.simetrico()

# Vecinos L1
observatorio_tacubaya = Conexion(est_observatorio, est_tacubaya, l_1, 3)
tacubaya_observatorio = observatorio_tacubaya.simetrico()
tacubaya_juanacatlan = Conexion(est_tacubaya, est_juanacatlan, l_1, 2)
juanacatlan_tacubaya = tacubaya_juanacatlan.simetrico()
juanacatlan_chapultepec = Conexion(est_juanacatlan, est_chapultepec, l_1, 2)
chapultepec_juanacatlan = juanacatlan_chapultepec.simetrico()
chapultepec_sevilla = Conexion(est_chapultepec, est_sevilla, l_1, 1)
sevilla_chapultepec = chapultepec_sevilla.simetrico()
sevilla_insurgentes = Conexion(est_sevilla, est_insurgentes, l_1, 1)
insurgentes_sevilla = sevilla_insurgentes.simetrico()
insurgentes_cuauhtemoc = Conexion(est_insurgentes, est_cuauhtemoc, l_1, 2)
cuauhtemoc_insurgentes = insurgentes_cuauhtemoc.simetrico()
cuauhtemoc_balderas = Conexion(est_cuauhtemoc, est_balderas, l_1, 1)
balderas_cuauhtemoc = cuauhtemoc_balderas.simetrico()

# Vecinos L12
mixcoac_insurgentes_sur = Conexion(est_mixcoac, est_insurgentes_sur, l_12, 2)
insurgentes_sur_mixcoac = mixcoac_insurgentes_sur.simetrico()
insurgentes_sur_hospital_20 = Conexion(est_insurgentes_sur, est_hospital_20, l_12, 2)
hospital_20_insurgentes_sur = insurgentes_sur_hospital_20.simetrico()
hospital_20_zapata = Conexion(est_hospital_20, est_zapata, l_12, 1)
zapata_hospital_20 = hospital_20_zapata.simetrico()
zapata_parque_venados = Conexion(est_zapata, est_parque_venados, l_12, 2)
parque_venados_zapata = zapata_parque_venados.simetrico()
parque_venados_eje_central = Conexion(est_parque_venados, est_eje_central, l_12, 3)
eje_central_parque_venados = parque_venados_eje_central.simetrico()

# Vecinos L3
balderas_juarez = Conexion(est_balderas, est_juarez, l_3, 2)
juarez_balderas = balderas_juarez.simetrico()
balderas_ninos_heroes = Conexion(est_balderas, est_ninos_heroes, l_3, 1)
ninos_heroes_balderas = balderas_ninos_heroes.simetrico()
ninos_heroes_hospital_general = Conexion(est_ninos_heroes, est_hospital_general, l_3, 1)
hospital_general_ninos_heroes = ninos_heroes_hospital_general.simetrico()
hospital_general_centro_medico = Conexion(est_hospital_general, est_centro_medico, l_3, 1)
centro_medico_hospital_general = hospital_general_centro_medico.simetrico()
centro_medico_etiopia = Conexion(est_centro_medico, est_etiopia, l_3, 3)
etiopia_centro_medico = centro_medico_etiopia.simetrico()
etiopia_eugenia = Conexion(est_etiopia, est_eugenia, l_3, 2)
eugenia_etiopia = etiopia_eugenia.simetrico()
eugenia_division = Conexion(est_eugenia, est_division, l_3, 2)
division_eugenia = eugenia_division.simetrico()
division_zapata = Conexion(est_division, est_zapata, l_3, 2)
zapata_division = division_zapata.simetrico()
zapata_coyoacan = Conexion(est_zapata, est_coyoacan, l_3, 2)
coyoacan_zapata = zapata_coyoacan.simetrico()
coyoacan_viveros = Conexion(est_coyoacan, est_viveros, l_3, 1)
viveros_coyoacan = coyoacan_viveros.simetrico()
viveros_ma_quevedo = Conexion(est_viveros, est_ma_quevedo, l_3, 2)
ma_quevedo_viveros = viveros_ma_quevedo.simetrico()
ma_quevedo_copilco = Conexion(est_ma_quevedo, est_copilco, l_3, 2)
copilco_ma_quevedo = ma_quevedo_copilco.simetrico()
copilco_universidad = Conexion(est_copilco, est_universidad, l_3, 3)
universidad_copilco = copilco_universidad.simetrico()

ESTACIONES = [ est_polanco, est_auditorio, est_constituyentes, est_tacubaya, 
              est_san_pedro, est_san_antonio, est_mixcoac, est_barranca, est_observatorio, 
              est_juanacatlan, est_chapultepec, est_sevilla, est_insurgentes, est_cuauhtemoc, 
              est_balderas, est_patriotismo, est_chilpancingo, est_centro_medico, est_lazaro, 
              est_insurgentes_sur, est_hospital_20, est_zapata, est_parque_venados, est_eje_central, 
              est_juarez, est_ninos_heroes, est_hospital_general, est_etiopia, est_eugenia, 
              est_division, est_coyoacan, est_viveros, est_ma_quevedo, est_copilco, est_universidad
              ]

LINEAS = [l_1, l_12, l_3, l_7, l_9]

TRANSBORDOS = [tacubaya_l7_l9, tacubaya_l7_l1, tacubaya_l9_l1, mixcoac_l7_l12, balderas_l3_l1,
               centro_medico_l9_l3, zapata_l12_l3]

CONEXIONES = [polanco_auditorio, auditorio_polanco, auditorio_constituyentes, constituyentes_auditorio,
              constituyentes_tacubaya,tacubaya_constituyentes,tacubaya_san_pedro,san_pedro_tacubaya,
              san_pedro_san_antonio,san_antonio_san_pedro,san_antonio_mixcoac,mixcoac_san_antonio,
              mixcoac_barranca,barranca_mixcoac,tacubaya_patriotismo,patriotismo_tacubaya,
              patriotismo_chilpancingo,chilpancingo_patriotismo,chilpancingo_centro_medico,
              centro_medico_chilpancingo,centro_medico_lazaro,lazaro_centro_medico,observatorio_tacubaya,
              tacubaya_observatorio,tacubaya_juanacatlan,juanacatlan_tacubaya,juanacatlan_chapultepec,
              chapultepec_juanacatlan,chapultepec_sevilla,sevilla_chapultepec,sevilla_insurgentes,
              insurgentes_sevilla,insurgentes_cuauhtemoc,cuauhtemoc_insurgentes,cuauhtemoc_balderas,
              balderas_cuauhtemoc,mixcoac_insurgentes_sur,insurgentes_sur_mixcoac,
              insurgentes_sur_hospital_20,hospital_20_insurgentes_sur,hospital_20_zapata,
              zapata_hospital_20,zapata_parque_venados,parque_venados_zapata,parque_venados_eje_central,
              eje_central_parque_venados,balderas_juarez,juarez_balderas,balderas_ninos_heroes,
              ninos_heroes_balderas,ninos_heroes_hospital_general,hospital_general_ninos_heroes,
              hospital_general_centro_medico,centro_medico_hospital_general,centro_medico_etiopia,
              etiopia_centro_medico, etiopia_eugenia, eugenia_etiopia,eugenia_division,division_eugenia,
              division_zapata,zapata_division, zapata_coyoacan,coyoacan_zapata,coyoacan_viveros,viveros_coyoacan,
              viveros_ma_quevedo, ma_quevedo_viveros,ma_quevedo_copilco,copilco_ma_quevedo,copilco_universidad,
              universidad_copilco
]

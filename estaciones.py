from common.estacion import Estacion, Linea, Conexion, Transbordo

# Linea 7
est_polanco = Estacion("Polanco", (float(152 / 536), float(26/603)), localizacion=(19.43381203002058, -99.19131847555241), pos_nombre=(float(105/536),float(30/603)), color=(229, 129, 38))
est_auditorio = Estacion("Auditorio", (float(152 / 536), float(94 / 603)), localizacion=(19.4251990996101, -99.1918734241658), pos_nombre=(float(100/536),float(97/603)), color=(229, 129, 38))
est_constituyentes = Estacion("Constituyentes", (float(152 / 536), float(156 / 603)), localizacion=(19.411805671823224, -99.19138047507347), pos_nombre=(float(71/536),float(160/603)), color=(229, 129, 38))
est_tacubaya = Estacion("Tacubaya", (float(152 / 536), float(216 / 603)), localizacion=(19.402609035365366, -99.18763121760838), pos_nombre=(float(93/536),float(216/603)))
est_san_pedro = Estacion("San Pedro de los Pinos", (float(152 / 536), float(278 / 603)), localizacion=(19.39145914334569, -99.18582852364457), pos_nombre=(float(160/536),float(282/603)), color=(229, 129, 38))
est_san_antonio = Estacion("San Antonio", (float(152 / 536), float(311 / 603)), localizacion=(19.38499538729885, -99.1866433534888), pos_nombre=(float(87/536),float(315/603)), color=(229, 129, 38))
est_mixcoac = Estacion("Mixcoac", (float(152 / 536), float(357 / 603)),localizacion=(19.376213004665775, -99.1878018802292), pos_nombre=(float(102/536),float(360/603)))
est_barranca = Estacion("Barranca del Muerto", (float(152 / 536), float(414 / 603)), localizacion=(19.361538963061196, -99.18926508506867), pos_nombre=(float(160/536),float(418/603)), color=(229, 129, 38))

# Linea 1
est_observatorio = Estacion("Observatorio", (float(114 / 536), float(256 / 603)), localizacion=(19.39829098056639, -99.2004013706456), pos_nombre=(float(51/536),float(273/603)), color=(194, 60, 127))
est_juanacatlan = Estacion("Juanacatlan", (float(189 / 536), float(181 / 603)), localizacion=(19.412946006441814, -99.18200782475782), pos_nombre=(float(196/536),float(186/603)), color=(194, 60, 127))
est_chapultepec = Estacion("Chapultepec", (float(223 / 536), float(147 / 603)), localizacion=(19.420607985893884, -99.1769188145414), pos_nombre=(float(231/536),float(153/603)), color=(194, 60, 127))
est_sevilla = Estacion("Sevilla", (float(257 / 536), float(112 / 603)), localizacion=(19.42153563017704, -99.1710509636407), pos_nombre=(float(265/536),float(120/603)), color=(194, 60, 127))
est_insurgentes = Estacion("Insurgentes", (float(291 / 536), float(77 / 603)), localizacion=(19.423634980727975, -99.1633036288456), pos_nombre=(float(227/536),float(82/603)), color=(194, 60, 127))
est_cuauhtemoc = Estacion("Cuauhtemoc", (float(336 / 536), float(77 / 603)), localizacion=(19.42566159881801, -99.15458860289701), pos_nombre=(float(300/536),float(67/603)), color=(194, 60, 127))
est_balderas = Estacion("Balderas", (float(379 / 536), float((77 / 603))), localizacion=(19.427211882417126, -99.14894265253375), pos_nombre=(float(385/536),float(80/603)))

# Linea 9
est_patriotismo = Estacion("Patriotismo", (float(232 / 536), float(217 / 603)), localizacion=(19.406058757243503, -99.17889839836167), pos_nombre=(float(200/536),float(234/603)), color=(119, 66, 52))
est_chilpancingo = Estacion("Chilpancingo", (float(322 / 536), float(217 / 603)), localizacion=(19.405897486248797, -99.16853478250196), pos_nombre=(float(290/536),float(207/603)), color=(119, 66, 52))
est_centro_medico = Estacion("Centro Medico", (float(379 / 536), float(217 / 603)), localizacion=(19.40656701868515, -99.1551792513246), pos_nombre=(float(387/536),float(207/603)))
est_lazaro = Estacion("Lazaro Cardenas", (float(473 / 536), float(217 / 603)), localizacion=(19.40721810482792, -99.1446280852223), pos_nombre=(float(454/536),float(233/603)), color=(119, 66, 52))

# Linea 12
est_insurgentes_sur = Estacion("Insurgentes sur", (float(217 / 536), float(357 / 603)), localizacion=(19.373518830329964, -99.17869155317403), pos_nombre=(float(181/536),float(345/603)), color=(168, 140, 38))
est_hospital_20 = Estacion("Hospital 20 de Noviembre", (float(290 / 536), float(357 / 603)), localizacion=(19.371902963494097, -99.17120580696158), pos_nombre=(float(246/536),float(380/612)), color=(168, 140, 38))
est_zapata = Estacion("Zapata", (float(379 / 536), float(357 / 603)), localizacion=(19.370687413650714, -99.16505860486687), pos_nombre=(float(388/536),float(371/603)))
est_parque_venados = Estacion("Parque de los Venados", (float(467 / 536), float(357 / 603)), localizacion=(19.370625373791682, -99.15872561482674), pos_nombre=(float(420/536),float(345/603)), color=(168, 140, 38))
est_eje_central = Estacion("Eje Central", (float(520 / 536), float(437 / 603)), localizacion=(19.361327761319615, -99.1514213209794), pos_nombre=(float(470/536),float(453/603)), color=(168, 140, 38))

# Linea 3
est_juarez = Estacion("Juarez", (float(379 / 536), float(18 / 603)), localizacion=(19.433224984330685, -99.14767631586872), pos_nombre=(float(385/536),float(25/603)), color=(141, 137, 38))
est_ninos_heroes = Estacion("Niños Heroes", (float(379 / 536), float(114 / 603)), localizacion=(19.419454817341986, -99.15040111837523), pos_nombre=(float(389/536),float(118/603)), color=(141, 137, 38))
est_hospital_general = Estacion("Hospital General", (float(379 / 536), float(151 / 603)), localizacion=(19.413746714038908, -99.1532556164282), pos_nombre=(float(388/536),float(154/603)), color=(141, 137, 38))
est_etiopia = Estacion("Etiopia", (float(379 / 536), float(252 / 603)), localizacion=(19.3959806524957, -99.1560563262052), pos_nombre=(float(340/536),float(255/603)), color=(141, 137, 38))
est_eugenia = Estacion("Eugenia", (float(379 / 536), float(287 / 603)), localizacion=(19.386161986226156, -99.15719111448146), pos_nombre=(float(330/536),float(290/603)), color=(141, 137, 38))
est_division = Estacion("Division del Norte", (float(379 / 536), float(321 / 603)), localizacion=(19.379164189449618, -99.15947096057036), pos_nombre=(float(287/536),float(326/603)), color=(141, 137, 38))
est_coyoacan = Estacion("Coyoacan", (float(379 / 536), float(391 / 603)), localizacion=(19.361354022325525, -99.17086352615256), pos_nombre=(float(388/536),float(395/603)), color=(141, 137, 38))
est_viveros = Estacion("Viveros", (float(379 / 536), float(426 / 603)), localizacion=(19.35402753048502, -99.17540934797833), pos_nombre=(float(388/536),float(430/603)), color=(141, 137, 38))
est_ma_quevedo = Estacion("M. A. De Quevedo", (float(379 / 536), float(460 / 603)), localizacion=(19.34624575058007, -99.18076583360612), pos_nombre=(float(280/536),float(465/603)), color=(141, 137, 38))
est_copilco = Estacion("Copilco", (float(379 / 536), float(495 / 603)), localizacion=(19.33618215676557, -99.17705637212309), pos_nombre=(float(388/536),float(495/603)), color=(141, 137, 38))
est_universidad = Estacion("Universidad", (float(379 / 536), float(529 / 603)), localizacion=(19.32440723326762, -99.173907446492), pos_nombre=(float(388/536),float(529/603)), color=(141, 137, 38))

# Lineas y Cabeceras
l_7 = Linea.crear_linea(7, (est_barranca, est_polanco), (229, 129, 38), pos_cuadrado=(float(139/536), float(426/603)))
l_9 = Linea.crear_linea(9, (est_tacubaya, est_lazaro), (119, 66, 52), pos_cuadrado=(float(117/536), float(175/603)))
l_1 = Linea.crear_linea(1, (est_observatorio, est_balderas), (194, 60, 127), pos_cuadrado=(float(73/536), float(230/603)))
l_12 = Linea.crear_linea(12, (est_mixcoac, est_eje_central), (168, 140, 38), pos_cuadrado=(float(112/536), float(365/603)))
l_3 = Linea.crear_linea(3, (est_universidad, est_juarez), (141, 137, 38), pos_cuadrado=(float(365/536), float(538/603)))
# Transbordos
tacubaya_l7_l1 = Transbordo(est_tacubaya, l_7, l_1, 3)
tacubaya_l7_l9 = Transbordo(est_tacubaya, l_7, l_9, 4)
tacubaya_l9_l1 = Transbordo(est_tacubaya, l_9, l_1, 5)
mixcoac_l7_l12 = Transbordo(est_mixcoac, l_7, l_12, 4)
balderas_l3_l1 = Transbordo(est_balderas, l_3, l_1, 2)
centro_medico_l9_l3 = Transbordo(est_centro_medico, l_9, l_3, 4)
zapata_l12_l3 = Transbordo(est_zapata, l_12, l_3, 2.5)

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

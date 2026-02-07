porcentaje_de_la_habilidad = [None,0,10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]


tipo_documento = [
    None,
    "Cédula de ciudadanía (CC)",
    "Targeta de identidad (TI)",
    "Registro civil (RC)",
    "Cédula de extranjería (CE)",
    "Carné de identidad (CI)",
    "Documento nacional de identidad (DNI)",
]

TIPO_DOCUMENTO = []
for i in tipo_documento:
    if i == None:
        document = [None, "Seleccione..."]
    else:
        document = [i, i]
    TIPO_DOCUMENTO.append(document)

tipo_sexo = [None, "Masculino", "Femenino"]

TIPO_SEXO = []
for i in tipo_sexo:
    if i == None:
        sexx = [None, "Seleccione..."]
    else:
        sexx = [i, i]
    TIPO_SEXO.append(sexx)

tipo_sangre = [None, "O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-", "no informa"]

TIPO_SANGRE = []
for i in tipo_sangre:
    if i == None:
        sangre = [None, "Seleccione..."]
    else:
        sangre = [i, i]
    TIPO_SANGRE.append(sangre)

tipo_estado_civil = [
    None,
    "Madre soltera",
    "Religioso(a)",
    "Casado(a)",
    "Divorciado(a)",
    "Soltero(a)",
    "Union libre",
    "Viudo(a)",
]

ESTADO_CIVIL_TIPO = []
for i in tipo_estado_civil:
    if i == None:
        civil = [None, "Seleccione..."]
    else:
        civil = [i, i]
    ESTADO_CIVIL_TIPO.append(civil)

lib_militar = [
    None,
    "Primera clase",
    "Segunda clase",
]

LIBRETA_MILITAR_CLASE = []
for i in lib_militar:
    if i == None:
        militar = [None, "Seleccione..."]
    else:
        militar = [i, i]
    LIBRETA_MILITAR_CLASE.append(militar)

NACIONALIDAD_CLASE = []
for i in [None, "Estrangero", "Colombiano"]:
    if i == None:
        nacion = [None, "Seleccione..."]
    else:
        nacion = [i, i]
    NACIONALIDAD_CLASE.append(nacion)

grado_profesional = [
    None,
    "Diplomado",
    "Cursos y seminarios",
    "Educación básica y media",
    "Formación técnica",
    "Formación tecnológica",
    "Título Profesional",
    "Título de especialización",
    "Título de Maestría o magíster",
    "Título de doctorado o phd",
    "Posdoctorado",
]

modalidad_academica=[
    None,
    "Presencial",
    "Virtual",
    "Híbrido",
]

MODALIDAD_ACADEMICA = []
for i in modalidad_academica:
    if i == None:
        modalidad = [None, "Seleccione..."]
    else:
        modalidad = [i, i]
    MODALIDAD_ACADEMICA.append(modalidad)


GRADO_ACADEMICO_PROFESIONAL = []
for i in grado_profesional:
    if i == None:
        grado = [None, "Seleccione..."]
    else:
        grado = [i, i]
    GRADO_ACADEMICO_PROFESIONAL.append(grado)



egresado_con_distincion = [None, "Si", "No"]

GRADUADO_CON_DISTINCION = []
for i in egresado_con_distincion:
    if i == None:
        grad_ditincion = [None, "Seleccione..."]
    else:
        grad_ditincion = [i, i]
    GRADUADO_CON_DISTINCION.append(grad_ditincion)

esgraduado_unieversitario = [None, "Si", "No"]

ES_GRADUADO_UNIVERSITARIO = []
for i in esgraduado_unieversitario:
    if i == None:
        grad_univ = [None, "Seleccione..."]
    else:
        grad_univ = [i, i]
    ES_GRADUADO_UNIVERSITARIO.append(grad_univ)

modalidad_empresa_laboral = [None, "Privada", "Publica", "Independiente"]

TIPO_DE_EMPRESA_LABORAL = []
for i in modalidad_empresa_laboral:
    if i == None:
        tipo_empresa = [None, "Seleccione..."]
    else:
        tipo_empresa = [i, i]
    TIPO_DE_EMPRESA_LABORAL.append(tipo_empresa)

tipo_contrato_con_empresa_laboral = [
    None,
    "Término fijo",
    "Término indefinido",
    "Obra o labor",
    "Orden de prestación de servicios",
    "Contrato de aprendisaje",
    "Contrato ocasional de trabajo",
]

TITPO_CONTRATO_EMPRESA_LABORAL = []
for i in tipo_contrato_con_empresa_laboral:
    if i == None:
        tipo_contrato_empresa = [None, "Seleccione..."]
    else:
        tipo_contrato_empresa = [i, i]
    TITPO_CONTRATO_EMPRESA_LABORAL.append(tipo_contrato_empresa)


tipo_del_evento_cientifico = [
    None,
    "Conferencias",
    "Congresos",
    "Simposios",
    "Seminarios",
    "Talleres",
    "Foros",
    "Coloquios",
    "Jornadas",
    "Mesas redondas",
    "Presentaciones de pósteres",
    "Webinars",
    "Cursos cortos",
    "Reuniones anuales",
    "Cumbres",
    "Hackatones",
    "Paneles de discusión",
    "Clínicas científicas",
    "Feria de ciencias",
    "Escuelas de verano",
]
TIPO_EVENTO_CIENTIFICO = []
for i in tipo_del_evento_cientifico:
    if i == None:
        tipo_evento = [None, "Seleccione..."]
    else:
        tipo_evento = [i, i]
    TIPO_EVENTO_CIENTIFICO.append(tipo_evento)


rol_del_evento_cientifico = [
    None,
    "Conferencista principal",
    "Ponente",
    "Moderador",
    "Panelista",
    "Miembro del comité organizador",
    "Revisor científico",
    "Expositor de póster",
    "Asistente",
    "Miembro del comité científico",
    "Evaluador de trabajos",
    "Presentador de taller",
    "Miembro del comité técnico",
    "Responsable de logística",
    "Moderador de mesa redonda",
    "Responsable de relaciones públicas",
    "Miembro del equipo de comunicación",
    "Traductor o intérprete",
    "Colaborador en redes sociales",
    "Instructor de tutorial",
    "Participante en discusión",
]
MODALIDAD_EVENTO_CIENTIFICO = []
for i in rol_del_evento_cientifico:
    if i == None:
        rol_evento = [None, "Seleccione..."]
    else:
        rol_evento = [i, i]
    MODALIDAD_EVENTO_CIENTIFICO.append(rol_evento)

NIVEL_SUFICIENCIA_INGLES = []
for i in porcentaje_de_la_habilidad:
    if i == None:
        idioma = [None, "Seleccione..."]
    else:
        idioma = [i, i]
    NIVEL_SUFICIENCIA_INGLES.append(idioma)


nivel_de_ingles = [None, "A1", "A2", "B1", "B2", "C1", "C2"]
NIVEL_INGLES_CERTIFICADO = []
for i in nivel_de_ingles:
    if i == None:
        nivel_idioma = [None, "Seleccione..."]
    else:
        nivel_idioma = [i, i]
    NIVEL_INGLES_CERTIFICADO.append(nivel_idioma)



departamentos_colombia = [
    None,
    "Amazonas",
    "Antioquia",
    "Arauca",
    "Atlántico",
    "Bolívar",
    "Boyacá",
    "Caldas",
    "Caquetá",
    "Casanare",
    "Cauca",
    "Cesar",
    "Chocó",
    "Córdoba",
    "Cundinamarca",
    "Guainía",
    "Guaviare",
    "Huila",
    "La Guajira",
    "Magdalena",
    "Meta",
    "Nariño",
    "Norte de Santander",
    "Putumayo",
    "Quindío",
    "Risaralda",
    "San Andrés y Providencia",
    "Santander",
    "Sucre",
    "Tolima",
    "Valle del Cauca",
    "Vaupés",
    "Vichada",
    "Otra"
]

DEPARTAMENTOS_COLOMBIA = []
for i in departamentos_colombia:
    if i == None:
        departamentos = [None, "Seleccione..."]
    else:
        departamentos = [i, i]
    DEPARTAMENTOS_COLOMBIA.append(departamentos)


paises_del_mundo = [
    None,
    "Afganistán",
    "Albania",
    "Alemania",
    "Andorra",
    "Angola",
    "Antigua y Barbuda",
    "Arabia Saudita",
    "Argelia",
    "Argentina",
    "Armenia",
    "Australia",
    "Austria",
    "Azerbaiyán",
    "Bahamas",
    "Bangladés",
    "Barbados",
    "Baréin",
    "Bélgica",
    "Belice",
    "Benín",
    "Bielorrusia",
    "Birmania",
    "Bolivia",
    "Bosnia y Herzegovina",
    "Botsuana",
    "Brasil",
    "Brunéi",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Bután",
    "Cabo Verde",
    "Camboya",
    "Camerún",
    "Canadá",
    "Catar",
    "Chad",
    "Chile",
    "China",
    "Chipre",
    "Colombia",
    "Comoras",
    "Corea del Norte",
    "Corea del Sur",
    "Costa Rica",
    "Costa de Marfil",
    "Croacia",
    "Cuba",
    "Dinamarca",
    "Dominica",
    "Ecuador",
    "Egipto",
    "El Salvador",
    "Emiratos Árabes Unidos",
    "Eritrea",
    "Eslovaquia",
    "Eslovenia",
    "España",
    "Estados Unidos",
    "Estonia",
    "Esuatini",
    "Etiopía",
    "Filipinas",
    "Finlandia",
    "Fiyi",
    "Francia",
    "Gabón",
    "Gambia",
    "Georgia",
    "Ghana",
    "Granada",
    "Grecia",
    "Guatemala",
    "Guinea",
    "Guinea-Bisáu",
    "Guinea Ecuatorial",
    "Guyana",
    "Haití",
    "Honduras",
    "Hungría",
    "India",
    "Indonesia",
    "Irak",
    "Irán",
    "Irlanda",
    "Islandia",
    "Islas Marshall",
    "Islas Salomón",
    "Israel",
    "Italia",
    "Jamaica",
    "Japón",
    "Jordania",
    "Kazajistán",
    "Kenia",
    "Kirguistán",
    "Kiribati",
    "Kuwait",
    "Laos",
    "Lesoto",
    "Letonia",
    "Líbano",
    "Liberia",
    "Libia",
    "Liechtenstein",
    "Lituania",
    "Luxemburgo",
    "Madagascar",
    "Malasia",
    "Malaui",
    "Maldivas",
    "Malí",
    "Malta",
    "Marruecos",
    "Mauricio",
    "Mauritania",
    "México",
    "Micronesia",
    "Moldavia",
    "Mónaco",
    "Mongolia",
    "Montenegro",
    "Mozambique",
    "Namibia",
    "Nauru",
    "Nepal",
    "Nicaragua",
    "Níger",
    "Nigeria",
    "Noruega",
    "Nueva Zelanda",
    "Omán",
    "Países Bajos",
    "Pakistán",
    "Palaos",
    "Panamá",
    "Papúa Nueva Guinea",
    "Paraguay",
    "Perú",
    "Polonia",
    "Portugal",
    "Reino Unido",
    "República Centroafricana",
    "República Checa",
    "República del Congo",
    "República Democrática del Congo",
    "República Dominicana",
    "Ruanda",
    "Rumanía",
    "Rusia",
    "Samoa",
    "San Cristóbal y Nieves",
    "San Marino",
    "San Vicente y las Granadinas",
    "Santa Lucía",
    "Santo Tomé y Príncipe",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leona",
    "Singapur",
    "Siria",
    "Somalia",
    "Sri Lanka",
    "Sudáfrica",
    "Sudán",
    "Sudán del Sur",
    "Suecia",
    "Suiza",
    "Surinam",
    "Tailandia",
    "Tanzania",
    "Tayikistán",
    "Timor Oriental",
    "Togo",
    "Tonga",
    "Trinidad y Tobago",
    "Túnez",
    "Turkmenistán",
    "Turquía",
    "Tuvalu",
    "Ucrania",
    "Uganda",
    "Uruguay",
    "Uzbekistán",
    "Vanuatu",
    "Vaticano",
    "Venezuela",
    "Vietnam",
    "Yemen",
    "Yibuti",
    "Zambia",
    "Zimbabue",
]

LISTA_PAISES_MUNDO = []
for i in paises_del_mundo:
    if i == None:
        paises = [None, "Seleccione..."]
    else:
        paises = [i, i]
    LISTA_PAISES_MUNDO.append(paises)

competencias_tecnicas_computacionales = [
    None,
    # Lenguajes de programación
    "Python",
    "JavaScript",
    "Java",
    "C#",
    "C++",
    "TypeScript",
    "Go",
    "Ruby",
    "PHP",
    "Kotlin",
    "Swift",
    "Rust",

    # Desarrollo web frontend
    "HTML5",
    "CSS3",
    "React",
    "Angular",
    "Vue.js",
    "Svelte",
    "Bootstrap",
    "Tailwind CSS",

    # Desarrollo web backend
    "Django",
    "Flask",
    "Node.js",
    "Express.js",
    "Spring Boot",
    "ASP.NET Core",
    "Laravel",
    "Ruby on Rails",

    # Bases de datos
    "MySQL",
    "PostgreSQL",
    "SQLite",
    "MongoDB",
    "Redis",
    "Firebase",

    # DevOps y Cloud
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",
    "GitLab",
    "CI/CD",
    "AWS",
    "Google Cloud Platform",
    "Microsoft Azure",

    # Mobile / aplicaciones
    "React Native",
    "Flutter",
    "Android Studio",
    "Xcode",

    # Big Data / ML / AI
    "TensorFlow",
    "PyTorch",
    "Pandas",
    "NumPy",
    "Scikit-Learn",
    "Apache Spark",

    # Testing y Calidad de Software
    "Unit Testing",
    "Selenium",
    "Jest",
    "pytest",

    # Otras habilidades técnicas útiles
    "REST API",
    "GraphQL",
    "Agile/Scrum",
    "TDD (Test-Driven Development)",
    "Clean Code",
    "LaTeX",
    "Wolfram Matemática"
    "Excel",
    "Power BI"
]

COMPETENCIAS_TECNICAS_COMPUTACIONALES = []
for i in competencias_tecnicas_computacionales:
    if i == None:
        competencia = [None, "Seleccione..."]
    else:
        competencia = [i, i]
    COMPETENCIAS_TECNICAS_COMPUTACIONALES.append(competencia)

DOMINIO_BASICO_COMPOTENCIA = []
for i in porcentaje_de_la_habilidad:
    if i == None:
        porcentaje_competencia = [None, "Seleccione..."]
    else:
        porcentaje_competencia = [i, i]
    DOMINIO_BASICO_COMPOTENCIA.append(porcentaje_competencia)

DOMINIO_MEDIO_COMPOTENCIA = []
for i in porcentaje_de_la_habilidad:
    if i == None:
        porcentaje_competencia = [None, "Seleccione..."]
    else:
        porcentaje_competencia = [i, i]
    DOMINIO_MEDIO_COMPOTENCIA.append(porcentaje_competencia)

DOMINIO_AVANZADO_COMPOTENCIA = []
for i in porcentaje_de_la_habilidad:
    if i == None:
        porcentaje_competencia = [None, "Seleccione..."]
    else:
        porcentaje_competencia = [i, i]
    DOMINIO_AVANZADO_COMPOTENCIA.append(porcentaje_competencia)

dominio_lenguejes = [
    None,
    "Inglés",
    "Mandarín",
    "Hindi",
    "Español",
    "Francés",
    "Árabe",
    "Bengalí",
    "Portugués",
    "Ruso",
    "Urdu",
    "Alemán",
    "Japonés",
    "Coreano",
    "Italiano",
    "Turco",
    "Vietnamita",
    "Persa (Farsi)",
    "Suajili",
    "Tamil",
    "Telugu",
    "Polaco",
    "Ucraniano",
    "Neerlandés",
    "Griego",
    "Sueco",
    "Noruego",
    "Danés",
    "Finlandés",
    "Húngaro",
    "Rumano",
    "Quechua",
    "Guaraní",
    "Aimara",
    "Náhuatl",
    "Maya",
    "Mapudungun",
    "Hausa",
    "Yoruba",
    "Zulu",
    "Xhosa"
]


DOMINIO_LENGUAGES = []
for i in dominio_lenguejes:
    if i == None:
        lenguajes = [None, "Seleccione..."]
    else:
        lenguajes = [i, i]
    DOMINIO_LENGUAGES.append(lenguajes)
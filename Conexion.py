import mysql.connector
from mysql.connector import errors
import config


def conectar():
    """Conectar con la base de datos y devolver un obj conexion."""
    try:
        conn = mysql.connector.connect(**config.credenciales)
    except errors.DatabaseError as err:
        print("Error al conectar.", err)
    else:
        print("CONECTADO!!")
        return conn


def create_if_not_exists():
    create_database = "CREATE DATABASE IF NOT EXISTS %s" % config.credenciales["database"]
    create_tables = """
        CREATE TABLE IF NOT EXISTS `calendario` (
            `idcalendario` int NOT NULL,
            PRIMARY KEY (`idcalendario`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

   CREATE TABLE IF NOT EXISTS `fecha` (
    `idfecha` int NOT NULL AUTO_INCREMENT,
    `fecha` date NOT NULL,
    PRIMARY KEY (`idfecha`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE IF NOT EXISTS `hora` (
    `idhora` int NOT NULL AUTO_INCREMENT,
    `hora` time DEFAULT NULL,
    PRIMARY KEY (`idhora`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


        CREATE TABLE IF NOT EXISTS `eventos` (
            `ideventos` int NOT NULL AUTO_INCREMENT,
            `titulo` varchar(100) DEFAULT NULL,
            `duracion` time DEFAULT NULL,
            `hora_idhora` int NOT NULL,
            `fecha_idfecha` int NOT NULL,
            `calendario_idcalendario` int NOT NULL,
            `importancia` varchar(45) DEFAULT NULL,
            `descripcion` varchar(150) DEFAULT NULL,
            `etiquetas` varchar(45) DEFAULT NULL,
            PRIMARY KEY (`ideventos`),
            KEY `fk_eventos_hora1_idx` (`hora_idhora`),
            KEY `fk_eventos_fecha1_idx` (`fecha_idfecha`),
            KEY `fk_eventos_calendario1_idx` (`calendario_idcalendario`),
            CONSTRAINT `fk_eventos_calendario1` FOREIGN KEY (`calendario_idcalendario`) REFERENCES `calendario` (`idcalendario`),
            CONSTRAINT `fk_eventos_fecha1` FOREIGN KEY (`fecha_idfecha`) REFERENCES `fecha` (`idfecha`),
            CONSTRAINT `fk_eventos_hora1` FOREIGN KEY (`hora_idhora`) REFERENCES `hora` (`idhora`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

        CREATE TABLE IF NOT EXISTS `etiquetas` (
            `id_etiquetas` int NOT NULL AUTO_INCREMENT,
            `nombre` varchar(15) DEFAULT NULL,
            PRIMARY KEY (`id_etiquetas`),
            UNIQUE KEY `id_etiquetas_UNIQUE` (`id_etiquetas`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

        CREATE TABLE IF NOT EXISTS `etiquetas_evento` (
            `id_etiqueta_evento` int NOT NULL AUTO_INCREMENT,
            `id_etiquetas` int NOT NULL,
            `id_evento` int NOT NULL,
            PRIMARY KEY (`id_etiqueta_evento`),
            KEY `fk_eventos_has_etiquetas_etiquetas1_idx` (`id_etiquetas`),
            KEY `fk_eventos_has_etiquetas_eventos` (`id_evento`),
            CONSTRAINT `fk_eventos_has_etiquetas_etiquetas1` FOREIGN KEY (`id_etiquetas`) REFERENCES `etiquetas` (`id_etiquetas`),
            CONSTRAINT `fk_eventos_has_etiquetas_eventos` FOREIGN KEY (`id_evento`) REFERENCES `eventos` (`ideventos`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
    """
    try:
        conn = mysql.connector.connect(user=config.credenciales["user"],
                                       password=config.credenciales["password"],
                                       host="127.0.0.1")
        cur = conn.cursor()
        cur.execute(create_database)
        cur.execute("USE %s" % config.credenciales["database"])
          # Crear las tablas
        for result in cur.execute(create_tables, multi=True):
            if result.with_rows:
                result.fetchall()

        #cur.execute(create_tables)
        conn.commit()
        conn.close()
    except errors.DatabaseError as err:
        print("Error al conectar o crear la base de datos.", err)
        raise

def nuevo_evento(evento):
    # Insertar en la tabla fecha
    query_fecha = "INSERT INTO fecha (fecha) VALUES (%s)"
    conn = conectar()
    cur = conn.cursor()
    cur.execute(query_fecha, (evento.fecha,))
    fecha_id = cur.lastrowid#obtiene el id que se

    # Insertar en la tabla hora
    query_hora = "INSERT INTO hora (hora) VALUES (%s)"
    cur.execute(query_hora, (evento.hora,))
    hora_id = cur.lastrowid #obtiene el id que se creo

  
    cur.execute("SELECT idcalendario FROM calendario WHERE idcalendario = 1")
    calendario_id = cur.fetchone()

    if calendario_id is None:
    # Si no existe un registro, crea uno con el valor 1
       query_calendario = "INSERT INTO calendario (idcalendario) VALUES (1)"
       cur.execute(query_calendario)
    else:
    # Si ya existe un registro, obtén el valor del id existente
       calendario_id = 1  # Como ya sabemos que existe el registro con idcalendario = 1, asignamos este valor a calendario_id
    
    conn.commit()
    conn.close()

def obtener_eventos():
    try:
        conn = conectar()
        cur = conn.cursor()
        query = """SELECT e.titulo, f.fecha, h.hora, e.duracion, e.descripcion, e.importancia, e.etiquetas
        FROM eventos e
        JOIN fecha f ON e.fecha_idfecha = f.idfecha
        JOIN hora h ON e.hora_idhora = h.idhora"""
        cur.execute(query)
        eventos = cur.fetchall()

        print(eventos)
        conn.close()
        return eventos
    except mysql.connector.Error as error:
        raise Exception(f"Error al obtener los eventos de la base de datos: {error}")

def actualizar_evento(titulo_evento, evento):
    query = """
        UPDATE eventos
        SET titulo = %s, fecha_idfecha = %s, hora_idhora = %s, duracion = %s, descripcion = %s, importancia = %s, etiquetas = %s
        WHERE titulo = %s
    """
    conn = conectar()
    cur = conn.cursor()
    cur.execute(query, (evento.titulo, evento.fecha, evento.hora, evento.duracion, evento.descripcion,
                        evento.importancia, evento.etiquetas, titulo_evento))
    conn.commit()
    conn.close()


  #esperar a cargar eventos

def eliminar_evento(tituloEvento):
    query = "DELETE FROM eventos WHERE titulo = %s"
    conn = conectar()
    cur = conn.cursor()
    cur.execute(query, (tituloEvento,))
    conn.commit()
    conn.close()
    
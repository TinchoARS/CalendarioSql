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
        print("Holaaa conecte perri")
        return conn


def create_if_not_exists():
    create_database = "CREATE DATABASE IF NOT EXISTS %s" % config.credenciales["database"]
    create_tables = """
        CREATE TABLE IF NOT EXISTS `calendario` (
            `idcalendario` int NOT NULL,
            PRIMARY KEY (`idcalendario`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

        CREATE TABLE IF NOT EXISTS `fecha` (
            `idfecha` int NOT NULL,
            `fecha` date NOT NULL,
            PRIMARY KEY (`idfecha`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

        CREATE TABLE IF NOT EXISTS `hora` (
            `idhora` int NOT NULL,
            `fecha_idfecha` int NOT NULL,
            PRIMARY KEY (`idhora`,`fecha_idfecha`),
            KEY `fk_hora_fecha1_idx` (`fecha_idfecha`),
            CONSTRAINT `fk_hora_fecha1` FOREIGN KEY (`fecha_idfecha`) REFERENCES `fecha` (`idfecha`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

        CREATE TABLE IF NOT EXISTS `eventos` (
            `ideventos` int NOT NULL AUTO_INCREMENT,
            `titulo` varchar(100) DEFAULT NULL,
            `duracion` time DEFAULT NULL,
            `descripcion` varchar(150) DEFAULT NULL,
            `recordatorio` datetime DEFAULT NULL,
            `hora_idhora` int NOT NULL,
            `fecha_idfecha` int NOT NULL,
            `calendario_idcalendario` int NOT NULL,
            `importancia` varchar(45) DEFAULT NULL,
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
                                       host="localhost")
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

create_if_not_exists()
conectar()
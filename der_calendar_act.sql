-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: calendario
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `calendario`
--

DROP TABLE IF EXISTS `calendario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `calendario` (
  `idcalendario` int NOT NULL,
  PRIMARY KEY (`idcalendario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calendario`
--

LOCK TABLES `calendario` WRITE;
/*!40000 ALTER TABLE `calendario` DISABLE KEYS */;
/*!40000 ALTER TABLE `calendario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `etiquetas`
--

DROP TABLE IF EXISTS `etiquetas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `etiquetas` (
  `id_etiquetas` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id_etiquetas`),
  UNIQUE KEY `id_etiquetas_UNIQUE` (`id_etiquetas`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `etiquetas`
--

LOCK TABLES `etiquetas` WRITE;
/*!40000 ALTER TABLE `etiquetas` DISABLE KEYS */;
/*!40000 ALTER TABLE `etiquetas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `etiquetas_evento`
--

DROP TABLE IF EXISTS `etiquetas_evento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `etiquetas_evento` (
  `id_etiqueta_evento` int NOT NULL AUTO_INCREMENT,
  `id_etiquetas` int NOT NULL,
  `id_evento` int NOT NULL,
  PRIMARY KEY (`id_etiqueta_evento`),
  KEY `fk_eventos_has_etiquetas_etiquetas1_idx` (`id_etiquetas`),
  KEY `fk_eventos_has_etiquetas_eventos` (`id_evento`),
  CONSTRAINT `fk_eventos_has_etiquetas_etiquetas1` FOREIGN KEY (`id_etiquetas`) REFERENCES `etiquetas` (`id_etiquetas`),
  CONSTRAINT `fk_eventos_has_etiquetas_eventos` FOREIGN KEY (`id_evento`) REFERENCES `eventos` (`ideventos`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `etiquetas_evento`
--

LOCK TABLES `etiquetas_evento` WRITE;
/*!40000 ALTER TABLE `etiquetas_evento` DISABLE KEYS */;
/*!40000 ALTER TABLE `etiquetas_evento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventos`
--

DROP TABLE IF EXISTS `eventos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventos` (
  `ideventos` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(100) DEFAULT NULL,
  `duracion` time DEFAULT NULL,
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos`
--

LOCK TABLES `eventos` WRITE;
/*!40000 ALTER TABLE `eventos` DISABLE KEYS */;
/*!40000 ALTER TABLE `eventos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fecha`
--

DROP TABLE IF EXISTS `fecha`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fecha` (
  `idfecha` int NOT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`idfecha`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fecha`
--

LOCK TABLES `fecha` WRITE;
/*!40000 ALTER TABLE `fecha` DISABLE KEYS */;
/*!40000 ALTER TABLE `fecha` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hora`
--

DROP TABLE IF EXISTS `hora`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hora` (
  `idhora` int NOT NULL,
  `fecha_idfecha` int NOT NULL,
  PRIMARY KEY (`idhora`,`fecha_idfecha`),
  KEY `fk_hora_fecha1_idx` (`fecha_idfecha`),
  CONSTRAINT `fk_hora_fecha1` FOREIGN KEY (`fecha_idfecha`) REFERENCES `fecha` (`idfecha`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hora`
--

LOCK TABLES `hora` WRITE;
/*!40000 ALTER TABLE `hora` DISABLE KEYS */;
/*!40000 ALTER TABLE `hora` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-17 19:02:48

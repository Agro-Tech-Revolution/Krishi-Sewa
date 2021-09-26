-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: soil_analyzer
-- ------------------------------------------------------
-- Server version	8.0.20

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
-- Table structure for table `admins_ticket`
--

DROP TABLE IF EXISTS `admins_ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins_ticket` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `link` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `category` varchar(10) NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `status` varchar(15) NOT NULL,
  `ticket_to_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admins_ticket_ticket_to_id_e332d1da_fk_auth_user_id` (`ticket_to_id`),
  CONSTRAINT `admins_ticket_ticket_to_id_e332d1da_fk_auth_user_id` FOREIGN KEY (`ticket_to_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins_ticket`
--

LOCK TABLES `admins_ticket` WRITE;
/*!40000 ALTER TABLE `admins_ticket` DISABLE KEYS */;
INSERT INTO `admins_ticket` VALUES (2,'Test','/farmers/profile/8','Test Details','User','2021-09-23 15:53:29.180401','Pending',8);
/*!40000 ALTER TABLE `admins_ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admins_ticketresponse`
--

DROP TABLE IF EXISTS `admins_ticketresponse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins_ticketresponse` (
  `id` int NOT NULL AUTO_INCREMENT,
  `response` longtext NOT NULL,
  `response_date` datetime(6) NOT NULL,
  `response_by_id` int DEFAULT NULL,
  `ticket_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admins_ticketresponse_response_by_id_bb545d52_fk_auth_user_id` (`response_by_id`),
  KEY `admins_ticketresponse_ticket_id_b5831192_fk_admins_ticket_id` (`ticket_id`),
  CONSTRAINT `admins_ticketresponse_response_by_id_bb545d52_fk_auth_user_id` FOREIGN KEY (`response_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `admins_ticketresponse_ticket_id_b5831192_fk_admins_ticket_id` FOREIGN KEY (`ticket_id`) REFERENCES `admins_ticket` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins_ticketresponse`
--

LOCK TABLES `admins_ticketresponse` WRITE;
/*!40000 ALTER TABLE `admins_ticketresponse` DISABLE KEYS */;
INSERT INTO `admins_ticketresponse` VALUES (3,'Why haven\'t you responded?','2021-09-23 15:53:55.394738',2,2);
/*!40000 ALTER TABLE `admins_ticketresponse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_feedback`
--

DROP TABLE IF EXISTS `api_feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_feedback` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `feedback_type` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_feedback`
--

LOCK TABLES `api_feedback` WRITE;
/*!40000 ALTER TABLE `api_feedback` DISABLE KEYS */;
INSERT INTO `api_feedback` VALUES (1,'Test','test@email.com','Comments','this is a comment'),(2,'Anuj Maharjan','test@test.com','Comments','This is a feedback'),(3,'Anuj','test@test.com','Bug Reports','report'),(4,'Anuj Maharjan','test@test.com','Questions','What is this?'),(5,'Anuj','anuj@email.com','Comments','haha');
/*!40000 ALTER TABLE `api_feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_profile`
--

DROP TABLE IF EXISTS `api_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_profile` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_type` varchar(50) NOT NULL,
  `profile_pic` varchar(500) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `contact` int DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `bio` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_profile_user_id_41309820_uniq` (`user_id`),
  CONSTRAINT `api_profile_user_id_41309820_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_profile`
--

LOCK TABLES `api_profile` WRITE;
/*!40000 ALTER TABLE `api_profile` DISABLE KEYS */;
INSERT INTO `api_profile` VALUES (1,'Admins','static/profile_pic/default_profile.jpg',2,NULL,'',''),(2,'Farmers','static/profile_pic/default_profile.jpg',3,NULL,NULL,NULL),(5,'Farmers','static/profile_pic/default_profile.jpg',6,NULL,NULL,''),(6,'Farmers','static/profile_pic/default_profile.jpg',7,NULL,NULL,''),(7,'Farmers','static/profile_pic/peaky blinders_JDHUgjn.jpg',8,NULL,NULL,''),(8,'Farmers','static/profile_pic/default_profile.jpg',9,NULL,NULL,''),(9,'Buyers','static/profile_pic/default_profile.jpg',10,NULL,NULL,''),(10,'Buyers','static/profile_pic/default_profile.jpg',11,NULL,NULL,''),(11,'Buyers','static/profile_pic/default_profile.jpg',12,NULL,NULL,''),(12,'Buyers','static/profile_pic/default_profile.jpg',13,NULL,NULL,''),(13,'Buyers','static/profile_pic/default_profile.jpg',14,NULL,NULL,''),(14,'Vendors','static/profile_pic/default_profile.jpg',15,NULL,NULL,''),(15,'Vendors','static/profile_pic/default_profile.jpg',16,NULL,NULL,'');
/*!40000 ALTER TABLE `api_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_reportuser`
--

DROP TABLE IF EXISTS `api_reportuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_reportuser` (
  `id` int NOT NULL AUTO_INCREMENT,
  `report_category` varchar(50) NOT NULL,
  `report_description` varchar(200) NOT NULL,
  `reported_date` datetime(6) NOT NULL,
  `reported_by_id` int DEFAULT NULL,
  `reported_user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_reportuser_reported_by_id_4c396c65_fk_auth_user_id` (`reported_by_id`),
  KEY `api_reportuser_reported_user_id_b692a593_fk_auth_user_id` (`reported_user_id`),
  CONSTRAINT `api_reportuser_reported_by_id_4c396c65_fk_auth_user_id` FOREIGN KEY (`reported_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `api_reportuser_reported_user_id_b692a593_fk_auth_user_id` FOREIGN KEY (`reported_user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_reportuser`
--

LOCK TABLES `api_reportuser` WRITE;
/*!40000 ALTER TABLE `api_reportuser` DISABLE KEYS */;
INSERT INTO `api_reportuser` VALUES (1,'Fake Account','This is fake','2021-09-17 07:06:08.464939',3,8);
/*!40000 ALTER TABLE `api_reportuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=133 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add profile',7,'add_profile'),(26,'Can change profile',7,'change_profile'),(27,'Can delete profile',7,'delete_profile'),(28,'Can view profile',7,'view_profile'),(29,'Can add report user',8,'add_reportuser'),(30,'Can change report user',8,'change_reportuser'),(31,'Can delete report user',8,'delete_reportuser'),(32,'Can view report user',8,'view_reportuser'),(33,'Can add feedback',9,'add_feedback'),(34,'Can change feedback',9,'change_feedback'),(35,'Can delete feedback',9,'delete_feedback'),(36,'Can view feedback',9,'view_feedback'),(37,'Can add products',10,'add_products'),(38,'Can change products',10,'change_products'),(39,'Can delete products',10,'delete_products'),(40,'Can view products',10,'view_products'),(41,'Can add note',11,'add_note'),(42,'Can change note',11,'change_note'),(43,'Can delete note',11,'delete_note'),(44,'Can view note',11,'view_note'),(45,'Can add product comment',12,'add_productcomment'),(46,'Can change product comment',12,'change_productcomment'),(47,'Can delete product comment',12,'delete_productcomment'),(48,'Can view product comment',12,'view_productcomment'),(49,'Can add product report',13,'add_productreport'),(50,'Can change product report',13,'change_productreport'),(51,'Can delete product report',13,'delete_productreport'),(52,'Can view product report',13,'view_productreport'),(53,'Can add product stock',14,'add_productstock'),(54,'Can change product stock',14,'change_productstock'),(55,'Can delete product stock',14,'delete_productstock'),(56,'Can view product stock',14,'view_productstock'),(57,'Can add product sold',15,'add_productsold'),(58,'Can change product sold',15,'change_productsold'),(59,'Can delete product sold',15,'delete_productsold'),(60,'Can view product sold',15,'view_productsold'),(61,'Can add products for sale',16,'add_productsforsale'),(62,'Can change products for sale',16,'change_productsforsale'),(63,'Can delete products for sale',16,'delete_productsforsale'),(64,'Can view products for sale',16,'view_productsforsale'),(65,'Can add production',17,'add_production'),(66,'Can change production',17,'change_production'),(67,'Can delete production',17,'delete_production'),(68,'Can view production',17,'view_production'),(69,'Can add home expenses',18,'add_homeexpenses'),(70,'Can change home expenses',18,'change_homeexpenses'),(71,'Can delete home expenses',18,'delete_homeexpenses'),(72,'Can view home expenses',18,'view_homeexpenses'),(73,'Can add expenses',19,'add_expenses'),(74,'Can change expenses',19,'change_expenses'),(75,'Can delete expenses',19,'delete_expenses'),(76,'Can view expenses',19,'view_expenses'),(77,'Can add npk test',20,'add_npktest'),(78,'Can change npk test',20,'change_npktest'),(79,'Can delete npk test',20,'delete_npktest'),(80,'Can view npk test',20,'view_npktest'),(81,'Can add image test',21,'add_imagetest'),(82,'Can change image test',21,'change_imagetest'),(83,'Can delete image test',21,'delete_imagetest'),(84,'Can view image test',21,'view_imagetest'),(85,'Can add equipment',22,'add_equipment'),(86,'Can change equipment',22,'change_equipment'),(87,'Can delete equipment',22,'delete_equipment'),(88,'Can view equipment',22,'view_equipment'),(89,'Can add equipment report',23,'add_equipmentreport'),(90,'Can change equipment report',23,'change_equipmentreport'),(91,'Can delete equipment report',23,'delete_equipmentreport'),(92,'Can view equipment report',23,'view_equipmentreport'),(93,'Can add buy details',24,'add_buydetails'),(94,'Can change buy details',24,'change_buydetails'),(95,'Can delete buy details',24,'delete_buydetails'),(96,'Can view buy details',24,'view_buydetails'),(97,'Can add equipment to display',25,'add_equipmenttodisplay'),(98,'Can change equipment to display',25,'change_equipmenttodisplay'),(99,'Can delete equipment to display',25,'delete_equipmenttodisplay'),(100,'Can view equipment to display',25,'view_equipmenttodisplay'),(101,'Can add rent details',26,'add_rentdetails'),(102,'Can change rent details',26,'change_rentdetails'),(103,'Can delete rent details',26,'delete_rentdetails'),(104,'Can view rent details',26,'view_rentdetails'),(105,'Can add equipment comment',27,'add_equipmentcomment'),(106,'Can change equipment comment',27,'change_equipmentcomment'),(107,'Can delete equipment comment',27,'delete_equipmentcomment'),(108,'Can view equipment comment',27,'view_equipmentcomment'),(109,'Can add ticket',28,'add_ticket'),(110,'Can change ticket',28,'change_ticket'),(111,'Can delete ticket',28,'delete_ticket'),(112,'Can view ticket',28,'view_ticket'),(113,'Can add ticket response',29,'add_ticketresponse'),(114,'Can change ticket response',29,'change_ticketresponse'),(115,'Can delete ticket response',29,'delete_ticketresponse'),(116,'Can view ticket response',29,'view_ticketresponse'),(117,'Can add chat room',30,'add_chatroom'),(118,'Can change chat room',30,'change_chatroom'),(119,'Can delete chat room',30,'delete_chatroom'),(120,'Can view chat room',30,'view_chatroom'),(121,'Can add messages',31,'add_messages'),(122,'Can change messages',31,'change_messages'),(123,'Can delete messages',31,'delete_messages'),(124,'Can view messages',31,'view_messages'),(125,'Can add Token',32,'add_token'),(126,'Can change Token',32,'change_token'),(127,'Can delete Token',32,'delete_token'),(128,'Can view Token',32,'view_token'),(129,'Can add token',33,'add_tokenproxy'),(130,'Can change token',33,'change_tokenproxy'),(131,'Can delete token',33,'delete_tokenproxy'),(132,'Can view token',33,'view_tokenproxy');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (2,'pbkdf2_sha256$216000$yAlRh6UjOkzl$TOUEK6Jot0hxCs1wCKc8DYU5JHg/rNDEKO1xHWyb8LY=','2021-09-25 16:50:10.562283',1,'sir_alex','Alex','Ferguson','alex@email.com',1,1,'2021-09-11 18:37:16.000000'),(3,'pbkdf2_sha256$216000$c6e5XvnKUdDw$odmQzRCa3tzNVG9kTqE6CNZtxgYJZRbUPVS/qT9Y1Z8=','2021-09-25 15:38:50.807164',0,'harry','Harry','Maguire','harry@gmail.com',0,1,'2021-09-11 18:38:34.000000'),(6,'pbkdf2_sha256$216000$xEE4Sy3ilTAM$dyclm5vZDuAqQTah216FNERw3pT5Cl5ALzewYVyV2Rc=','2021-09-23 12:06:20.203624',0,'rafael','Rafael','Varane','rafael@gmail.com',0,1,'2021-09-13 14:47:56.000000'),(7,'pbkdf2_sha256$216000$g2GIOfuPSA5H$CtoNhR+OAy7K/o67xOUpOieGRrQ9tVeg6SDb1GGfa3E=','2021-09-23 12:20:55.988641',0,'david','David','De Gea','david@gmail.com',0,1,'2021-09-13 15:56:50.000000'),(8,'pbkdf2_sha256$216000$4sH6qWHdzM72$0Vf5PwMaz16lAFVc5mlk17AB4oZ4XXp84kIKXqGKoJk=','2021-09-25 16:01:56.115758',0,'aaron','Aaron','Wan-Bissaka','aaron@gmail.com',0,1,'2021-09-17 06:49:39.000000'),(9,'pbkdf2_sha256$216000$ssrM0aP31XEy$i9/k3y43ltNIWT1l7BAh605mmeurQVcOnLMRAkV5NoI=','2021-09-23 12:20:24.316091',0,'bruno','Bruno','Fernandes','anjmhrjn1@gmail.com',0,1,'2021-09-17 06:58:17.000000'),(10,'pbkdf2_sha256$216000$N6u0TMUNesH0$4/2Pvv3zNiv69hscGpV9wflnjEEGmj7sH7Z5DaMzgj4=','2021-09-25 16:04:32.087739',0,'luke','Luke','Shaw','luke@gmail.com',0,1,'2021-09-23 05:22:04.000000'),(11,'pbkdf2_sha256$216000$GtdpwagKC4Q0$j1bGmm3eRGRRjh22GU6eKDRkO9Qy49T5UsNGFarm04g=','2021-09-23 13:26:24.747130',0,'scott','Scott','Mctominay','scott@gmail.com',0,1,'2021-09-23 05:22:47.000000'),(12,'pbkdf2_sha256$216000$pjtpSfQzQONT$mt5Chh19Qkp20djeO85h+GcDNN5chW944ETI/7nXXbs=','2021-09-23 13:42:04.024887',0,'nemanja','Nemanja','Matic','nemanja@gmail.com',0,1,'2021-09-23 05:23:39.000000'),(13,'pbkdf2_sha256$216000$3pywgy7MNZvI$VvSP+eF//Q11D8U/5thYN33+VmC+Z7Zz4KrvVvDG6qY=','2021-09-23 12:01:40.805780',0,'paul','Paul','Pogba','paul@gmail.com',0,1,'2021-09-23 05:24:33.000000'),(14,'pbkdf2_sha256$216000$I07dlMfyptnw$MVaZ9XJg0kqE3/16e0kiK+WyOg8dmulNOrRYtwO3/NM=','2021-09-23 13:43:01.682071',0,'jadon','Jadon','Sancho','jadon@gmail.com',0,1,'2021-09-23 05:25:20.000000'),(15,'pbkdf2_sha256$216000$ndEo2a1pATJz$V+LGzQ1ZQ+OUyW4iVOHaXzc/XZd9UywW9LJTCRfpJGk=','2021-09-25 16:48:56.800962',0,'cristiano','Cristiano','Ronaldo','cristiano@gmail.com',0,1,'2021-09-23 05:25:51.000000'),(16,'pbkdf2_sha256$216000$fYrUOtN22t44$rUEXBxSBx3vwNWqxk7h6ptnhfUfZCfemR60o1qFC4xs=','2021-09-23 13:44:43.008855',0,'marcus','Marcus','Rashford','marcus@gmail.com',0,1,'2021-09-23 05:26:35.000000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
INSERT INTO `authtoken_token` VALUES ('0eb95fd275e9011b8469a37889844b2d8a7f5d43','2021-09-13 14:47:57.038035',6),('12d2fae882e2544307da2f9decfe1d6f306d7b4f','2021-09-17 06:58:18.212486',9),('3017ac7f07ca1b061c24dda5ba96e9c5197fbbf0','2021-09-23 05:22:05.038765',10),('4f49365e3fc322c2e0b1f28551a3933267490380','2021-09-23 05:25:21.149745',14),('54174f6016c602b66d3461be685073d724c09d08','2021-09-23 05:22:47.767041',11),('5d498be25f60ba75829aa5009847000165eabb7f','2021-09-11 18:37:52.379285',2),('61fbd694e121e6bbd301c4f81d1966b1077a32d6','2021-09-13 15:56:50.336313',7),('6b661c4b8230f8ee479a362faa14d90788791381','2021-09-17 06:49:39.700202',8),('aaa5b7bf429dc20f63521d6754380ee89671530b','2021-09-23 05:26:35.851760',16),('ac5ab8101bc7a46004d9c21943e7f0cd04832989','2021-09-23 05:24:34.153560',13),('ae4520a1d1f2f3853c5e42276829aec49dd79af2','2021-09-23 05:25:51.965801',15),('b000bc030eb9f3788a0532c3c9e8eb2c59cfe82f','2021-09-11 18:38:34.419240',3),('bbb3bc9e12c380947d3214e4a5872781f128dbcf','2021-09-23 05:23:39.783024',12);
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_chatroom`
--

DROP TABLE IF EXISTS `chat_chatroom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_chatroom` (
  `room_code` varchar(8) NOT NULL,
  `first_user_id` int DEFAULT NULL,
  `second_user_id` int DEFAULT NULL,
  PRIMARY KEY (`room_code`),
  KEY `chat_chatroom_first_user_id_fc9d033d_fk_auth_user_id` (`first_user_id`),
  KEY `chat_chatroom_second_user_id_cb564d82_fk_auth_user_id` (`second_user_id`),
  CONSTRAINT `chat_chatroom_first_user_id_fc9d033d_fk_auth_user_id` FOREIGN KEY (`first_user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `chat_chatroom_second_user_id_cb564d82_fk_auth_user_id` FOREIGN KEY (`second_user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_chatroom`
--

LOCK TABLES `chat_chatroom` WRITE;
/*!40000 ALTER TABLE `chat_chatroom` DISABLE KEYS */;
INSERT INTO `chat_chatroom` VALUES ('AAPEDHBV',3,7),('DFFVTPQJ',15,15),('FJJDBGEH',6,6),('IMLLGMIT',7,7),('KJSDVWEZ',3,15),('KWEEKJMP',3,8),('MIFMSPVG',8,8),('QNUNYYGW',3,3),('RCEUOVZF',3,6),('TIBGDHOO',2,2),('ZQCXJHUV',3,2);
/*!40000 ALTER TABLE `chat_chatroom` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_messages`
--

DROP TABLE IF EXISTS `chat_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `message` longtext NOT NULL,
  `sent_date` datetime(6) NOT NULL,
  `room_code_id` varchar(8) NOT NULL,
  `sent_by_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `chat_messages_room_code_id_7cce1e97_fk_chat_chatroom_room_code` (`room_code_id`),
  KEY `chat_messages_sent_by_id_47eb32da_fk_auth_user_id` (`sent_by_id`),
  CONSTRAINT `chat_messages_room_code_id_7cce1e97_fk_chat_chatroom_room_code` FOREIGN KEY (`room_code_id`) REFERENCES `chat_chatroom` (`room_code`),
  CONSTRAINT `chat_messages_sent_by_id_47eb32da_fk_auth_user_id` FOREIGN KEY (`sent_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_messages`
--

LOCK TABLES `chat_messages` WRITE;
/*!40000 ALTER TABLE `chat_messages` DISABLE KEYS */;
INSERT INTO `chat_messages` VALUES (11,'Hello','2021-09-23 15:07:35.711816','KJSDVWEZ',3),(12,'hello','2021-09-23 15:41:04.659873','KJSDVWEZ',3),(13,'hello','2021-09-23 15:46:08.884475','KJSDVWEZ',15);
/*!40000 ALTER TABLE `chat_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2021-09-11 18:37:46.873195','1','anjmhrjn',3,'',4,2),(2,'2021-09-11 18:37:52.381130','2','5d498be25f60ba75829aa5009847000165eabb7f',1,'[{\"added\": {}}]',33,2),(3,'2021-09-11 18:38:02.031292','1','Profile object (1)',1,'[{\"added\": {}}]',7,2),(4,'2021-09-13 15:59:04.806059','7','vendor',2,'[{\"changed\": {\"fields\": [\"Active\"]}}]',4,2),(5,'2021-09-13 15:59:39.535978','5','useruser',2,'[{\"changed\": {\"fields\": [\"Active\"]}}]',4,2),(6,'2021-09-13 15:59:50.271778','6','test',2,'[{\"changed\": {\"fields\": [\"Active\"]}}]',4,2),(7,'2021-09-13 16:00:04.294057','3','farmers',2,'[{\"changed\": {\"fields\": [\"Username\", \"First name\", \"Last name\"]}}]',4,2),(8,'2021-09-13 16:00:26.145062','6','buyers',2,'[{\"changed\": {\"fields\": [\"Username\", \"First name\", \"Last name\"]}}]',4,2),(9,'2021-09-13 16:00:35.303517','4','testuser',3,'',4,2),(10,'2021-09-13 16:00:35.309664','5','useruser',3,'',4,2),(11,'2021-09-13 16:00:44.836910','7','vendors',2,'[{\"changed\": {\"fields\": [\"Username\"]}}]',4,2),(12,'2021-09-13 16:01:01.135970','5','Profile object (5)',2,'[{\"changed\": {\"fields\": [\"User type\"]}}]',7,2),(13,'2021-09-17 06:59:15.419843','8','alpha101',2,'[{\"changed\": {\"fields\": [\"Active\"]}}]',4,2),(14,'2021-09-22 09:39:39.617440','1','ProductStock object (1)',2,'[{\"changed\": {\"fields\": [\"Stock\"]}}]',14,2),(15,'2021-09-23 05:10:57.461852','2','akash_admin',2,'[{\"changed\": {\"fields\": [\"Username\"]}}]',4,2),(16,'2021-09-23 05:12:13.965044','2','akash_admin',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',4,2),(17,'2021-09-23 05:12:52.208329','2','ProductSold object (2)',3,'',15,2),(18,'2021-09-23 05:12:52.261642','1','ProductSold object (1)',3,'',15,2),(19,'2021-09-23 05:13:15.191453','1','Production object (1)',3,'',17,2),(20,'2021-09-23 05:13:24.767922','1','ProductStock object (1)',3,'',14,2),(21,'2021-09-23 05:13:39.018115','1','ProductsForSale object (1)',3,'',16,2),(22,'2021-09-23 05:14:22.438919','9','akash',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',4,2),(23,'2021-09-23 05:14:27.158496','9','anuj',2,'[{\"changed\": {\"fields\": [\"Username\"]}}]',4,2),(24,'2021-09-23 05:14:43.082733','9','anuj',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\"]}}]',4,2),(25,'2021-09-23 05:15:13.933986','8','elisha',2,'[{\"changed\": {\"fields\": [\"Username\", \"First name\", \"Last name\", \"Email address\"]}}]',4,2),(26,'2021-09-23 05:15:26.470733','8','elisha',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',4,2),(27,'2021-09-23 05:15:58.853130','6','ursula',2,'[{\"changed\": {\"fields\": [\"Username\", \"First name\", \"Last name\"]}}]',4,2),(28,'2021-09-23 05:16:09.552755','6','ursula',2,'[{\"changed\": {\"fields\": [\"Email address\"]}}]',4,2),(29,'2021-09-23 05:16:28.998351','3','pawan',2,'[{\"changed\": {\"fields\": [\"Username\", \"First name\", \"Last name\", \"Email address\"]}}]',4,2),(30,'2021-09-23 05:17:56.963802','7','anil',2,'[{\"changed\": {\"fields\": [\"Username\", \"First name\", \"Last name\", \"Email address\"]}}]',4,2),(31,'2021-09-23 05:18:09.646576','2','akash_admin',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',4,2),(32,'2021-09-23 05:19:18.836293','2','sir_alex',2,'[{\"changed\": {\"fields\": [\"Username\", \"First name\", \"Last name\", \"Email address\"]}}]',4,2),(33,'2021-09-23 05:19:54.570821','7','david',2,'[{\"changed\": {\"fields\": [\"Username\", \"First name\", \"Last name\", \"Email address\"]}}]',4,2),(34,'2021-09-23 05:20:12.202412','9','bruno',2,'[{\"changed\": {\"fields\": [\"Username\", \"First name\", \"Last name\"]}}]',4,2),(35,'2021-09-23 05:20:41.531235','8','aaron',2,'[{\"changed\": {\"fields\": [\"Username\", \"First name\", \"Last name\", \"Email address\"]}}]',4,2),(36,'2021-09-23 05:20:53.265615','3','harry',2,'[{\"changed\": {\"fields\": [\"Username\", \"First name\", \"Last name\"]}}]',4,2),(37,'2021-09-23 05:20:59.160338','3','harry',2,'[{\"changed\": {\"fields\": [\"Email address\"]}}]',4,2),(38,'2021-09-23 05:21:22.044646','6','rafael',2,'[{\"changed\": {\"fields\": [\"Username\", \"First name\", \"Last name\", \"Email address\"]}}]',4,2),(39,'2021-09-23 05:27:56.690745','15','cristiano',2,'[{\"changed\": {\"fields\": [\"Email address\", \"Active\"]}}]',4,2),(40,'2021-09-23 05:28:11.398662','14','jadon',2,'[{\"changed\": {\"fields\": [\"Email address\", \"Active\"]}}]',4,2),(41,'2021-09-23 05:28:27.082512','10','luke',2,'[{\"changed\": {\"fields\": [\"Email address\", \"Active\"]}}]',4,2),(42,'2021-09-23 05:28:36.373115','14','jadon',2,'[{\"changed\": {\"fields\": [\"Email address\"]}}]',4,2),(43,'2021-09-23 05:28:53.141307','16','marcus',2,'[{\"changed\": {\"fields\": [\"Email address\"]}}]',4,2),(44,'2021-09-23 05:28:58.148925','16','marcus',2,'[{\"changed\": {\"fields\": [\"Active\"]}}]',4,2),(45,'2021-09-23 05:29:07.797058','12','nemanja',2,'[{\"changed\": {\"fields\": [\"Email address\", \"Active\"]}}]',4,2),(46,'2021-09-23 05:29:20.212155','13','paul',2,'[{\"changed\": {\"fields\": [\"Email address\", \"Active\"]}}]',4,2),(47,'2021-09-23 05:29:34.439654','11','scott',2,'[{\"changed\": {\"fields\": [\"Email address\", \"Active\"]}}]',4,2),(48,'2021-09-23 05:30:18.613358','5','Profile object (5)',2,'[{\"changed\": {\"fields\": [\"User type\"]}}]',7,2),(49,'2021-09-23 05:30:24.404072','6','Profile object (6)',2,'[{\"changed\": {\"fields\": [\"User type\"]}}]',7,2),(50,'2021-09-23 05:30:29.317121','7','Profile object (7)',2,'[]',7,2),(51,'2021-09-23 05:30:34.288711','8','Profile object (8)',2,'[]',7,2),(52,'2021-09-23 05:30:40.443086','9','Profile object (9)',2,'[{\"changed\": {\"fields\": [\"User type\"]}}]',7,2),(53,'2021-09-23 05:30:45.966053','10','Profile object (10)',2,'[{\"changed\": {\"fields\": [\"User type\"]}}]',7,2),(54,'2021-09-23 05:30:52.723112','11','Profile object (11)',2,'[{\"changed\": {\"fields\": [\"User type\"]}}]',7,2),(55,'2021-09-23 05:31:01.396164','12','Profile object (12)',2,'[{\"changed\": {\"fields\": [\"User type\"]}}]',7,2),(56,'2021-09-23 05:31:05.963992','13','Profile object (13)',2,'[{\"changed\": {\"fields\": [\"User type\"]}}]',7,2),(57,'2021-09-23 05:31:11.419978','15','Profile object (15)',2,'[{\"changed\": {\"fields\": [\"User type\"]}}]',7,2),(58,'2021-09-23 05:31:15.287296','14','Profile object (14)',2,'[{\"changed\": {\"fields\": [\"User type\"]}}]',7,2),(59,'2021-09-23 12:16:39.035737','6','ProductStock object (6)',2,'[{\"changed\": {\"fields\": [\"Stock\"]}}]',14,2),(60,'2021-09-23 13:11:16.873086','1','BuyDetails object (1)',3,'',24,2),(61,'2021-09-23 13:11:35.097576','1','EquipmentToDisplay object (1)',3,'',25,2),(62,'2021-09-23 13:11:52.301807','10','Messages object (10)',3,'',31,2),(63,'2021-09-23 13:11:52.307304','9','Messages object (9)',3,'',31,2),(64,'2021-09-23 13:11:52.310727','8','Messages object (8)',3,'',31,2),(65,'2021-09-23 13:11:52.314404','7','Messages object (7)',3,'',31,2),(66,'2021-09-23 13:11:52.318423','6','Messages object (6)',3,'',31,2),(67,'2021-09-23 13:11:52.321479','5','Messages object (5)',3,'',31,2),(68,'2021-09-23 13:11:52.324474','4','Messages object (4)',3,'',31,2),(69,'2021-09-23 13:11:52.326940','3','Messages object (3)',3,'',31,2),(70,'2021-09-23 13:11:52.329936','2','Messages object (2)',3,'',31,2),(71,'2021-09-23 13:11:52.332634','1','Messages object (1)',3,'',31,2),(72,'2021-09-23 15:51:16.693293','1','Ticket object (1)',3,'',28,2);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(28,'admins','ticket'),(29,'admins','ticketresponse'),(9,'api','feedback'),(7,'api','profile'),(8,'api','reportuser'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(32,'authtoken','token'),(33,'authtoken','tokenproxy'),(30,'chat','chatroom'),(31,'chat','messages'),(5,'contenttypes','contenttype'),(19,'farmers','expenses'),(18,'farmers','homeexpenses'),(21,'farmers','imagetest'),(11,'farmers','note'),(20,'farmers','npktest'),(12,'farmers','productcomment'),(17,'farmers','production'),(13,'farmers','productreport'),(10,'farmers','products'),(16,'farmers','productsforsale'),(15,'farmers','productsold'),(14,'farmers','productstock'),(6,'sessions','session'),(24,'vendors','buydetails'),(22,'vendors','equipment'),(27,'vendors','equipmentcomment'),(23,'vendors','equipmentreport'),(25,'vendors','equipmenttodisplay'),(26,'vendors','rentdetails');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-09-11 18:34:09.711749'),(2,'auth','0001_initial','2021-09-11 18:34:09.950596'),(3,'admin','0001_initial','2021-09-11 18:34:10.596502'),(4,'admin','0002_logentry_remove_auto_add','2021-09-11 18:34:10.797005'),(5,'admin','0003_logentry_add_action_flag_choices','2021-09-11 18:34:10.808378'),(6,'admins','0001_initial','2021-09-11 18:34:10.852630'),(7,'admins','0002_auto_20210704_2115','2021-09-11 18:34:11.173222'),(8,'admins','0003_auto_20210704_2318','2021-09-11 18:34:11.661764'),(9,'admins','0004_auto_20210705_1033','2021-09-11 18:34:13.946863'),(10,'admins','0005_ticket_ticketresponse','2021-09-11 18:34:14.017527'),(11,'api','0001_initial','2021-09-11 18:34:14.253813'),(12,'api','0002_auto_20210621_1324','2021-09-11 18:34:14.301947'),(13,'api','0003_profile','2021-09-11 18:34:14.340577'),(14,'api','0004_equipment','2021-09-11 18:34:14.467869'),(15,'api','0005_auto_20210626_2100','2021-09-11 18:34:14.796185'),(16,'api','0006_auto_20210626_2207','2021-09-11 18:34:14.879508'),(17,'api','0004_auto_20210626_1704','2021-09-11 18:34:15.223213'),(18,'api','0007_merge_20210701_2118','2021-09-11 18:34:15.226890'),(19,'api','0008_delete_equipment','2021-09-11 18:34:15.249365'),(20,'api','0009_auto_20210806_1632','2021-09-11 18:34:15.366856'),(21,'api','0010_auto_20210806_1633','2021-09-11 18:34:15.441236'),(22,'api','0011_profile_bio','2021-09-11 18:34:15.484074'),(23,'api','0012_auto_20210814_1647','2021-09-11 18:34:15.510276'),(24,'api','0013_auto_20210822_2204','2021-09-11 18:34:15.522244'),(25,'api','0014_reportuser','2021-09-11 18:34:15.570058'),(26,'api','0015_auto_20210824_1933','2021-09-11 18:34:15.969328'),(27,'api','0016_feedback','2021-09-11 18:34:16.001185'),(28,'api','0017_feedback_description','2021-09-11 18:34:16.083269'),(29,'contenttypes','0002_remove_content_type_name','2021-09-11 18:34:16.234342'),(30,'auth','0002_alter_permission_name_max_length','2021-09-11 18:34:16.319116'),(31,'auth','0003_alter_user_email_max_length','2021-09-11 18:34:16.364568'),(32,'auth','0004_alter_user_username_opts','2021-09-11 18:34:16.377931'),(33,'auth','0005_alter_user_last_login_null','2021-09-11 18:34:16.468933'),(34,'auth','0006_require_contenttypes_0002','2021-09-11 18:34:16.473645'),(35,'auth','0007_alter_validators_add_error_messages','2021-09-11 18:34:16.487638'),(36,'auth','0008_alter_user_username_max_length','2021-09-11 18:34:16.631570'),(37,'auth','0009_alter_user_last_name_max_length','2021-09-11 18:34:16.778369'),(38,'auth','0010_alter_group_name_max_length','2021-09-11 18:34:16.890068'),(39,'auth','0011_update_proxy_permissions','2021-09-11 18:34:16.903348'),(40,'auth','0012_alter_user_first_name_max_length','2021-09-11 18:34:17.001739'),(41,'authtoken','0001_initial','2021-09-11 18:34:17.066967'),(42,'authtoken','0002_auto_20160226_1747','2021-09-11 18:34:17.489719'),(43,'authtoken','0003_tokenproxy','2021-09-11 18:34:17.496063'),(44,'chat','0001_initial','2021-09-11 18:34:17.572533'),(45,'farmers','0001_initial','2021-09-11 18:34:17.922200'),(46,'farmers','0002_auto_20210627_2049','2021-09-11 18:34:18.355634'),(47,'farmers','0003_auto_20210627_2056','2021-09-11 18:34:18.992201'),(48,'farmers','0004_products_prod_img','2021-09-11 18:34:19.037198'),(49,'farmers','0005_auto_20210704_2115','2021-09-11 18:34:19.525595'),(50,'farmers','0006_auto_20210705_1033','2021-09-11 18:34:20.249264'),(51,'farmers','0007_auto_20210705_1746','2021-09-11 18:34:21.433797'),(52,'farmers','0008_auto_20210705_1825','2021-09-11 18:34:21.996698'),(53,'farmers','0009_auto_20210705_2024','2021-09-11 18:34:22.045825'),(54,'farmers','0010_productsold_remarls','2021-09-11 18:34:22.092776'),(55,'farmers','0011_auto_20210707_1433','2021-09-11 18:34:22.127009'),(56,'farmers','0012_auto_20210707_2039','2021-09-11 18:34:22.220031'),(57,'farmers','0013_homeexpenses','2021-09-11 18:34:22.325267'),(58,'farmers','0014_homeexpenses_expense_of','2021-09-11 18:34:22.424041'),(59,'farmers','0015_auto_20210708_1542','2021-09-11 18:34:22.535353'),(60,'farmers','0016_auto_20210708_1548','2021-09-11 18:34:22.569861'),(61,'farmers','0017_auto_20210708_2208','2021-09-11 18:34:22.910048'),(62,'farmers','0018_delete_expenses','2021-09-11 18:34:22.933957'),(63,'farmers','0019_expenses','2021-09-11 18:34:22.995701'),(64,'farmers','0020_auto_20210712_1924','2021-09-11 18:34:23.266815'),(65,'farmers','0021_productsold_seen','2021-09-11 18:34:23.326325'),(66,'farmers','0022_remove_productsold_sold_by','2021-09-11 18:34:23.545698'),(67,'farmers','0023_auto_20210807_1441','2021-09-11 18:34:23.601481'),(68,'farmers','0024_productsforsale_to_display','2021-09-11 18:34:23.737011'),(69,'farmers','0025_auto_20210808_2234','2021-09-11 18:34:23.774317'),(70,'farmers','0026_auto_20210813_2240','2021-09-11 18:34:23.997945'),(71,'farmers','0027_auto_20210911_2320','2021-09-11 18:34:24.239859'),(72,'sessions','0001_initial','2021-09-11 18:34:24.282346'),(73,'vendors','0001_initial','2021-09-11 18:34:24.354103'),(74,'vendors','0002_auto_20210701_2125','2021-09-11 18:34:24.517560'),(75,'vendors','0003_auto_20210701_2128','2021-09-11 18:34:24.582157'),(76,'vendors','0004_auto_20210703_1412','2021-09-11 18:34:24.772671'),(77,'vendors','0005_auto_20210703_1925','2021-09-11 18:34:25.153613'),(78,'vendors','0006_auto_20210707_2039','2021-09-11 18:34:26.988370'),(79,'vendors','0007_auto_20210707_2056','2021-09-11 18:34:27.538375'),(80,'vendors','0008_auto_20210707_2214','2021-09-11 18:34:27.694944'),(81,'vendors','0009_auto_20210728_2030','2021-09-11 18:34:27.855132'),(82,'vendors','0010_auto_20210728_2047','2021-09-11 18:34:28.135277'),(83,'vendors','0011_auto_20210731_1555','2021-09-11 18:34:28.180087'),(84,'vendors','0012_auto_20210807_1259','2021-09-11 18:34:28.253710'),(85,'vendors','0013_auto_20210807_1305','2021-09-11 18:34:28.570133'),(86,'vendors','0014_auto_20210807_1441','2021-09-11 18:34:28.599455'),(87,'vendors','0015_equipmenttodisplay_to_display','2021-09-11 18:34:28.689897'),(88,'vendors','0016_auto_20210809_2204','2021-09-11 18:34:28.839099'),(89,'vendors','0017_auto_20210813_2240','2021-09-11 18:34:28.974272');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `farmers_expenses`
--

DROP TABLE IF EXISTS `farmers_expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `farmers_expenses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `particular` varchar(75) NOT NULL,
  `expense_type` varchar(50) NOT NULL,
  `unit` varchar(20) NOT NULL,
  `quantity` double NOT NULL,
  `amount` double NOT NULL,
  `expense_date` datetime(6) NOT NULL,
  `remarks` varchar(150) DEFAULT NULL,
  `expense_of_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `farmers_expenses_expense_of_id_fde5d3f4_fk_auth_user_id` (`expense_of_id`),
  CONSTRAINT `farmers_expenses_expense_of_id_fde5d3f4_fk_auth_user_id` FOREIGN KEY (`expense_of_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `farmers_expenses`
--

LOCK TABLES `farmers_expenses` WRITE;
/*!40000 ALTER TABLE `farmers_expenses` DISABLE KEYS */;
INSERT INTO `farmers_expenses` VALUES (1,'Manure purchase','Before Harvesting','kg',50,15000,'2021-09-23 06:03:21.585227','Amount spent on manure purchase.',3),(2,'Crop','During Harvesting','gallons',33,25000,'2021-09-23 06:04:43.829596','Water supply for crop maintenance.',3);
/*!40000 ALTER TABLE `farmers_expenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `farmers_homeexpenses`
--

DROP TABLE IF EXISTS `farmers_homeexpenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `farmers_homeexpenses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(50) NOT NULL,
  `quantity` double NOT NULL,
  `estimated_price` double NOT NULL,
  `date` datetime(6) NOT NULL,
  `expense_of_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `farmers_homeexpenses_expense_of_id_6b564ed0_fk_auth_user_id` (`expense_of_id`),
  KEY `farmers_homeexpenses_product_id_29109241_fk_farmers_products_id` (`product_id`),
  CONSTRAINT `farmers_homeexpenses_expense_of_id_6b564ed0_fk_auth_user_id` FOREIGN KEY (`expense_of_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `farmers_homeexpenses_product_id_29109241_fk_farmers_products_id` FOREIGN KEY (`product_id`) REFERENCES `farmers_products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `farmers_homeexpenses`
--

LOCK TABLES `farmers_homeexpenses` WRITE;
/*!40000 ALTER TABLE `farmers_homeexpenses` DISABLE KEYS */;
INSERT INTO `farmers_homeexpenses` VALUES (1,'Consumed',12,2500,'2021-09-23 06:00:07.575485',3,1,'Potato consumed at home.'),(2,'Wastes',25,1500,'2021-09-23 06:01:52.703965',3,3,'Eaten by insects.');
/*!40000 ALTER TABLE `farmers_homeexpenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `farmers_imagetest`
--

DROP TABLE IF EXISTS `farmers_imagetest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `farmers_imagetest` (
  `id` int NOT NULL AUTO_INCREMENT,
  `image` varchar(150) NOT NULL,
  `recomended_crops` varchar(255) NOT NULL,
  `test_of_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `farmers_imagetest_test_of_id_94285c12_fk_auth_user_id` (`test_of_id`),
  CONSTRAINT `farmers_imagetest_test_of_id_94285c12_fk_auth_user_id` FOREIGN KEY (`test_of_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `farmers_imagetest`
--

LOCK TABLES `farmers_imagetest` WRITE;
/*!40000 ALTER TABLE `farmers_imagetest` DISABLE KEYS */;
INSERT INTO `farmers_imagetest` VALUES (1,'static/image_test/black_TUpBGWe.jpg','Black Soil: Wheat, Jowar, Millet, Linseed, Castor, Sunflower',3);
/*!40000 ALTER TABLE `farmers_imagetest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `farmers_note`
--

DROP TABLE IF EXISTS `farmers_note`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `farmers_note` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `content` varchar(500) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `posted_by_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `farmers_note_posted_by_id_d37f123e_fk_auth_user_id` (`posted_by_id`),
  CONSTRAINT `farmers_note_posted_by_id_d37f123e_fk_auth_user_id` FOREIGN KEY (`posted_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `farmers_note`
--

LOCK TABLES `farmers_note` WRITE;
/*!40000 ALTER TABLE `farmers_note` DISABLE KEYS */;
/*!40000 ALTER TABLE `farmers_note` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `farmers_npktest`
--

DROP TABLE IF EXISTS `farmers_npktest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `farmers_npktest` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nitrogen` double NOT NULL,
  `phosphorus` double NOT NULL,
  `potassium` double NOT NULL,
  `temperature` double NOT NULL,
  `humidity` double NOT NULL,
  `ph` double NOT NULL,
  `recommended_crop` varchar(50) NOT NULL,
  `test_of_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `farmers_npktest_test_of_id_f232b559_fk_auth_user_id` (`test_of_id`),
  CONSTRAINT `farmers_npktest_test_of_id_f232b559_fk_auth_user_id` FOREIGN KEY (`test_of_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `farmers_npktest`
--

LOCK TABLES `farmers_npktest` WRITE;
/*!40000 ALTER TABLE `farmers_npktest` DISABLE KEYS */;
INSERT INTO `farmers_npktest` VALUES (1,75,70,50,32,55,7,'banana',3),(2,12,50,31,25,22,7,'Kidneybeans',3),(3,75,50,50,12,12,7,'Chickpea',3);
/*!40000 ALTER TABLE `farmers_npktest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `farmers_productcomment`
--

DROP TABLE IF EXISTS `farmers_productcomment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `farmers_productcomment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `comment` varchar(200) NOT NULL,
  `comment_date` datetime(6) NOT NULL,
  `comment_by_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `farmers_productcomme_product_id_9d8a1223_fk_farmers_p` (`product_id`),
  KEY `farmers_productcomment_comment_by_id_b16c2bec_fk_auth_user_id` (`comment_by_id`),
  CONSTRAINT `farmers_productcomme_product_id_9d8a1223_fk_farmers_p` FOREIGN KEY (`product_id`) REFERENCES `farmers_productsforsale` (`id`),
  CONSTRAINT `farmers_productcomment_comment_by_id_b16c2bec_fk_auth_user_id` FOREIGN KEY (`comment_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `farmers_productcomment`
--

LOCK TABLES `farmers_productcomment` WRITE;
/*!40000 ALTER TABLE `farmers_productcomment` DISABLE KEYS */;
INSERT INTO `farmers_productcomment` VALUES (2,'This is test comment.','2021-09-23 15:37:07.466976',3,10);
/*!40000 ALTER TABLE `farmers_productcomment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `farmers_production`
--

DROP TABLE IF EXISTS `farmers_production`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `farmers_production` (
  `id` int NOT NULL AUTO_INCREMENT,
  `production_qty` double NOT NULL,
  `area` double NOT NULL,
  `production_date` datetime(6) NOT NULL,
  `farmer_id_id` int DEFAULT NULL,
  `product_id_id` int DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `farmers_production_farmer_id_id_fb38931a_fk_auth_user_id` (`farmer_id_id`),
  KEY `farmers_production_product_id_id_f676be4c_fk_farmers_products_id` (`product_id_id`),
  CONSTRAINT `farmers_production_farmer_id_id_fb38931a_fk_auth_user_id` FOREIGN KEY (`farmer_id_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `farmers_production_product_id_id_f676be4c_fk_farmers_products_id` FOREIGN KEY (`product_id_id`) REFERENCES `farmers_products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `farmers_production`
--

LOCK TABLES `farmers_production` WRITE;
/*!40000 ALTER TABLE `farmers_production` DISABLE KEYS */;
INSERT INTO `farmers_production` VALUES (2,10200,20500,'2021-09-23 05:52:45.040939',3,2,NULL),(3,15000,23000,'2021-09-23 05:53:09.387212',3,5,NULL),(4,5000,12000,'2021-09-23 05:53:44.682884',3,3,NULL),(5,3000,7000,'2021-09-23 05:58:28.512435',3,1,NULL),(6,3000,8200,'2021-09-23 05:58:44.888499',3,9,NULL),(7,5000,8500,'2021-09-23 06:14:18.950056',6,2,NULL),(8,5000,9000,'2021-09-23 06:14:41.864049',6,5,NULL),(9,2000,6200,'2021-09-23 06:14:59.184262',6,3,NULL),(10,2000,7150,'2021-09-23 06:18:55.897281',6,7,NULL),(11,3000,7150,'2021-09-23 06:19:11.472229',6,8,NULL),(12,5125,8700,'2021-09-23 06:20:26.202100',7,11,NULL),(13,3325,7255,'2021-09-23 06:20:57.728937',7,14,NULL),(14,7300,11250,'2021-09-23 06:21:21.302479',7,13,NULL),(15,7875,14350,'2021-09-23 06:22:01.276273',7,1,NULL),(16,3370,11300,'2021-09-23 06:22:55.175111',7,10,NULL),(17,3300,5235,'2021-09-23 10:05:40.550712',8,19,NULL),(18,8320,12570,'2021-09-23 10:06:08.357018',8,15,NULL),(19,7325,14250,'2021-09-23 10:06:28.846372',8,16,NULL),(20,8235,13350,'2021-09-23 10:06:59.093278',8,7,NULL),(21,3350,10525,'2021-09-23 10:07:29.758227',8,21,NULL),(22,7390,12570,'2021-09-23 10:08:00.627312',8,25,NULL),(23,13275,24570,'2021-09-23 10:08:52.449472',9,25,NULL),(24,8575,15250,'2021-09-23 10:09:14.999806',9,28,NULL),(25,7900,15730,'2021-09-23 10:09:38.543643',9,12,NULL),(26,4570,11375,'2021-09-23 10:11:01.069480',9,19,NULL),(27,9350,21025,'2021-09-23 10:11:58.505887',9,18,NULL);
/*!40000 ALTER TABLE `farmers_production` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `farmers_productreport`
--

DROP TABLE IF EXISTS `farmers_productreport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `farmers_productreport` (
  `id` int NOT NULL AUTO_INCREMENT,
  `report_category` varchar(50) NOT NULL,
  `report_description` varchar(200) NOT NULL,
  `reported_date` datetime(6) NOT NULL,
  `reported_by_id` int DEFAULT NULL,
  `reported_product_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `farmers_productrepor_reported_product_id_da1fa6d2_fk_farmers_p` (`reported_product_id`),
  KEY `farmers_productreport_reported_by_id_cfadf88f_fk_auth_user_id` (`reported_by_id`),
  CONSTRAINT `farmers_productrepor_reported_product_id_da1fa6d2_fk_farmers_p` FOREIGN KEY (`reported_product_id`) REFERENCES `farmers_productsforsale` (`id`),
  CONSTRAINT `farmers_productreport_reported_by_id_cfadf88f_fk_auth_user_id` FOREIGN KEY (`reported_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `farmers_productreport`
--

LOCK TABLES `farmers_productreport` WRITE;
/*!40000 ALTER TABLE `farmers_productreport` DISABLE KEYS */;
/*!40000 ALTER TABLE `farmers_productreport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `farmers_products`
--

DROP TABLE IF EXISTS `farmers_products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `farmers_products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `prod_name` varchar(100) NOT NULL,
  `prod_category` varchar(25) NOT NULL,
  `prod_img` varchar(1200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `farmers_products`
--

LOCK TABLES `farmers_products` WRITE;
/*!40000 ALTER TABLE `farmers_products` DISABLE KEYS */;
INSERT INTO `farmers_products` VALUES (1,'Potato','Vegetables','static/product_images/potato.jpg'),(2,'Wheat','Cereals','static/product_images/wheat.jpg'),(3,'Corn','Cereals','static/product_images/corn_Jd0hdlR.jpg'),(4,'Buckwheat','Cereals','static/product_images/buckwheat.jpg'),(5,'Rice','Cereals','static/product_images/rice.jpg'),(6,'Black Eyed Peas','Pulses','static/product_images/black eyed peas.jpg'),(7,'Chickpeas','Pulses','static/product_images/chickpeas_mpLKjMr.jpg'),(8,'Kidney Beans','Pulses','static/product_images/kidney beans.jpg'),(9,'Onion','Vegetables','static/product_images/onions_o74UJdd.jpg'),(10,'Cauliflower','Vegetables','static/product_images/cauliflower.jpg'),(11,'Apple','Fruits','static/product_images/apple.jpg'),(12,'Orange','Fruits','static/product_images/orange_8qoXn0q.jpg'),(13,'Mango','Fruits','static/product_images/mango.jpg'),(14,'Banana','Fruits','static/product_images/banana.jpg'),(15,'Almonds','Nuts','static/product_images/almonds.jpg'),(16,'Cashews','Nuts','static/product_images/cashews.jpg'),(17,'Pistachio','Nuts','static/product_images/pistachio.jpg'),(18,'Soybean','Oilseeds','static/product_images/soybean.jpg'),(19,'Peanuts','Oilseeds','static/product_images/peanuts.png'),(20,'Cassava','Sugars and Starches','static/product_images/cassava.jpg'),(21,'Sweet Potato','Sugars and Starches','static/product_images/sweet potato.jpg'),(22,'Cotton','Fibres','static/product_images/cotton.jpg'),(23,'Jute','Fibres','static/product_images/jute.jpg'),(24,'Coconut','Beverages','static/product_images/coconut.jpg'),(25,'Coffee','Beverages','static/product_images/coffee.jpg'),(26,'Betel Nut','Narcotics','static/product_images/betel nut.jpg'),(27,'Turmeric','Spices','static/product_images/turmeric.jpg'),(28,'Cinnamon','Spices','static/product_images/cinnamon.jpg'),(29,'Mustard','Condiments','static/product_images/mustard.jpg'),(30,'Tulsi','Others','static/product_images/tulsi.jpg');
/*!40000 ALTER TABLE `farmers_products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `farmers_productsforsale`
--

DROP TABLE IF EXISTS `farmers_productsforsale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `farmers_productsforsale` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quantity_in_kg` double NOT NULL,
  `price_per_kg` double NOT NULL,
  `added_date` datetime(6) NOT NULL,
  `added_by_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `details` varchar(250) DEFAULT NULL,
  `to_display` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `farmers_productsforsale_added_by_id_f02561d9_fk_auth_user_id` (`added_by_id`),
  KEY `farmers_productsfors_product_id_4f8fa6f6_fk_farmers_p` (`product_id`),
  CONSTRAINT `farmers_productsfors_product_id_4f8fa6f6_fk_farmers_p` FOREIGN KEY (`product_id`) REFERENCES `farmers_products` (`id`),
  CONSTRAINT `farmers_productsforsale_added_by_id_f02561d9_fk_auth_user_id` FOREIGN KEY (`added_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `farmers_productsforsale`
--

LOCK TABLES `farmers_productsforsale` WRITE;
/*!40000 ALTER TABLE `farmers_productsforsale` DISABLE KEYS */;
INSERT INTO `farmers_productsforsale` VALUES (2,1000,430,'2021-09-23 10:18:35.198724',9,25,'Freshly grinded coffee beans.',1),(3,2500,750,'2021-09-23 10:22:50.648855',9,28,'Fresh Cinnamon.',1),(4,3000,120,'2021-09-23 10:23:57.914784',9,12,'Fresh orange',1),(5,1000,350,'2021-09-23 10:24:40.124072',9,19,'Fresh peanuts.',1),(6,1250,550,'2021-09-23 11:36:17.278307',8,19,'Peanuts from Nepalgunj.',1),(7,2400,1000,'2021-09-23 11:36:43.358582',8,15,'Healthy almonds.',1),(8,3500,750,'2021-09-23 11:37:32.815601',8,16,'Good cashews.',1),(9,1500,590,'2021-09-23 11:38:38.471355',8,25,'Good coffee',1),(10,5000,250,'2021-09-23 11:41:10.954976',3,2,'Wheat from Dhangadi.',1),(11,10000,120,'2021-09-23 11:41:36.592972',3,5,'Best rice in town.',1),(12,2000,120,'2021-09-23 11:41:59.048586',3,3,'Tasty corn.',1),(13,1500,95,'2021-09-23 11:42:38.678914',3,9,'Onions fresh from dhangadi.',1),(14,2500,95,'2021-09-23 11:46:02.707884',7,11,'Fresh apples',1),(15,2500,100,'2021-09-23 11:46:33.394721',7,14,'Healthy banana',1),(16,1000,80,'2021-09-23 11:47:08.527800',7,1,'Tasty potato.',1);
/*!40000 ALTER TABLE `farmers_productsforsale` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `farmers_productsold`
--

DROP TABLE IF EXISTS `farmers_productsold`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `farmers_productsold` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quantity_sold` double NOT NULL,
  `sold_price` double NOT NULL,
  `sold_date` datetime(6) NOT NULL,
  `sold_to_id` int DEFAULT NULL,
  `sold_product_id` int DEFAULT NULL,
  `remarks` varchar(1250) DEFAULT NULL,
  `approved` tinyint(1) NOT NULL,
  `seen` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `farmers_productsold_sold_product_id_2577a026_fk_farmers_p` (`sold_product_id`),
  KEY `farmers_productsold_sold_to_id_215cfe10_fk_auth_user_id` (`sold_to_id`),
  CONSTRAINT `farmers_productsold_sold_product_id_2577a026_fk_farmers_p` FOREIGN KEY (`sold_product_id`) REFERENCES `farmers_productsforsale` (`id`),
  CONSTRAINT `farmers_productsold_sold_to_id_215cfe10_fk_auth_user_id` FOREIGN KEY (`sold_to_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `farmers_productsold`
--

LOCK TABLES `farmers_productsold` WRITE;
/*!40000 ALTER TABLE `farmers_productsold` DISABLE KEYS */;
INSERT INTO `farmers_productsold` VALUES (3,500,125000,'2021-09-23 11:55:20.762745',10,10,'I need 20 containers each with 25kg of wheat.',0,1),(4,1000,120000,'2021-09-23 11:56:03.394762',10,11,'I need 40 containers each of 25kg.',1,1),(5,250,30000,'2021-09-23 11:56:48.628198',10,12,'I need 10 containers each of 25kg.',0,0),(6,250,23750,'2021-09-23 11:57:14.974756',10,13,'I need 10 containers each of 25kg.',0,1),(7,100,25000,'2021-09-23 11:58:32.825423',11,10,'I need 4 containers each of 25kg.',1,1),(8,100,12000,'2021-09-23 11:58:58.743472',11,11,'I need 4 containers each of 25kg.',0,0),(9,50,6000,'2021-09-23 11:59:11.446180',11,12,'I need 2 containers each of 25 kg.',1,1),(10,50,4750,'2021-09-23 11:59:23.452814',11,13,'I need 2 containers each of 25 kg.',1,1),(11,100,25000,'2021-09-23 12:00:19.273443',12,10,'I need 4 containers each of 25kg.',0,0),(12,50,6000,'2021-09-23 12:00:31.628639',12,11,'I need 2 containers each of 25 kg.',1,1),(13,100,9500,'2021-09-23 12:00:49.313270',12,13,'I need 4 containers each of 25 kg.',0,1),(14,10,4300,'2021-09-23 12:02:49.725880',13,2,'I need 2 packets each of 5kg.',1,1),(15,20,15000,'2021-09-23 12:03:25.482082',13,3,'I need 4 packets each of 5kg.',1,1),(16,250,20000,'2021-09-23 12:03:41.240183',13,16,'I need 10 containers each of 25kg.',1,1),(17,50,50000,'2021-09-23 12:04:54.160556',14,7,'I need 10 packets each of 5 kg',1,1),(18,50,37500,'2021-09-23 12:05:09.606114',14,8,'I need 10 packets each of 5 kg.',1,1),(19,100,9500,'2021-09-23 12:05:26.421782',14,14,'I need 4 containers each of 25 kg.',1,1);
/*!40000 ALTER TABLE `farmers_productsold` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `farmers_productstock`
--

DROP TABLE IF EXISTS `farmers_productstock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `farmers_productstock` (
  `id` int NOT NULL AUTO_INCREMENT,
  `stock` double NOT NULL,
  `farmer_id_id` int DEFAULT NULL,
  `product_id_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `farmers_productstock_farmer_id_id_f74e582c_fk_auth_user_id` (`farmer_id_id`),
  KEY `farmers_productstock_product_id_id_f4ecabe7_fk_farmers_p` (`product_id_id`),
  CONSTRAINT `farmers_productstock_farmer_id_id_f74e582c_fk_auth_user_id` FOREIGN KEY (`farmer_id_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `farmers_productstock_product_id_id_f4ecabe7_fk_farmers_p` FOREIGN KEY (`product_id_id`) REFERENCES `farmers_products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `farmers_productstock`
--

LOCK TABLES `farmers_productstock` WRITE;
/*!40000 ALTER TABLE `farmers_productstock` DISABLE KEYS */;
INSERT INTO `farmers_productstock` VALUES (2,10100,3,2),(3,13950,3,5),(4,4925,3,3),(5,2988,3,1),(6,2950,3,9),(7,5000,6,2),(8,5000,6,5),(9,2000,6,3),(10,2000,6,7),(11,3000,6,8),(12,5025,7,11),(13,3325,7,14),(14,7300,7,13),(15,7625,7,1),(16,3370,7,10),(17,3300,8,19),(18,8270,8,15),(19,7275,8,16),(20,8235,8,7),(21,3350,8,21),(22,7390,8,25),(23,13265,9,25),(24,8555,9,28),(25,7900,9,12),(26,4570,9,19),(27,9350,9,18);
/*!40000 ALTER TABLE `farmers_productstock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_buydetails`
--

DROP TABLE IF EXISTS `vendors_buydetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_buydetails` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quantity` double NOT NULL,
  `total_price` double NOT NULL,
  `sold_date` datetime(6) NOT NULL,
  `remarks` varchar(150) DEFAULT NULL,
  `approved` tinyint(1) NOT NULL,
  `equipment_id` int DEFAULT NULL,
  `sold_to_id` int DEFAULT NULL,
  `delivered_address` varchar(100) NOT NULL,
  `seen` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendors_buydetails_equipment_id_76e2e411_fk_vendors_e` (`equipment_id`),
  KEY `vendors_buydetails_sold_to_id_3ba164cd_fk_auth_user_id` (`sold_to_id`),
  CONSTRAINT `vendors_buydetails_equipment_id_76e2e411_fk_vendors_e` FOREIGN KEY (`equipment_id`) REFERENCES `vendors_equipmenttodisplay` (`id`),
  CONSTRAINT `vendors_buydetails_sold_to_id_3ba164cd_fk_auth_user_id` FOREIGN KEY (`sold_to_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_buydetails`
--

LOCK TABLES `vendors_buydetails` WRITE;
/*!40000 ALTER TABLE `vendors_buydetails` DISABLE KEYS */;
INSERT INTO `vendors_buydetails` VALUES (2,1,25000,'2021-09-23 13:20:54.346778','',1,7,3,'Nepalgunj',1),(3,1,75000,'2021-09-23 13:21:24.470110','',1,8,3,'Nepalgunj',1),(4,1,89500,'2021-09-23 13:22:43.492091','',1,2,10,'Dhangadi',1),(5,1,75000,'2021-09-23 13:22:58.526227','',0,8,10,'Dhangadi',1),(6,3,75000,'2021-09-23 13:23:08.509023','',0,5,10,'Dhangadi',0),(7,1,33000,'2021-09-23 13:23:21.664638','',1,6,10,'Dhangadi',1),(8,1,95000,'2021-09-23 13:26:40.146918','',1,4,11,'Dang',1),(9,1,83000,'2021-09-23 13:26:54.990798','',1,9,11,'Dang',1),(10,2,50000,'2021-09-23 13:27:03.743224','',0,5,11,'Dang',1),(11,1,89500,'2021-09-23 13:27:11.858043','',1,2,11,'Dang',1),(12,2,50000,'2021-09-23 13:27:26.471703','',0,7,11,'Dang',0),(13,2,66000,'2021-09-23 13:42:20.425228','',0,6,12,'Jhapa',0),(14,2,150000,'2021-09-23 13:42:30.684578','',0,8,12,'Jhapa',1),(15,3,75000,'2021-09-23 13:42:47.954297','',1,5,12,'Jhapa',1),(16,1,95000,'2021-09-23 13:43:18.863093','',0,4,14,'Birgunj',0),(17,5,125000,'2021-09-23 13:43:29.278559','',1,7,14,'Birgunj',1);
/*!40000 ALTER TABLE `vendors_buydetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_equipment`
--

DROP TABLE IF EXISTS `vendors_equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_equipment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(70) NOT NULL,
  `category` varchar(25) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vendors_equipment_name_c703c1b8_uniq` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_equipment`
--

LOCK TABLES `vendors_equipment` WRITE;
/*!40000 ALTER TABLE `vendors_equipment` DISABLE KEYS */;
INSERT INTO `vendors_equipment` VALUES (1,'Utility Tractor','Tractor'),(2,'Compact Tractor','Tractor'),(3,'Sugarcane Harvester','Harvester'),(4,'Sport ATV','ATV or UTV'),(5,'Utility ATV','ATV or UTV'),(6,'Single Furrow Plow','Plows'),(7,'Double Furrow Plow','Plows'),(8,'Disc Harrows','Harrows'),(9,'Tine Harrows','Harrows'),(10,'Rotary Fertilizer Spreader','Fertilizer Spreaders'),(11,'Drop Fertilizer Spreader','Fertilizer Spreaders'),(12,'Liquid Fertilizer Spreader','Fertilizer Spreaders'),(13,'Belt Seeder','Seeders'),(14,'Vacuum Seeder','Seeders'),(15,'Pneumatic Seeder','Seeders'),(16,'Vertical Balers','Balers'),(17,'Horizontal Balers','Balers'),(18,'Two-Ram Balers','Balers'),(19,'Nitrogen Testing Kit','Other'),(20,'Potassium Testing Kit','Other'),(21,'Phosphorus Testing Kit','Other'),(22,'pH Value Testing Kit','Other');
/*!40000 ALTER TABLE `vendors_equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_equipmentcomment`
--

DROP TABLE IF EXISTS `vendors_equipmentcomment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_equipmentcomment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `comment` varchar(200) NOT NULL,
  `comment_date` datetime(6) NOT NULL,
  `comment_by_id` int DEFAULT NULL,
  `equipment_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `vendors_equipmentcomment_comment_by_id_858d9efa_fk_auth_user_id` (`comment_by_id`),
  KEY `vendors_equipmentcom_equipment_id_79fb1b92_fk_vendors_e` (`equipment_id`),
  CONSTRAINT `vendors_equipmentcom_equipment_id_79fb1b92_fk_vendors_e` FOREIGN KEY (`equipment_id`) REFERENCES `vendors_equipmenttodisplay` (`id`),
  CONSTRAINT `vendors_equipmentcomment_comment_by_id_858d9efa_fk_auth_user_id` FOREIGN KEY (`comment_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_equipmentcomment`
--

LOCK TABLES `vendors_equipmentcomment` WRITE;
/*!40000 ALTER TABLE `vendors_equipmentcomment` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendors_equipmentcomment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_equipmentreport`
--

DROP TABLE IF EXISTS `vendors_equipmentreport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_equipmentreport` (
  `id` int NOT NULL AUTO_INCREMENT,
  `report_category` varchar(50) NOT NULL,
  `report_description` varchar(200) NOT NULL,
  `reported_date` datetime(6) NOT NULL,
  `reported_by_id` int DEFAULT NULL,
  `reported_equipment_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `vendors_equipmentreport_reported_by_id_18b07b87_fk_auth_user_id` (`reported_by_id`),
  KEY `vendors_equipmentrep_reported_equipment_i_38714829_fk_vendors_e` (`reported_equipment_id`),
  CONSTRAINT `vendors_equipmentrep_reported_equipment_i_38714829_fk_vendors_e` FOREIGN KEY (`reported_equipment_id`) REFERENCES `vendors_equipmenttodisplay` (`id`),
  CONSTRAINT `vendors_equipmentreport_reported_by_id_18b07b87_fk_auth_user_id` FOREIGN KEY (`reported_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_equipmentreport`
--

LOCK TABLES `vendors_equipmentreport` WRITE;
/*!40000 ALTER TABLE `vendors_equipmentreport` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendors_equipmentreport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_equipmenttodisplay`
--

DROP TABLE IF EXISTS `vendors_equipmenttodisplay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_equipmenttodisplay` (
  `id` int NOT NULL AUTO_INCREMENT,
  `modal` varchar(75) NOT NULL,
  `available_for_rent` tinyint(1) DEFAULT NULL,
  `available_to_buy` tinyint(1) DEFAULT NULL,
  `price_to_buy_per_item` double DEFAULT NULL,
  `price_per_hour` double DEFAULT NULL,
  `duration` double DEFAULT NULL,
  `details` varchar(200) DEFAULT NULL,
  `date` datetime(6) NOT NULL,
  `eqp_img` varchar(1200) DEFAULT NULL,
  `added_by_id` int DEFAULT NULL,
  `equipment_id` int DEFAULT NULL,
  `to_display` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendors_equipmenttod_equipment_id_799bebcf_fk_vendors_e` (`equipment_id`),
  KEY `vendors_equipmenttodisplay_added_by_id_0a6db078_fk_auth_user_id` (`added_by_id`),
  CONSTRAINT `vendors_equipmenttod_equipment_id_799bebcf_fk_vendors_e` FOREIGN KEY (`equipment_id`) REFERENCES `vendors_equipment` (`id`),
  CONSTRAINT `vendors_equipmenttodisplay_added_by_id_0a6db078_fk_auth_user_id` FOREIGN KEY (`added_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_equipmenttodisplay`
--

LOCK TABLES `vendors_equipmenttodisplay` WRITE;
/*!40000 ALTER TABLE `vendors_equipmenttodisplay` DISABLE KEYS */;
INSERT INTO `vendors_equipmenttodisplay` VALUES (2,'UT101',1,1,89500,125,168,'Best utility tractor in town','2021-09-23 12:49:41.610244','static/eqp_images/utility tractor.jpg',15,1,1),(3,'SH-101',1,0,NULL,100,168,'You can only rent this. Best in town.','2021-09-23 12:50:45.346719','static/eqp_images/sugarcane harvester.png',15,3,1),(4,'UA-101',0,1,95000,NULL,NULL,'Utility ATV with no attachments','2021-09-23 12:54:52.038020','static/eqp_images/utility atv.jpg',15,5,1),(5,'SFP-101',0,1,25000,NULL,NULL,'Single Furrow Plow in green color.','2021-09-23 12:57:42.217369','static/eqp_images/sf plow.jpg',15,6,1),(6,'DH-101',0,1,33000,NULL,NULL,'Blue colored disc harrows.','2021-09-23 12:59:30.318495','static/eqp_images/disc harrow.jpg',16,8,1),(7,'DFS-101',0,1,25000,NULL,NULL,'Green colored drop fertilizer spreader for your lawn.','2021-09-23 13:01:24.563342','static/eqp_images/drop spreader.jpg',16,11,1),(8,'BS-101',0,1,75000,NULL,NULL,'Orange colored belt seeder','2021-09-23 13:04:18.329163','static/eqp_images/belt seeder.jpg',16,13,1),(9,'VB-101',0,1,83000,NULL,NULL,'Blue colored vertical baler.','2021-09-23 13:09:34.569505','static/eqp_images/vertical balers.jpg',16,16,1);
/*!40000 ALTER TABLE `vendors_equipmenttodisplay` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors_rentdetails`
--

DROP TABLE IF EXISTS `vendors_rentdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendors_rentdetails` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rented_quantity` double NOT NULL,
  `rented_duration` double NOT NULL,
  `total_price` double NOT NULL,
  `rented_date` datetime(6) NOT NULL,
  `remarks` varchar(150) DEFAULT NULL,
  `approved` tinyint(1) NOT NULL,
  `equipment_id` int DEFAULT NULL,
  `rented_to_id` int DEFAULT NULL,
  `delivered_address` varchar(100) NOT NULL,
  `seen` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendors_rentdetails_equipment_id_7baf69fd_fk_vendors_e` (`equipment_id`),
  KEY `vendors_rentdetails_rented_to_id_7dd314f4_fk_auth_user_id` (`rented_to_id`),
  CONSTRAINT `vendors_rentdetails_equipment_id_7baf69fd_fk_vendors_e` FOREIGN KEY (`equipment_id`) REFERENCES `vendors_equipmenttodisplay` (`id`),
  CONSTRAINT `vendors_rentdetails_rented_to_id_7dd314f4_fk_auth_user_id` FOREIGN KEY (`rented_to_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors_rentdetails`
--

LOCK TABLES `vendors_rentdetails` WRITE;
/*!40000 ALTER TABLE `vendors_rentdetails` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendors_rentdetails` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-09-26  9:58:15

-- MySQL dump 10.13  Distrib 8.0.26, for Linux (x86_64)
--
-- Host: localhost    Database: flobot
-- ------------------------------------------------------
-- Server version	8.0.26-0ubuntu0.20.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `default_buckets`
--

DROP TABLE IF EXISTS `default_buckets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `default_buckets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `url` varchar(64) DEFAULT NULL,
  `photo_id` varchar(128) DEFAULT NULL,
  `caption` varchar(128) DEFAULT NULL,
  `categ` varchar(128) DEFAULT NULL,
  `cost` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `default_buckets`
--

LOCK TABLES `default_buckets` WRITE;
/*!40000 ALTER TABLE `default_buckets` DISABLE KEYS */;
INSERT INTO `default_buckets` VALUES (1,NULL,'AgACAgIAAxkBAAEBxhphKW32ZRxmBAKD-aiwaN6H_egv2AACN7QxG_RnUUnDOAMyHemzVAEAAwIAA3gAAyAE','Букет из 5 белых роз 60 см','Розы',550),(2,NULL,'AgACAgIAAxkBAAEBxiVhKW5DqpGHaOIqp00QjzuNh0GvuQACOLQxG_RnUUnsdBFSgFMFIQEAAwIAA3gAAyAE','5 Хризантем с эвкалиптом','Хризантемы',850),(3,NULL,'AgACAgIAAxkBAAEBxjBhKW63Tp6RaKX0wPs3rnWOgblZBwACObQxG_RnUUm2Nf_NKUOeUQEAAwIAA3gAAyAE','Кустовые розы 5 штук','Розы',1100),(4,NULL,'AgACAgIAAxkBAAEBxjthKW-qqeIvnoPUlhEPEij-8-xcwQACOrQxG_RnUUn64_pRhsN0vwEAAwIAA3gAAyAE','Букет «Солнечный круг» из 25 желтых роз \n40-50 см','Розы',1500),(5,NULL,'AgACAgIAAxkBAAEBxkZhKW_skioG39bfkDr9ixP_j7H1lQACO7QxG_RnUUm1iGvSLgIIRAEAAwIAA3gAAyAE','Букет из роз Мистик бабблс','Розы',1400),(6,NULL,'AgACAgIAAxkBAAEBxlFhKXApWXRYVhcdZOD6v647Wqh2DgACPLQxG_RnUUmmgZS9XVRxMwEAAwIAA3gAAyAE','Букет радужных гипсофил в коробке','Гипсофилы',1400),(7,NULL,'AgACAgIAAxkBAAEBxlxhKXBT0hGlIBIEGamasP0XwBdD8AACPbQxG_RnUUleV-AJi4aF3wEAAwIAA3gAAyAE','Букет из альстромерий','Альстромерии',1200),(8,NULL,'AgACAgIAAxkBAAEBxnNhKXDR8opQNlhMWdKhyGAAASH7gXEAAj-0MRv0Z1FJyZits_HuNF0BAAMCAAN4AAMgBA','Потрясающий мини-букет из одной гортензии','Гортензии',700),(9,NULL,'AgACAgIAAxkBAAEBxn5hKXPtVO63TLZgz0lfZiMgOqIFwQACQbQxG_RnUUl-D2nUa3JZoAEAAwIAA3gAAyAE','Букет из 7 веток радужных гипсофил','Гипсофилы',1300),(10,NULL,'AgACAgIAAxkBAAEBxolhKXQ8qcUIS7rZ_dQMjLA2lQiURwACQrQxG_RnUUkEEOu11iQEPwEAAwIAA3gAAyAE','Букет «Мини Ми» из 7 гербер','Герберы',1100),(11,NULL,'AgACAgIAAxkBAAEBxpRhKXR3tkenr9VzsTncKLYmAfpRZQACRLQxG_RnUUls17iDIRechAEAAwIAA3gAAyAE','Букет «Три сезона» из 3-х гортензий','Гортензии',1250),(12,NULL,'AgACAgIAAxkBAAEBxvlhKfQY_Dsk3_0m915YRb3s1V2mIwACnLQxG_RnUUl--xCuPLvV-QEAAwIAA3gAAyAE','Букет «Конвертик»\nИз 3-х пионов,одной розы и эустомы','Пионы',1499),(13,NULL,'AgACAgIAAxkBAAEBxwRhKfUODlM396xM2LXQqDHHWmakAgACoLQxG_RnUUnABMEaQB9tXAEAAwIAA3gAAyAE','Букет из одного пиона «Сара Бернар»,3-х штук диантуса,одного лизиантуса','Пионы',1999),(14,NULL,'AgACAgIAAxkBAAEBxw9hKfW22wprmdgkjEyIRlWFuJQcrQACpLQxG_RnUUlNyrSXU1f0FwEAAwIAA3gAAyAE','Букет из 5 белых пион \n«Снег»','Пионы',1999),(15,NULL,'AgACAgIAAxkBAAEBxxphKfY5GoGvuqSpPub3ugtspTWwEwACpbQxG_RnUUnSVAABgySjlyIBAAMCAAN4AAMgBA','Букет«Саншайн»из 5 пион и 3-х питтоспорумов','Пионы',2300),(16,NULL,'AgACAgIAAxkBAAEBxyVhKf81QQj_MZjSq_KFKjLENSFF6gACybQxG_RnUUmO3lsycah8WQEAAwIAA3gAAyAE','Букет «Дон Пион» из 3-х пион и эвкалипта','Пионы',1600),(17,NULL,'AgACAgIAAxkBAAEBxzBhKf_H4BC197l36Ry7WUCSp00LYwAC0rQxG_RnUUlb9MUyheP68wEAAwIAA3gAAyAE','Букет из 7 пион Сара Бернар и эвкалипта','Пионы',2500),(18,NULL,'AgACAgIAAxkBAAEBxzthKgABZ-4BjqarkgjxSxtNPh8D3Z4AAtO0MRv0Z1FJRKkYDMLlyE4BAAMCAAN4AAMgBA','Букет из 5 нежных пион','Пионы',1999),(19,NULL,'AgACAgIAAxkBAAEBx11hKg0zGqztawslwp_cjFwxQFpiiQACb7UxG2N2UElY4VC8_JGE1wEAAwIAA3gAAyAE','Букет с 11 пионами и лавандой','Пионы',4900),(20,NULL,'AgACAgIAAxkBAAEBx2hhKg2H4YTlES5Kd65WzZRiqikYkgACcLUxG2N2UEm1F7KKycgU8QEAAwIAA3gAAyAE','Красивый букет из 7 пион','Пионы',2500),(21,NULL,'AgACAgIAAxkBAAEBx3NhKhC7A_74E5SjW0CCNjmGrg_XDwACdbUxG2N2UEnL4X67E5dXWgEAAwIAA3gAAyAE','Букет из 5 белых кустовых хризантем','Хризантемы',900),(22,NULL,'AgACAgIAAxkBAAEBx35hKhD5GKH_oESdfydyWrJOOeB4LAACdrUxG2N2UEn92kgjuPnyWQEAAwIAA3gAAyAE','Букет из 9 розовых хризантем','Хризантемы',1499),(23,NULL,'AgACAgIAAxkBAAEBx4lhKhKxaE5GkYEYeqIfPV7JEKpYOAACd7UxG2N2UEmK12HmEpsYAgEAAwIAA3gAAyAE','Букет из 9 кустовых хризантем','Хризантемы',1200),(24,NULL,'AgACAgIAAxkBAAEBx5RhKhLo18ogcJeD1Dy4FVvEQSVRRAACeLUxG2N2UElz9sWi7CemyAEAAwIAA3gAAyAE','Букет «Ванильное облако»\n9 кустовых хризантем','Хризантемы',1399),(25,NULL,'AgACAgIAAxkBAAEBx59hKhPmQ0elBLd5nqSnmAxDIxndtwACe7UxG2N2UEnoZa8NgkNeSAEAAwIAA3gAAyAE','Букет Альстромерий','Альстромерии',1300),(26,NULL,'AgACAgIAAxkBAAEBx6phKhQcawkz1UthH8CNW6JR2zlYLgACfLUxG2N2UEm-FnY1V2C4mQEAAwIAA3gAAyAE','Букет Альстромерий Микс','Альстромерии',1200),(27,NULL,'AgACAgIAAxkBAAEBx7VhKhRW-er4ys3Q-CWDVjIhHd4FzAACfbUxG2N2UElxXfh32_V6rwEAAwIAA3gAAyAE','Букет «Предвкушение»\nИз герберы,кустовой розы,писташа','Герберы',1499),(28,NULL,'AgACAgIAAxkBAAEByBthK0ueGoAtiFEwhf61WBhuWBOIPAAC8LMxG2N2YEkgcMvenFqFNwEAAwIAA3gAAyAE','Букет из Гербер и Хризантем','Герберы',1299),(29,NULL,'AgACAgIAAxkBAAEByCZhK0vj_Y-DHGD36sVDTvtCKnxiygAC8bMxG2N2YEmySQ2WkPer3QEAAwIAA3gAAyAE','Букет «Зефир»\nИз:1-й шт. гортензии\n1-й шт. Герберы мини\n1-й шт. Диантуса\n1-й шт. Кустовой розы','Герберы',1600),(30,NULL,'AgACAgIAAxkBAAEByDFhK0zHbwybp3MlsIMZQ1Z5WsDCnQAC8rMxG2N2YEluEpszhAuWhgEAAwIAA3gAAyAE','Букет «На облаках»\nИз 7 шт. Гербер и 7 шт. эвкалипта','Герберы',1699),(31,NULL,'AgACAgIAAxkBAAEByDxhK01nRSKYCSS3yRzfIRxFb3E3QgAC87MxG2N2YEkvVvU3If22gQEAAwIAA3gAAyAE','Букет «Луч Солнца»из Гербер\n11 шт. Гербер\n6 шт. Писташа','Герберы',2100),(32,NULL,'AgACAgIAAxkBAAEByEdhK03dA7GscorJWR2z4McmF9dyqAAC9LMxG2N2YElm3fQGlcuLCQEAAwIAA3gAAyAE','Герберы «Микс»\nИз 9 Гербер','Герберы',1499),(33,NULL,'AgACAgIAAxkBAAEByFJhK06cy6gqrFvXJVjEIMmXy6ocKwAC9bMxG2N2YEkZEqD2XhqJugEAAwIAA3gAAyAE','Букет «Тёплый беж»\nИз 15 штук Гербер Мини','Герберы',1999);
/*!40000 ALTER TABLE `default_buckets` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-08-29 14:24:53

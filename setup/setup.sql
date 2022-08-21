-- -------------------------------------------------------------
-- TablePlus 4.8.2(436)
--
-- https://tableplus.com/
--
-- Database: test_db
-- Generation Time: 2022-08-21 17:16:58.3860
-- -------------------------------------------------------------


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


CREATE TABLE `cart` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(8) COLLATE utf8mb4_bin NOT NULL,
  `product_id` varchar(16) COLLATE utf8mb4_bin NOT NULL,
  `quantity` smallint unsigned NOT NULL DEFAULT '1',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user` (`user_id`),
  CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE `order` (
  `order_id` varchar(16) COLLATE utf8mb4_bin NOT NULL,
  `user_id` varchar(8) COLLATE utf8mb4_bin NOT NULL,
  `total` decimal(8,2) unsigned NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE `order_item` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` varchar(16) COLLATE utf8mb4_bin NOT NULL,
  `product_id` varchar(16) COLLATE utf8mb4_bin NOT NULL,
  `quantity` smallint unsigned NOT NULL DEFAULT '1',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user` (`order_id`),
  CONSTRAINT `fk_order_id` FOREIGN KEY (`order_id`) REFERENCES `order` (`order_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE `product` (
  `product_id` varchar(16) COLLATE utf8mb4_bin NOT NULL,
  `title` varchar(256) COLLATE utf8mb4_bin NOT NULL,
  `price` decimal(8,2) unsigned NOT NULL,
  `quantity` smallint unsigned NOT NULL,
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE `user` (
  `user_id` varchar(8) COLLATE utf8mb4_bin NOT NULL,
  `name` varchar(256) COLLATE utf8mb4_bin DEFAULT NULL,
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

INSERT INTO `order` (`order_id`, `user_id`, `total`, `created`) VALUES
('5ad5308e-212e-11', 'user001', 2300.00, '2022-08-21 08:50:49'),
('e93fdf7e-2127-11', 'user003', 2500.00, '2022-08-21 08:04:41'),
('f765a8de-212e-11', 'user002', 300.00, '2022-08-21 08:55:12');

INSERT INTO `order_item` (`id`, `order_id`, `product_id`, `quantity`, `created`) VALUES
(1, 'e93fdf7e-2127-11', 'product005', 5, '2022-08-21 08:04:42'),
(2, '5ad5308e-212e-11', 'product001', 1, '2022-08-21 08:50:49'),
(3, '5ad5308e-212e-11', 'product002', 2, '2022-08-21 08:50:49'),
(4, '5ad5308e-212e-11', 'product003', 6, '2022-08-21 08:50:49'),
(5, 'f765a8de-212e-11', 'product001', 1, '2022-08-21 08:55:12'),
(6, 'f765a8de-212e-11', 'product002', 1, '2022-08-21 08:55:12');

INSERT INTO `product` (`product_id`, `title`, `price`, `quantity`, `modified`, `created`) VALUES
('product001', 'Title 1', 100.00, 1000, '2022-08-20 16:46:23', '2022-08-20 16:46:23'),
('product002', 'Title 2', 200.00, 2000, '2022-08-20 16:46:23', '2022-08-20 16:46:23'),
('product003', 'Title 3', 300.00, 3000, '2022-08-20 16:46:23', '2022-08-20 16:46:23'),
('product004', 'Title 4', 400.00, 4000, '2022-08-20 16:46:23', '2022-08-20 16:46:23'),
('product005', 'Title 5', 500.00, 5000, '2022-08-20 16:46:23', '2022-08-20 16:46:23');

INSERT INTO `user` (`user_id`, `name`, `modified`, `created`) VALUES
('user001', 'Ben', '2022-08-20 16:40:33', '2022-08-20 16:40:33'),
('user002', 'John', '2022-08-20 16:40:33', '2022-08-20 16:40:33'),
('user003', 'Amy', '2022-08-20 16:40:33', '2022-08-20 16:40:33'),
('user004', 'Sarah', '2022-08-20 16:40:33', '2022-08-20 16:40:33');



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
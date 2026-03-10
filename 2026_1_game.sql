-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: mariadb
-- Generation Time: Mar 07, 2026 at 08:21 AM
-- Server version: 10.6.20-MariaDB-ubu2004
-- PHP Version: 8.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `2026_1_game`
--
CREATE DATABASE IF NOT EXISTS `2026_1_game` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `2026_1_game`;

-- --------------------------------------------------------

--
-- Table structure for table `travels`
--

CREATE TABLE `travels` (
  `travel_pk` char(32) NOT NULL,
  `travel_title` varchar(20) NOT NULL,
  `travel_date_from` bigint(20) NOT NULL,
  `travel_date_to` bigint(20) NOT NULL,
  `travel_description` varchar(500) NOT NULL,
  `travel_location` varchar(100) NOT NULL,
  `travel_country` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_pk` char(32) NOT NULL,
  `user_first_name` varchar(20) NOT NULL,
  `user_last_name` varchar(20) NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `user_password` varchar(255) NOT NULL,
  `user_created_at` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_pk`, `user_first_name`, `user_last_name`, `user_email`, `user_password`, `user_created_at`) VALUES
('8fcf604be3794825b8fc380fa60a5eaa', 'aa', 'bb', 'aa@a.com', 'scrypt:32768:8:1$L2kz5lr62KVyaXDA$fc36678e2dc4f9f9e09fc742961b27cd6220492320fcaf664fc66ce37bdef2af6d1fe8360753575ffbd4d9cae2046aee0c3387d75a3d84906e25060e67c47b8d', 1772725543);

-- --------------------------------------------------------

--
-- Table structure for table `user_travels`
--

CREATE TABLE `user_travels` (
  `user_fk` char(32) NOT NULL,
  `travel_fk` char(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `travels`
--
ALTER TABLE `travels`
  ADD PRIMARY KEY (`travel_pk`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_pk`),
  ADD UNIQUE KEY `user_email` (`user_email`);

--
-- Indexes for table `user_travels`
--
ALTER TABLE `user_travels`
  ADD KEY `user_fk` (`user_fk`),
  ADD KEY `travel_fk` (`travel_fk`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `user_travels`
--
ALTER TABLE `user_travels`
  ADD CONSTRAINT `travel_fk` FOREIGN KEY (`travel_fk`) REFERENCES `travels` (`travel_pk`),
  ADD CONSTRAINT `user_fk` FOREIGN KEY (`user_fk`) REFERENCES `users` (`user_pk`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

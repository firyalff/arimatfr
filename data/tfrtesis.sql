-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Sep 17, 2017 at 05:29 PM
-- Server version: 10.1.26-MariaDB
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tfrtesis`
--

-- --------------------------------------------------------

--
-- Table structure for table `asfr`
--

CREATE TABLE `asfr` (
  `year` int(11) NOT NULL,
  `age` int(11) NOT NULL,
  `rate` double NOT NULL,
  `prediction` double DEFAULT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `asfr_error_log`
--

CREATE TABLE `asfr_error_log` (
  `batch_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `age` int(11) NOT NULL,
  `mean_squared_error` double NOT NULL,
  `mean_absolute_error` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `asfr_prediction`
--

CREATE TABLE `asfr_prediction` (
  `batch_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `year` int(11) NOT NULL,
  `age` int(11) NOT NULL,
  `prediction` double NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tfr`
--

CREATE TABLE `tfr` (
  `year` int(11) NOT NULL,
  `rate` double NOT NULL,
  `rateyoung` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tfr_error_log`
--

CREATE TABLE `tfr_error_log` (
  `batch_id` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mean_squared_error` double NOT NULL,
  `mean_absolute_error` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tfr_prediction`
--

CREATE TABLE `tfr_prediction` (
  `batch_id` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `year` int(11) NOT NULL,
  `prediction` double NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `asfr_error_log`
--
ALTER TABLE `asfr_error_log`
  ADD KEY `batch_id` (`batch_id`);

--
-- Indexes for table `asfr_prediction`
--
ALTER TABLE `asfr_prediction`
  ADD KEY `batch_id` (`batch_id`);

--
-- Indexes for table `tfr_error_log`
--
ALTER TABLE `tfr_error_log`
  ADD KEY `batch_id` (`batch_id`);

--
-- Indexes for table `tfr_prediction`
--
ALTER TABLE `tfr_prediction`
  ADD KEY `batch_id` (`batch_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

/*
SQLyog Community Edition- MySQL GUI v7.0  
MySQL - 5.0.51b-community-nt : Database - james
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`james` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `james`;

/*Table structure for table `globalvars` */

DROP TABLE IF EXISTS `globalvars`;

CREATE TABLE `globalvars` (
  `user_id` varchar(200) NOT NULL,
  `study_day` int(11) NOT NULL,
  `varkey` varchar(200) NOT NULL,
  `varvalue` varchar(200) default NULL,
  PRIMARY KEY  (`user_id`,`study_day`,`varkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `logs` */

DROP TABLE IF EXISTS `logs`;

CREATE TABLE `logs` (
  `user_id` varchar(200) NOT NULL,
  `log_entry` varchar(5000) NOT NULL,
  `log_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `motivation` */

DROP TABLE IF EXISTS `motivation`;

CREATE TABLE `motivation` (
  `user_id` varchar(200) NOT NULL,
  `study_day` int(11) NOT NULL,
  `motivation` varchar(200) NOT NULL,
  `rating` int(11) default NULL,
  PRIMARY KEY  (`user_id`,`study_day`,`motivation`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `usedfiles` */

DROP TABLE IF EXISTS `usedfiles`;

CREATE TABLE `usedfiles` (
  `user_id` varchar(200) NOT NULL,
  `filename` varchar(200) NOT NULL,
  `day_used` int(11) default NULL,
  PRIMARY KEY  (`user_id`,`filename`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `user_id` varchar(200) NOT NULL,
  `start_date` date default NULL,
  `study_day` int(11) default NULL,
  `study_condition` varchar(4) default NULL,
  `email` varchar(200) default NULL,
  `interaction_day` int(11) default NULL,
  `last_login` date default NULL,
  PRIMARY KEY  (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;

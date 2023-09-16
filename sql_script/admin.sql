/*
Navicat MySQL Data Transfer

Source Server         : 本机
Source Server Version : 50724
Source Host           : localhost:3306
Source Database       : flaskproject

Target Server Type    : MYSQL
Target Server Version : 50724
File Encoding         : 65001

Date: 2023-09-10 18:48:54
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `nickname` varchar(15) NOT NULL,
  `mobile` bigint(11) NOT NULL,
  `password` varchar(15) NOT NULL,
  PRIMARY KEY (`mobile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES ('root', '0', '123456');
INSERT INTO `admin` VALUES ('zhengdx', '15815023612', '123456');
INSERT INTO `admin` VALUES ('wy', '18127670413', '123456');

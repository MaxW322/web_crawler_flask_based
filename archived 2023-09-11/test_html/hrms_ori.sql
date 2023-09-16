/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50627
Source Host           : localhost:3306
Source Database       : HRMS

Target Server Type    : MYSQL
Target Server Version : 50627
File Encoding         : 65001

Date: 2020-01-13 20:31:52
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `admin`
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `account` varchar(15) NOT NULL,
  `password` varchar(15) NOT NULL,
  PRIMARY KEY (`account`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES ('root', '123456');

-- ----------------------------
-- Table structure for `staff`
-- ----------------------------
DROP TABLE IF EXISTS `staff`;
CREATE TABLE `staff` (
  `staff_num` varchar(15) NOT NULL,
  `staff_name` varchar(15) NOT NULL,
  `gender` varchar(50) DEFAULT NULL,
  `age` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `marriage` varchar(50) DEFAULT NULL,
  `post` varchar(50) DEFAULT NULL,
  `department_num` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`staff_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of `staff`
-- ----------------------------
INSERT INTO `staff` VALUES ('10001', '张三', '男', '22', '18112341234', '已婚', '员工', '001');
INSERT INTO `staff` VALUES ('10002', '赵五', '男', '22', '18112341236', '已婚', '经理', '001');
INSERT INTO `staff` VALUES ('20001', '李四', '女', '23', '18112341266', '未婚', '经理', '002');
INSERT INTO `staff` VALUES ('20002', '魏二', '女', '23', '18112341239', '未婚', '员工', '002');
INSERT INTO `staff` VALUES ('30001', '郭六', '女', '23', '18112341237', '未婚', '经理', '003');
INSERT INTO `staff` VALUES ('30002', '杨七', '男', '22', '18112341238', '已婚', '员工', '003');


-- ----------------------------
-- Table structure for `department`
-- ----------------------------
DROP TABLE IF EXISTS `department`;
CREATE TABLE `department` (
  `department_num` varchar(50) NOT NULL,
  `department_name` varchar(50) NOT NULL,
  PRIMARY KEY (`department_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of teacher_basic
-- ----------------------------
INSERT INTO `department` VALUES ('001', '人事部');
INSERT INTO `department` VALUES ('002', '市场部');
INSERT INTO `department` VALUES ('003', '客服部');

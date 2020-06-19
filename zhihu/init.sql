
-- 建表语句
CREATE TABLE `zhihu` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_name` varchar(256) DEFAULT NULL COMMENT '用户名',
  `sex` varchar(32) DEFAULT NULL COMMENT '性别',
  `user_sign` varchar(256) DEFAULT NULL COMMENT '用户签名',
  `user_avatar` varchar(512) DEFAULT NULL COMMENT '所在头像',
  `user_url` varchar(1024) DEFAULT NULL COMMENT '用户主页地址',
  `user_add` varchar(1024) DEFAULT NULL COMMENT '用户关注列表',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `zhihu_activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_name` varchar(256) DEFAULT NULL COMMENT '用户名',
  `title` varchar(512) DEFAULT NULL COMMENT '活动名称',
  `activity_type` varchar(64) DEFAULT NULL COMMENT '活动类型(如关注的列表)',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
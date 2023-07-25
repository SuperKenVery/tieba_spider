CREATE TABLE `tieba` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(256) NOT NULL COMMENT '帖子标题',
  `create_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `creator` varchar(64) NOT NULL COMMENT '创建人',
  `content` mediumtext COMMENT '帖子内容',
  `link` varchar(2048) DEFAULT NULL COMMENT '链接',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='百度贴吧';


CREATE TABLE `tieba_reply` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reply_id` varchar(256) NOT NULL COMMENT '回复ID',
  `create_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `creator` varchar(64) NOT NULL COMMENT '创建人',
  `content` mediumtext COMMENT '回复内容',
  `link` varchar(2048) DEFAULT NULL COMMENT '帖子链接',
  `sex` varchar(16) DEFAULT NULL COMMENT '性别',
  `location` varchar(20) DEFAULT NULL COMMENT '地区',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='百度贴吧帖子回复';
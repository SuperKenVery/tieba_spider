CREATE TABLE `school_news` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(256) NOT NULL COMMENT '新闻标题',
  `create_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `creator` varchar(64) NOT NULL COMMENT '创建人',
  `content` mediumtext COMMENT '文章内容',
  `link` varchar(2048) DEFAULT NULL COMMENT '链接',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7196 DEFAULT CHARSET=utf8 COMMENT='学校新闻';
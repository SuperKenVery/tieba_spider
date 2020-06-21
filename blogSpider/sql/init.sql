CREATE TABLE `articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(256) NOT NULL DEFAULT '' COMMENT '文章标题',
  `content` mediumtext NOT NULL  COMMENT '文章内容',
  `origin_url` varchar(256)  COMMENT '原文链接',
  `cover_images` text  COMMENT '封面图链接',
  `spider_time` TIMESTAMP  DEFAULT CURRENT_TIMESTAMP  COMMENT '采集时间',
  `origin_name` varchar(256)  COMMENT '来源网站',
  `has_publish` smallint(2)  COMMENT '是否已发布(0未发布;已发布)',
  `publish_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP  COMMENT '发布时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='文章列表';

CREATE TABLE `images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `href` varchar(256) NOT NULL DEFAULT '' COMMENT '图片链接',
  `has_publish` smallint(2)  COMMENT '是否已发布(0未发布;1已发布)',
  `publish_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP  COMMENT '发布时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='图片列表';
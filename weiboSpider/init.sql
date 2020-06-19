CREATE TABLE `weibo` (
  `id` varchar(64) NOT NULL COMMENT '主键',
  `bid` varchar(64) NOT NULL COMMENT '微博ID',
  `user_id` varchar(11) NOT NULL COMMENT '用户ID',
  `screen_name` varchar(64) NOT NULL COMMENT '用户昵称',
  `text` varchar(1024) NOT NULL COMMENT '微博内容',
  `topics` varchar(1024) NOT NULL COMMENT '话题',
  `at_users` varchar(1024) NOT NULL COMMENT '@的用户',
  `pics` varchar(1024) NOT NULL COMMENT '图片列表',
  `video_url` varchar(1024) NOT NULL COMMENT '视频列表',
  `location` varchar(128) NOT NULL COMMENT '发布地点',
  `created_at` datetime NOT NULL COMMENT '发布时间',
  `source` varchar(128) NOT NULL COMMENT '微博来源',
  `attitudes_count` int(11) NOT NULL COMMENT '点赞数',
  `comments_count` int(11) NOT NULL COMMENT '评论数',
  `reposts_count` int(11) NOT NULL COMMENT '转发数',
  `retweet_id` varchar(32) NOT NULL COMMENT '转发数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `comments` (
  `id` varchar(64) NOT NULL COMMENT '主键',
  `mid` varchar(64) NOT NULL COMMENT '评论ID',
  `screen_name` varchar(64) DEFAULT NULL COMMENT '用户昵称',
  `like_count` int(11) DEFAULT NULL COMMENT '喜欢的数量',
  `floor_number` int(11) DEFAULT NULL COMMENT '楼层数',
  `follow_count` int(11) DEFAULT NULL COMMENT '回复数',
  `source` varchar(128) DEFAULT NULL COMMENT '来源',
  `comment` varchar(1024) DEFAULT NULL COMMENT '评论内容',
  `gender` varchar(32) DEFAULT NULL COMMENT '性别',
  `rootid` varchar(64) DEFAULT NULL COMMENT '根评论ID',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
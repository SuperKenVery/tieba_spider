CREATE TABLE `feiyan_data` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `province_name` varchar(64) DEFAULT NULL COMMENT '国家、省份',
  `province_id` varchar(64) DEFAULT NULL COMMENT '国家ID',
  `continents` varchar(64) DEFAULT NULL COMMENT '州（亚洲、欧洲等等）',
  `current_confirmed_count` int(10) DEFAULT NULL COMMENT '当前确诊人数',
  `confirmed_count` int(10) DEFAULT NULL COMMENT '确诊总人数',
  `cured_count` int(10) DEFAULT NULL COMMENT '治愈人数',
  `dead_count` int(10) DEFAULT NULL COMMENT '死亡人数',
  `suspected_count` int(10) DEFAULT NULL COMMENT '疑似病例',
  `country_type` int(10) DEFAULT NULL COMMENT '国家类型',
  `modify_time` datetime DEFAULT NULL COMMENT '更新时间',
  `is_new` smallint(2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7178 DEFAULT CHARSET=utf8 COMMENT='肺炎疫情实时数据';


CREATE TABLE `feiyan_incr` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `province_name` varchar(64) DEFAULT NULL,
  `modify_time` datetime DEFAULT NULL,
  `confirmed_count` int(10) DEFAULT NULL,
  `confirmed_incr` int(10) DEFAULT NULL COMMENT '新增确诊人数',
  `cured_count` int(10) DEFAULT NULL COMMENT '治愈人数',
  `cured_incr` int(10) DEFAULT NULL COMMENT '新增治愈人数',
  `dead_count` int(10) DEFAULT NULL COMMENT '死亡人数',
  `dead_incr` int(10) DEFAULT NULL COMMENT '新增死亡人数',
  `current_confirmed_count` int(10) DEFAULT NULL COMMENT '当前确诊人数',
  `current_confirmed_incr` int(10) DEFAULT NULL COMMENT '当前新增确诊人数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12119 DEFAULT CHARSET=utf8 COMMENT='肺炎疫情每日数据新增';

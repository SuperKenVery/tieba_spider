CREATE TABLE `job_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_name` varchar(64) NOT NULL DEFAULT '' COMMENT '岗位名称',
  `position` varchar(64)  COMMENT '地理位置',
  `edu_level` varchar(64)  COMMENT '学历要求',
  `working_exp` varchar(64)  COMMENT '工作经历',
  `people_num` varchar(64)  COMMENT '招聘人数',
  `welfare` varchar(64)  COMMENT '公司福利',
  `salary` varchar(64)  COMMENT '薪资',
  `job_detail` text  COMMENT '岗位描述',
  `company_name` varchar(256)   COMMENT '公司名称',
  `company_type` varchar(64)   COMMENT '公司性质',
  `company_industry` varchar(64)   COMMENT '公司所在行业',
  `company_size` varchar(64)   COMMENT '公司规模',
  `company_display` varchar(256)   COMMENT '公司地点',
  `company_desc` text  COMMENT '公司描述',
  `company_url` varchar(64)  COMMENT '公司招聘主页',
  `update_date` varchar(32)  COMMENT '更新时间',
  `position_url` varchar(64)  COMMENT '详情页链接',
  PRIMARY KEY (`id`),
  INDEX INDEX_position(`position`),
  INDEX INDEX_edu_level(`edu_level`),
  INDEX INDEX_working_exp(`working_exp`),
  INDEX INDEX_salary(`salary`),
  INDEX INDEX_company_type(`company_type`),
  INDEX INDEX_company_industry(`company_industry`),
  INDEX INDEX_company_size(`company_size`),
  INDEX INDEX_company_display(`company_display`),
  FULLTEXT INDEX INDEX_job_detail(`job_detail`),
  FULLTEXT INDEX INDEX_company_desc(`company_desc`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='岗位信息表';




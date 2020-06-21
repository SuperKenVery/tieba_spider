CREATE TABLE `proxy_ip` (
`id`  int(10) NOT NULL AUTO_INCREMENT ,
`ip`  varchar(32) NULL COMMENT 'IP地址' ,
`port`  int(10) NULL COMMENT '端口号' ,
`speed`  double(10,0) NULL COMMENT '速度' ,
`proxy_type`  varchar(16) NULL COMMENT '代理类型' ,
PRIMARY KEY (`id`)
);
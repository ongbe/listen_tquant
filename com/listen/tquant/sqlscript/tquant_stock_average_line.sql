CREATE TABLE `tquant_stock_average_line` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT '主键id',
	`security_code` VARCHAR(20) NOT NULL COMMENT '股票代码',
	`exchange_code` VARCHAR(20) NOT NULL COMMENT '交易所标识,SZ,SH',
	`the_date` DATE NOT NULL COMMENT '交易日',
	`ma` INT(11) NOT NULL COMMENT '均线类型，5-5日均线，10-10日均线等',
	`close` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '日收盘价',
	`close_avg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT 'ma日均收盘价',
	`close_pre_avg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '前一ma日均收盘价',
	`close_avg_chg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT 'ma日均收盘价波动幅度（涨跌幅）',
	`close_avg_chg_avg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT 'ma日均收盘价波动幅度（涨跌幅）均',
	`amount` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '当日成交额(元)',
	`amount_avg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT 'ma日均成交额(元)',
	`amount_pre_avg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '前一ma日均成交额(元)',
	`amount_avg_chg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT 'ma日均交易额涨跌幅',
	`amount_avg_chg_avg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT 'ma日均交易额涨跌幅均',
	`vol` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '当日成交量(手)',
	`vol_avg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT 'ma日均成交量(手)',
	`vol_pre_avg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '前一ma日均成交量(手)',
	`vol_avg_chg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT 'ma日均成交量涨跌幅',
	`vol_avg_chg_avg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT 'ma日均成交量涨跌幅均',
	`price_avg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT 'ma日均成交价价（平均成交价）',
	`price_pre_avg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '前一ma日均成交价',
	`price_avg_chg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT 'ma日均成交价涨跌幅',
	`price_avg_chg_avg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT 'ma日均成交价涨跌幅均',
	`amount_flow_chg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '日金钱流向涨跌幅',
	`amount_flow_chg_avg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '日金钱流向涨跌幅均',
	`vol_flow_chg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '日成交量流向涨跌幅',
	`vol_flow_chg_avg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '日成交量流向涨跌幅均',
	`close_ma_price_avg_chg` DECIMAL(20,2) NULL DEFAULT NULL COMMENT '收盘价/ma日均价幅度',
	`auto_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '时间戳',
	PRIMARY KEY (`id`),
	UNIQUE INDEX `security_code_the_date_ma` (`security_code`, `the_date`, `ma`, `exchange_code`),
	INDEX `security_code` (`security_code`),
	INDEX `auto_date` (`auto_date`),
	INDEX `ma` (`ma`)
)
COMMENT='股票均线数据\r\nma日均收盘价=sum(前ma日(含)的收盘价)/ma\r\nma日均收盘价涨跌幅=(ma日均收盘价 - 前一ma日均收盘价)/前一ma日均收盘价 * 100\r\nma日均收盘价涨跌幅均=sum(前ma日(含)均收盘价涨跌幅)/ma\r\n\r\nma日均成交额=sum(前ma日(含)的成交额)/ma\r\nma日均成交额涨跌幅=(ma日均成交额 - 前一ma日均成交额)/前一ma日均成交额 * 100\r\nma日均成交额涨跌幅均=sum(前ma日(含)均成交额涨跌幅)/ma\r\n\r\nma日均成交量=sum(前ma日(含)的成交量)/ma\r\nma日均成交量涨跌幅=(ma日均成交量 - 前一ma日均成交量)/前一ma日均成交量 * 100\r\nma日均成交量涨跌幅均=sum(前ma日(含)均成交量涨跌幅)/ma\r\n\r\nma日均成交价=sum(前ma日(含)的成交额)/sum(ma日(含)的成交量)\r\nma日均成交价涨跌幅=(ma日均成交价 - 前一ma日均成交价)/前一ma日均成交价 * 100\r\nma日均成交价涨跌幅均=sum(前ma日(含)均成交价涨跌幅)/ma\r\n\r\n日金钱流向涨跌幅=日成交额/ma日(含)均成交额 * 100\r\n日金钱流向涨跌幅均=sum(前ma日(含)金钱流向涨跌幅)/ma\r\n\r\n日成交量流向涨跌幅=日成交量/ma日(含)均成交量 * 100\r\n日成交量流向涨跌幅均=sum(前ma日(含)成交量流向涨跌幅)/ma\r\n'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=15644
;

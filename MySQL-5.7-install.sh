#!/bin/bash
############################
# description:MySQL5.7自动安装脚本,本脚本适用于CentOS/RedHat 6.X和7.X
# version：2.5.2
# author: <zhaojinlong898@qq.com>
# date:2017-11-7
############################

export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin

# Check if user is root
if [ $UID -ne 0 ];then
   echo "Must be use ROOT"
   exit 1
fi 

###### 参数设置 #######################################################
# CentOS系统大版本:6或7
SYSVS=7
#hostname=mysqldb
# RAM为物理内存大小，单位：G
RAM=16
ip_last=58

PORT=3306
BASEDIR=/usr/local
DATADIR=/data/mysql
SOCK=${BASEDIR}/mysql/mysql${PORT}.sock
MYPW=rootroot
INPUT=/data/tools/mysql-5.7.19-linux-glibc2.12-x86_64.tar.gz
#######################################################################

#源码依赖包
#yum -y update
#yum -y install gcc gcc-c++ automake autoconf openssl openssl-devel zlib zlib-devel libaio wget lsof vim-enhanced sysstat ntpdate
################

# 新建用户
groupadd mysql
useradd -r -g mysql -M -s /sbin/nologin mysql
 
 
# 下载解压
#wget https://cdn.mysql.com//Downloads/MySQL-5.7/$mysql_version
tar xf ${INPUT} -C ${BASEDIR}/src
ln -s ${BASEDIR}/src/mysql-5.7.*-linux-glibc*-x86_64 ${BASEDIR}/mysql
mkdir -p ${BASEDIR}/{src,mysql/{logs,tmp}}
chown mysql.mysql ${BASEDIR}/src/mysql-5.7.*-linux-glibc*-x86_64  ${BASEDIR}/mysql /data/mysql -R


# 添加环境变量
echo export PATH='${PATH}':${BASEDIR}/mysql/bin > /etc/profile.d/mysql.sh
source /etc/profile


# 添加mysql类到系统中
echo "${BASEDIR}/mysql/lib" >> /etc/ld.so.conf.d/mysql.conf
ldconfig


# 修改启动脚本;默认安装在/usr/local/目录下；
sed -i "s#/usr/local/mysql#${BASEDIR}/mysql#g" ${BASEDIR}/mysql/bin/mysqld_safe
sed -i "s#/usr/local/mysql#${BASEDIR}/mysql#g" ${BASEDIR}/mysql/support-files/mysql.server


# 修改配置文件
cat > /etc/my.cnf << EOF
[client]
port = ${PORT}
socket = ${SOCK}
default-character-set=utf8

[mysql]
prompt="\u@`hostname` \R:\m:\s [\d]> "
no-auto-rehash
 
[mysqld]
user = mysql
port = ${PORT}
socket = ${SOCK}
pid-file = `hostname`.pid
basedir = ${BASEDIR}/mysql
datadir = ${DATADIR}
event_scheduler = 0
explicit-defaults-for-timestamp=on
tmpdir = ${BASEDIR}/mysql/tmp

######timeout settings######
interactive_timeout = 300
wait_timeout = 300
 
character-set-server = utf8mb4

########connection settings########
lower_case_table_names=1
open_files_limit = 65535
max_connections = 1024
max_user_connections= 1998
max_connect_errors = 100000

########log settings########
log-output=file
slow_query_log = 1
slow_query_log_file = ${BASEDIR}/mysql/logs/slow.log
log-error = ${BASEDIR}/mysql/logs/error.log
log_error_verbosity=2
pid-file = mysql.pid
long_query_time = 1
log-slow-slave-statements = 1
 
#####binlog settings#######
server-id = ${ip_last}
auto_increment_increment = 1
auto_increment_offset = 1
binlog_format = row
log-bin = ${BASEDIR}/mysql/logs/mysql-bin
binlog_cache_size = 4M
max_binlog_size = 1G
max_binlog_cache_size = 2G
sync_binlog = 1
expire_logs_days = 90
#procedure 
log_bin_trust_function_creators=1
 
####GTID settings########
gtid-mode=on
binlog_gtid_simple_recovery = 1
enforce_gtid_consistency = 1
log_slave_updates
 
####relay log settings#####
skip_slave_start = 1
max_relay_log_size = 128M
relay_log_purge = 1
relay_log_recovery = 1
relay-log=${BASEDIR}/mysql/logs/relay-bin
relay-log-index=${BASEDIR}/mysql/logs/relay-bin.index
#skip-grant-tables
 
####buffers & cache settings########
table_open_cache = 4096
table_definition_cache = 4096
max_heap_table_size = 96M
sort_buffer_size = 16M
join_buffer_size = 16M
thread_cache_size = 3000
query_cache_size = 0
query_cache_type = 0
query_cache_limit = 256K
query_cache_min_res_unit = 512
thread_stack = 192K
tmp_table_size = 96M
key_buffer_size = 8M
read_buffer_size = 2M
read_rnd_buffer_size = 16M
bulk_insert_buffer_size = 32M
 
#######myisam sttings#####
myisam_sort_buffer_size = 128M
myisam_max_sort_file_size = 10G
myisam_repair_threads = 1
 
#####innodb settings######
innodb_buffer_pool_size = $[${RAM}*7/10]G
innodb_buffer_pool_instances = 1
innodb_data_file_path = ibdata1:1G:autoextend
innodb_flush_log_at_trx_commit = 1
innodb_log_buffer_size = 1G
innodb_log_file_size = 100M
innodb_log_files_in_group = 3
innodb_max_dirty_pages_pct = 50
innodb_file_per_table = 1 
innodb_status_file = 1
innodb_buffer_pool_load_at_startup = 1
innodb_buffer_pool_dump_at_shutdown = 1
transaction_isolation = READ-COMMITTED
innodb_flush_method = O_DIRECT
innodb_lock_wait_timeout = 10
innodb_rollback_on_timeout = 1
innodb_print_all_deadlocks = 1
innodb_file_per_table = 1
innodb_online_alter_log_max_size = 1G
internal_tmp_disk_storage_engine = InnoDB
innodb_stats_on_metadata = 0

######io settings############
innodb_io_capacity = 4000
innodb_io_capacity_max = 8000
innodb_flush_neighbors = 0
innodb_write_io_threads = 8
innodb_read_io_threads = 8
innodb_purge_threads = 4
innodb_page_cleaners = 4


######innodb monitor settings#####
innodb_monitor_enable="module_innodb"
innodb_monitor_enable="module_server"
innodb_monitor_enable="module_dml"
innodb_monitor_enable="module_ddl"
innodb_monitor_enable="module_trx"
innodb_monitor_enable="module_os"
innodb_monitor_enable="module_purge"
innodb_monitor_enable="module_log"
innodb_monitor_enable="module_lock"
innodb_monitor_enable="module_buffer"
innodb_monitor_enable="module_index"
innodb_monitor_enable="module_ibuf_system"
innodb_monitor_enable="module_buffer_page"
innodb_monitor_enable="module_adaptive_hash"


[mysqldump]
quick
max_allowed_packet = 32M
EOF
 
 
# 初始化数据库
cd ${BASEDIR}/mysql/
./bin/mysqld --initialize-insecure --basedir=${BASEDIR}/mysql --datadir=${DATADIR} --user=mysql


# 添加到系统服务并启动
if [ ${SYSVS} -eq 7 ];
	then
		# 添加到系统服务7
cat > /usr/lib/systemd/system/mysqld.service << EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target

[Install]
WantedBy=multi-user.target

[Service]
User=mysql
Group=mysql
ExecStart=${BASEDIR}/mysql/bin/mysqld --defaults-file=/etc/my.cnf
LimitNOFILE = 5000
EOF
		systemctl enable mysqld.service
		systemctl list-unit-files | grep mysql
		systemctl start mysqld.service
		# systemctl disable mysqld.service
	else
		# 添加到系统服务6
		chmod 755 support-files/mysql.server
		cp support-files/mysql.server /etc/init.d/mysqld
		chkconfig --add mysqld
		chkconfig mysqld on
		chkconfig --list mysqld
		service mysqld start
fi

 
# PW=`cat /data/mysql/mysql${PORT}/data/error.log |grep "root@localhost"|awk -F " " '{print $11}'`
# mysqladmin -u root password '${MYPW}'
# mysql -uroot -p${PW} -e 'set password=password('${MYPW}');'
# mysql -uroot -p${PW} -e 'UPDATE mysql.user SET authentication_string=password('${MYPW}') WHERE user='root';'
#
# cd ${BASEDIR}/mysql/ && ./bin/mysql_secure_installation 
echo 'The installation is complete!'

#!/bin/bash
###################
# 二进制自动安装数据库脚本root密码letian318将脚本和安装包放在/root目录即可
# 程序目录/usr/local/mysql
# 数据目录/data/mysql
# 日志目录/log/mysql
# 端口号默认3306
# author：898009427@qq.com
####################

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

# Check if user is root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script, please use root to install"
    exit 1
fi

clear
echo "========================================================================="
echo "A tool to auto-compile & install MySQL 5.6.36 on Redhat/CentOS6.* Linux "
echo "========================================================================="
cur_dir=$(pwd)
#set mysql root password
echo "==========================="
mysqlrootpwd="letian318"
echo -e "Please input the root password of mysql:"
read -p "(Default password: letian318):" mysqlrootpwd
if [ "$mysqlrootpwd" = "" ]; then
mysqlrootpwd="letian318"
fi
echo "==========================="
echo "MySQL root password:$mysqlrootpwd"
echo "==========================="
#which MySQL Version do you want to install?
echo "==========================="
isinstallmysql56="n"
echo "Install MySQL 5.6.36,Please input y"
read -p "(Please input y , n):" isinstallmysql56
case "$isinstallmysql56" in
y|Y|Yes|YES|yes|yES|yEs|YeS|yeS)
echo "You will install MySQL 5.6.36"
isinstallmysql56="y"
;;
*)
echo "INPUT error,You will exit install MySQL 5.6.36"
isinstallmysql56="n"
    exit
esac
get_char()
{
SAVEDSTTY=`stty -g`
stty -echo
stty cbreak
#dd if=/dev/tty bs=1 count=1 2> /dev/null
stty -raw
stty echo
stty $SAVEDSTTY
}
echo ""
echo "Press any key to start...or Press Ctrl+c to cancel"
char=`get_char`
# Initialize  the installation related content.
function InitInstall()
{
cat /etc/issue
uname -a
MemTotal=`free -m | grep Mem | awk '{print  $2}'`  
echo -e "\n Memory is: ${MemTotal} MB "
#Set timezone
#rm -rf /etc/localtime
#ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
    #Delete Old Mysql program
rpm -qa|grep mysql
rpm -e mysql
#yum -y remove mysql-server mysql mysql-libs
#yum -y remove php-mysql
#yum -y install yum-fastestmirror
#yum -y update
#Disable SeLinux
if [ -s /etc/selinux/config ]; then
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
fi
    setenforce 0
}
#Installation of depend on and optimization options.
function InstallDependsAndOpt()
{
cd $cur_dir
cat >>/etc/security/limits.conf<<EOF
mysql soft nproc 10240
mysql hard nproc 10240
* soft nofile 10240
* hard nofile 10240
EOF
echo "fs.file-max=65535" >> /etc/sysctl.conf
echo "deadline" >/sys/block/sda/queue/scheduler
echo "vm.swappiness = 0" >>/etc/sysctl.conf
}
#Install MySQL
function InstallMySQL56()
{
echo "============================Install MySQL 5.6.36=================================="
cd $cur_dir
#Backup old my.cnf
#rm -f /etc/my.cnf
if [ -s /etc/my.cnf ]; then
    mv /etc/my.cnf /etc/my.cnf.`date +%Y%m%d%H%M%S`.bak
fi
#mysql directory configuration
groupadd mysql -g 512
useradd -u 512 -g mysql -s /sbin/nologin -d /home/mysql mysql
tar xvf /root/mysql-5.6.36-linux-glibc2.5-x86_64.tar.gz
mv /root/mysql-5.6.36-linux-glibc2.5-x86_64 /usr/local/mysql
mkdir -p /data/mysql
mkdir -p /log/mysql
chown -R mysql:mysql /data/mysql
chown -R mysql:mysql /usr/local/mysql
chown -R mysql:mysql /log
#edit /etc/my.cnf
SERVERID=`ifconfig eth0 | grep "inet addr" | awk '{ print $2}'| awk -F. '{ print $3$4}'`
cat >>/etc/my.cnf<<EOF
[client]
port= 3306
socket= /tmp/mysql.sock
default-character-set=utf8
[mysql]
prompt="\\u@\\h:\p  \\R:\\m:\\s [\\d]>"
default-character-set=utf8
no-auto-rehash
[mysqld]
port= 3306
socket= /tmp/mysql.sock
basedir= /usr/local/mysql
datadir= /data/mysql
#timeout
interactive_timeout = 300
wait_timeout = 300

#character set
character-set-server = utf8

open_files_limit = 65535
max_connections = 1024
max_connect_errors = 100000

default_time_zone = SYSTEM
skip-name-resolve = 1
#logs
log-output=file
slow_query_log = 1
slow_query_log_file = slow.log
log-error = error.log
log_warnings = 2
pid-file = mysql.pid
long_query_time = 1
#log-slow-admin-statements = 1
#log-queries-not-using-indexes = 1
log-slow-slave-statements = 1

#binlog
binlog_format = row
server-id = 203306
log-bin = mybinlog
binlog_cache_size = 4M
max_binlog_size = 1G
max_binlog_cache_size = 2G
sync_binlog = 1
expire_logs_days = 10

#relay log
skip_slave_start = 1
max_relay_log_size = 1G
relay_log_purge = 1
relay_log_recovery = 1
log_slave_updates
#slave-skip-errors=1032,1053,1062

explicit_defaults_for_timestamp=1
#buffers & cache
table_open_cache = 2048
table_definition_cache = 2048
table_open_cache = 2048
max_heap_table_size = 96M
sort_buffer_size = 2M
join_buffer_size = 2M
thread_cache_size = 256
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

#innodb
default_storage_engine = InnoDB
#innodb_buffer_pool_size  memery 60%-80%
innodb_buffer_pool_size = 100M
#innodb_buffer_pool_instances = (cpu -1)
innodb_buffer_pool_instances = 1
innodb_data_file_path = ibdata1:1G:autoextend
innodb_flush_log_at_trx_commit = 1
innodb_log_buffer_size = 64M
innodb_log_file_size = 500M
innodb_log_files_in_group = 3
innodb_max_dirty_pages_pct = 50
innodb_file_per_table = 1
innodb_rollback_on_timeout
innodb_status_file = 1
innodb_io_capacity = 2000
transaction_isolation = READ-COMMITTED
innodb_flush_method = O_DIRECT
EOF
/usr/local/mysql/scripts/mysql_install_db --basedir=/usr/local/mysql --datadir=/data/mysql --defaults-file=/etc/my.cnf --user=mysql
cp /usr/local/mysql/support-files/mysql.server /etc/init.d/mysqld
chmod 700 /etc/init.d/mysqld
chkconfig --add mysqld
chkconfig --level 2345 mysqld on
cat > /etc/ld.so.conf.d/mysql-x86_64.conf<<EOF
/usr/local/mysql/lib
EOF
ldconfig
if [ -d "/proc/vz" ];then
ulimit -s unlimited
fi
/etc/init.d/mysqld start
cat >> /etc/profile <<EOF
export PATH=$PATH:/usr/local/mysql/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/mysql/lib
EOF
source /etc/profile
/usr/local/mysql/bin/mysqladmin -u root password $mysqlrootpwd
cat > /tmp/mysql_sec_script<<EOF
use mysql;
delete from mysql.user where user!='root' or host!='localhost';
grant all privileges on *.* to  'sys_admin'@'%' identified by 'letian318';
flush privileges;
truncate table db;
drop database test;
EOF
/usr/local/mysql/bin/mysql -u root -p$mysqlrootpwd -h localhost < /tmp/mysql_sec_script
#rm -f /tmp/mysql_sec_script
/etc/init.d/mysqld restart
echo "============================MySQL 5.6.36 install completed========================="
}
function CheckInstall()
{
echo "===================================== Check install ==================================="
clear
ismysql=""
echo "Checking..."
if [ -s /usr/local/mysql/bin/mysql ] && [ -s /usr/local/mysql/bin/mysqld_safe ] && [ -s /etc/my.cnf ]; then
  echo "MySQL: OK"
  ismysql="ok"
  else
  echo "Error: /usr/local/mysql not found!!!MySQL install failed."
fi
if [ "$ismysql" = "ok" ]; then
echo "Install MySQL 5.6.36 completed! enjoy it."
echo "========================================================================="
netstat -ntl
else
echo "Sorry,Failed to install MySQL!"
echo "You can tail /root/mysql-install.log from your server."
fi
}
#The installation log
InitInstall 2>&1 | tee /root/mysql-install.log
CheckAndDownloadFiles 2>&1 | tee -a /root/mysql-install.log
InstallDependsAndOpt 2>&1 | tee -a /root/mysql-install.log
InstallMySQL56 2>&1 | tee -a /root/mysql-install.log
CheckInstall 2>&1 | tee -a /root/mysql-install.log

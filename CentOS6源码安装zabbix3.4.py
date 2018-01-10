zabbix源码安装

推荐使用"notepad++"打开此文档， "alt+0"将函数折叠后方便查阅

0.环境：
	CentOS:	6.9
	IP:192.168.1.92
	JDK：1.7.0.45
	ngingx:	1.13.6
	mysql:	5.7.15-linux-glibc2.5-x86_64
	php:	5.6.31
	zabbix:	3.4.2

	源码包存放路径：/data/tools/
	安装路径：		/usr/local/



1.关闭防火墙和selinux
	1.1. 关闭iptables
	]# service iptables stop
	iptables: Setting chains to policy ACCEPT: filter          [  OK  ]
	iptables: Flushing firewall rules:                         [  OK  ]
	iptables: Unloading modules:                               [  OK  ]
	]# chkconfig --level 35 iptables off

	1.2. 关闭selinux
	]# sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
	]# setenforce 0
	]# getenforce 		# 查看selinux的模式
	开启模式显示结果：Enforcing
	关闭模式显示结果：Disabled



2.二进制安装JDK（1.7.0.45）：用于java-geteway
	2.1. 上传JDK1.7到/data/tools/目录下，解压：
	]# tar xf jdk-7u45-linux-x64.tar.gz -C /opt/

	2.2. 添加环境变量，添加Java进程；
	]# vim /etc/profile
	# java
	export JAVA_HOME=/opt/jdk1.7.0_45
	export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH
	export CLASSPATH=.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib 
	]# source /etc/profile 	# 使配置文件立即生效；
	]# echo $PATH
	]# java -version			# 验证

	
	
3.安装编译工具
	]# yum install gcc gcc-c++ make automake autoconf
	包 gcc-4.4.7-18.el6.x86_64 已安装并且是最新版本
	包 gcc-c++-4.4.7-18.el6.x86_64 已安装并且是最新版本
	包 1:make-3.81-23.el6.x86_64 已安装并且是最新版本
	包 automake-1.11.1-4.el6.noarch 已安装并且是最新版本
	包 autoconf-2.63-5.1.el6.noarch 已安装并且是最新版本
	无须任何处理

	
	
4.源码安装ngingx(1.13.6)
	4.1 下载解压编译
	]# yum install pcre-devel openssl-devel
	软件包                                                架构                                     版本                                          仓库   
	===========================================================================================================================
	正在安装:
	 openssl-devel                                         x86_64                                   1.0.1e-57.el6                                     base   
	 pcre-devel                                            x86_64                                   7.8-7.el6                                         base   
	为依赖而安装:
	 keyutils-libs-devel                                   x86_64                                   1.4-5.el6                                         base   
	 krb5-devel                                            x86_64                                   1.10.3-65.el6                                     base   
	 libcom_err-devel                                      x86_64                                   1.41.12-23.el6                                    base   
	 libkadm5                                              x86_64                                   1.10.3-65.el6                                     base   
	 libselinux-devel                                      x86_64                                   2.0.94-7.el6                                      base   
	 libsepol-devel                                        x86_64                                   2.0.41-4.el6                                      base   
	 zlib-devel                                            x86_64                                   1.2.3-29.el6                                      base   
	为依赖而更新:
	 e2fsprogs                                             x86_64                                   1.41.12-23.el6                                    base   
	 e2fsprogs-libs                                        x86_64                                   1.41.12-23.el6                                    base   
	 krb5-libs                                             x86_64                                   1.10.3-65.el6                                     base   
	 libcom_err                                            x86_64                                   1.41.12-23.el6                                    base   
	 libss                                                 x86_64                                   1.41.12-23.el6                                    base   
	 openssl                                               x86_64                                   1.0.1e-57.el6                                     base   
	=============================================================================================
	]# useradd -u 888 -M -s /sbin/nologin www
	]# mkdir -pv /data/tools/
	]# cd /data/tools/
	]# wget http://nginx.org/download/nginx-1.13.6.tar.gz
	]# tar xf nginx-1.13.6.tar.gz 
	]# cd nginx-1.13.6
	]# ./configure --prefix=/usr/local/nginx-1.13.6 --user=www --group=www --with-http_ssl_module --with-http_stub_status_module
	]# echo $?	
	0
	]# make && make install
	]# ln -s  /usr/local/nginx-1.13.6 /usr/local/nginx

	4.2 配置
	]# cat /usr/local/nginx/conf/nginx.conf					# 全部替换
	worker_processes  1;
	events {
		worker_connections  1024;
	}
	
	http {
		include       mime.types;
		default_type  application/octet-stream;
		log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
						  '$status $body_bytes_sent "$http_referer" '
						  '"$http_user_agent" "$http_x_forwarded_for"';
		sendfile        on;
		keepalive_timeout  65;
		
		server {
			listen       80;
			server_name  localhost;
			access_log  logs/host.access.log  main;
			root   html;
			index  index.php index.html index.htm;

			error_page   500 502 503 504  /50x.html;
			location = /50x.html {
				root   html;
			}
			
			location ~ .*\.(php|php5)?$ {
				fastcgi_pass   127.0.0.1:9000;
				fastcgi_index  index.php;
				include        fastcgi.conf;
			}
		}
	}


	4.3 启动nginx
	]# cd /usr/local/nginx/sbin
	]# ./nginx
	]# ss -tnl | grep 80



5.二进制安装mysql(5.7.15)
	5.1. 说明
	mysql版本：mysql-5.7.15-linux-glibc2.5-x86_64.tar.gz
	mysql程序安装路径：/data/mysql
	mysql数据存放路径：/data/mysql/data
	socket存放路径： /data/mysql/mysql.sock
	安装方式：二进制安装

	5.2. 新建用户
	]# groupadd mysql
	]# useradd -r -g mysql -M -s /bin/false mysql

	5.3. 下载解压
	]# cd /data/tools
	]# wget https://cdn.mysql.com/archives/mysql-5.7/mysql-5.7.15-linux-glibc2.5-x86_64.tar.gz
	]# tar -xvf  mysql-5.7.15-linux-glibc2.5-x86_64.tar.gz -C /data
	]# ln -s mysql-5.7.15-linux-glibc2.5-x86_64  /data/mysql
	]# chown -R mysql:mysql /data/mysql/

	5.4. 添加环境变量：
	]# echo "PATH=$PATH:/data/mysql/bin" > /etc/profile.d/mysql.sh
	]# source /etc/profile/mysql.sh
	]# echo $PATH				#验证

	5.5. 添加mysql类到系统中
	]# rpm -qa | grep mysql
	]# rpm -e mysql		# 卸载掉rpm安装的mysql,不然后面编译zabbix会报错；
	]# echo '/data/mysql/lib' >> /etc/ld.so.conf
	]# ldconfig			# 重新加载动态链接库

	5.6. 修改启动脚本
	# 如果安装在/usr/local/mysql/目录下，则两个sed不许执行，因为默认安装在/usr/local/目录下；
	]# sed -i 's#/usr/local/mysql#/data/mysql#g' /data/mysql/bin/mysqld_safe
	]# sed -i 's#/usr/local/mysql#/data/mysql#g' /data/mysql/support-files/mysql.server

	5.7. 初始化数据库
	]# cd /data/mysql/
	]# ./bin/mysqld --initialize --basedir=/data/mysql --datadir=/data/mysql/data --user=mysql
	2017-07-11T07:34:36.210764Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
	2017-07-11T07:34:37.826785Z 0 [Warning] InnoDB: New log files created, LSN=45790
	2017-07-11T07:34:38.275547Z 0 [Warning] InnoDB: Creating foreign key constraint system tables.
	2017-07-11T07:34:38.487524Z 0 [Warning] No existing UUID has been found, so we assume that this is the first time that this server has been started. Generating a new UUID: 65189e9f-660b-11e7-912f-b0518e005cf6.
	2017-07-11T07:34:38.544417Z 0 [Warning] Gtid table is not ready to be used. Table 'mysql.gtid_executed' cannot be opened.
	2017-07-11T07:34:38.545337Z 1 [Note] A temporary password is generated for root@localhost: chpta=hXj4*#
	# 注意：root@localhost：后面的是临时密码，如果没有输出上面的信息，请把/etc/my.cnf文件移走。

	5.8.	修改配置文件
	]# vim /etc/my.cnf
	[client]
	port                               = 3306
	socket                             = /data/mysql/mysql.sock
	default-character-set              = utf8

	[mysqld]
	user                               = mysql
	port                               = 3306
	basedir                            = /data/mysql
	datadir                            = /data/mysql/data
	socket                             = /data/mysql/mysql.sock
	character-set-server               = utf8
	collation-server                   = utf8_general_ci
	innodb_file_per_table              = 1
	lower_case_table_names             = 1
	skip_name_resolve                  = 1
	open_files_limit                   = 65535
	back_log                           = 1024
	max_connections                    = 512
	max_connect_errors                 = 1000000
	table_open_cache_instances         = 64
	thread_stack                       = 512K
	external-locking                   = FALSE
	max_allowed_packet                 = 32M
	sort_buffer_size                   = 16M
	join_buffer_size                   = 16M
	thread_cache_size                  = 768
	query_cache_size                   = 0
	query_cache_type                   = 0
	interactive_timeout                = 600
	wait_timeout                       = 600
	tmp_table_size                     = 96M
	max_heap_table_size                = 96M
	log_error                          = /data/mysql/error.log
	slow_query_log                     = 1
	slow_query_log_file                = /data/mysql/slow.log
	long_query_time                    = 1
	binlog-ignore-db                   = mysql
	log-bin                            = /data/mysql/mysql-bin
	sync_binlog                        = 1
	binlog_cache_size                  = 4M
	max_binlog_cache_size              = 2G
	max_binlog_size                    = 1G
	expire_logs_days                   = 90
	default-storage-engine             = InnoDB

	[mysqldump]
	quick
	max_allowed_packet                 = 32M


	5.9.	将服务脚本复制到/etc/init.d目录下，并添加到服务列表
	]# cp  support-files/mysql.server  /etc/init.d/mysqld
	]# ll  /etc/init.d/mysqld 		#查看是否有执行权限
	-rwxr-xr-x 1 root root 10856 8月  12 12:04 /etc/init.d/mysqld

	5.10.	添加开机自启动
	]# chkconfig --add mysqld
	]# chkconfig mysqld on
	]# chkconfig --list mysqld

	5.11.	启动mysql
	]#  /data/mysql/bin/mysqld_safe  &			#守护进程能在崩溃后自动重启，推荐
	或者
	]# service mysqld status
	]# ps -ef  | grep mysql							#查看是否运行

	12.	配置安全策略：
	]# /data/mysql/bin/mysql_secure_installation 

	Securing the MySQL server deployment.

	Enter password for user root: 		#输入初始化时的临时密码

	The existing password for the user account root has expired. Please set a new password.

	New password: 		#设置新密码

	Re-enter new password: 	#重复新密码

	VALIDATE PASSWORD PLUGIN can be used to test passwords
	and improve security. It checks the strength of password
	and allows the users to set only those passwords which are
	secure enough. Would you like to setup VALIDATE PASSWORD plugin?

	Press y|Y for Yes, any other key for No: y		#是否设置密码安全插件(不是DBA，不推荐设置)

	There are three levels of password validation policy:

	LOW    Length >= 8
	MEDIUM Length >= 8, numeric, mixed case, and special characters
	STRONG Length >= 8, numeric, mixed case, special characters and dictionary                  file

	Please enter 0 = LOW, 1 = MEDIUM and 2 = STRONG: 0			#选择0，长度大于8位；根据自己设置
	Using existing password for root.

	Estimated strength of the password: 100 
	Change the password for root ? ((Press y|Y for Yes, any other key for No) : n	#是否更改root的现有密码

	 ... skipping.
	By default, a MySQL installation has an anonymous user,
	allowing anyone to log into MySQL without having to have
	a user account created for them. This is intended only for
	testing, and to make the installation go a bit smoother.
	You should remove them before moving into a production
	environment.

	Remove anonymous users? (Press y|Y for Yes, any other key for No) : y	#删除匿名用户
	Success.


	Normally, root should only be allowed to connect from
	'localhost'. This ensures that someone cannot guess at
	the root password from the network.

	Disallow root login remotely? (Press y|Y for Yes, any other key for No) : y	#禁止root登录远程
	Success.

	By default, MySQL comes with a database named 'test' that
	anyone can access. This is also intended only for testing,
	and should be removed before moving into a production
	environment.


	Remove test database and access to it? (Press y|Y for Yes, any other key for No) : y		#删除测试数据库
	 - Dropping test database...
	Success.

	 - Removing privileges on test database...
	Success.

	Reloading the privilege tables will ensure that all changes
	made so far will take effect immediately.

	Reload privilege tables now? (Press y|Y for Yes, any other key for No) : y		#重新加载权限表
	Success.

	All done! 
	]# 

	5.13. 增加zabbix用户及授权
	]# mysql -uroot -p 
	]# mysql> create database zabbix character set utf8 collate utf8_bin; 
	]# mysql> grant all privileges on zabbix.* to "zabbix"@"%" identified by '<password>'; 
	]# mysql> quit;



6.源码安装php(5.6.31)
	6.1 安装依赖包
	]# wget -O /etc/yum.repos.d/epel.repo  http://mirrors.aliyun.com/repo/epel-6.repo
	]# yum install curl curl-devel freetype freetype-devel gd gd-devel libjpeg libjpeg-devel libjpeg-turbo-devel 
	 软件包                                               架构                                   版本                                                仓库    
	=======================================================================================================================================
	正在安装:
	 freetype-devel                                       x86_64                                 2.3.11-17.el6                                       base    
	 gd                                                   x86_64                                 2.0.35-11.el6                                       base    
	 gd-devel                                             x86_64                                 2.0.35-11.el6                                       base    
	 libcurl-devel                                        x86_64                                 7.19.7-53.el6_9                                     updates 
	 libjpeg-turbo-devel                                  x86_64                                 1.2.1-3.el6_5                                       base    
	正在升级:
	 curl                                                 x86_64                                 7.19.7-53.el6_9                                     updates 
	为依赖而安装:
	 fontconfig-devel                                     x86_64                                 2.8.0-5.el6                                         base    
	 libX11-devel                                         x86_64                                 1.6.4-3.el6                                         base    
	 libXau-devel                                         x86_64                                 1.0.6-4.el6                                         base    
	 libXpm                                               x86_64                                 3.5.10-2.el6                                        base    
	 libXpm-devel                                         x86_64                                 3.5.10-2.el6                                        base    
	 libidn-devel                                         x86_64                                 1.18-2.el6                                          base    
	 libpng-devel                                         x86_64                                 2:1.2.49-2.el6_7                                    base    
	 libxcb-devel                                         x86_64                                 1.12-4.el6                                          base    
	 xorg-x11-proto-devel                                 noarch                                 7.7-14.el6                                          base    
	为依赖而更新:
	 libX11                                               x86_64                                 1.6.4-3.el6                                         base    
	 libX11-common                                        noarch                                 1.6.4-3.el6                                         base    
	 libcurl                                              x86_64                                 7.19.7-53.el6_9                                     updates 
	 libxcb                                               x86_64                                 1.12-4.el6                                          base    
	=========================================================================================================================================================
	包 curl-7.19.7-53.el6_9.x86_64 已安装并且是最新版本
	包 libcurl-devel-7.19.7-53.el6_9.x86_64 已安装并且是最新版本
	包 freetype-2.3.11-17.el6.x86_64 已安装并且是最新版本
	包 freetype-devel-2.3.11-17.el6.x86_64 已安装并且是最新版本
	包 gd-2.0.35-11.el6.x86_64 已安装并且是最新版本
	包 gd-devel-2.0.35-11.el6.x86_64 已安装并且是最新版本
	包 libjpeg-turbo-1.2.1-3.el6_5.x86_64 已安装并且是最新版本
	包 libjpeg-turbo-devel-1.2.1-3.el6_5.x86_64 已安装并且是最新版本
	包 libjpeg-turbo-devel-1.2.1-3.el6_5.x86_64 已安装并且是最新版本
	无须任何处理

	]# yum install libpng libpng-devel libxml2-devel libcurl-devel libxslt-devel zlib zlib-devel
	依赖关系解决
	============================================================================================================================================
	 软件包                                               架构                                     版本        										仓库    
	=============================================================================================================================================
	正在安装:
	 libxml2-devel                                        x86_64                                   2.7.6-21.el6_8.1                                   base
	 libxslt-devel                                        x86_64                                   1.1.26-2.el6_3.1                                   base
	为依赖而安装:
	 libgcrypt-devel                                      x86_64                                   1.4.5-12.el6_8                                     base
	 libgpg-error-devel                                   x86_64                                   1.7-4.el6                                          base
	 libxslt                                              x86_64                                   1.1.26-2.el6_3.1                                   base
	为依赖而更新:
	 libgcrypt                                            x86_64                                   1.4.5-12.el6_8                                     base
	 libxml2                                              x86_64                                   2.7.6-21.el6_8.1                                   base
	 libxml2-python                                       x86_64                                   2.7.6-21.el6_8.1                                   base
	============================================================================================================================================
	包 2:libpng-1.2.49-2.el6_7.x86_64 已安装并且是最新版本
	包 2:libpng-devel-1.2.49-2.el6_7.x86_64 已安装并且是最新版本
	包 libxml2-devel-2.7.6-21.el6_8.1.x86_64 已安装并且是最新版本
	包 libcurl-devel-7.19.7-53.el6_9.x86_64 已安装并且是最新版本
	包 libxslt-devel-1.1.26-2.el6_3.1.x86_64 已安装并且是最新版本
	包 zlib-1.2.3-29.el6.x86_64 已安装并且是最新版本
	包 zlib-devel-1.2.3-29.el6.x86_64 已安装并且是最新版本
	无须任何处理

	]# yum install openldap  openldap-devel
	依赖关系解决
	=================================================================================================================================================
	 软件包                                             架构                                     版本                                                 仓库   
	=================================================================================================================================================
	正在安装:
	 openldap-devel                                     x86_64                                   2.4.40-16.el6                                        base
	正在升级:
	 openldap                                           x86_64                                   2.4.40-16.el6                                        base
	为依赖而安装:
	 cyrus-sasl-devel                                   x86_64                                   2.1.23-15.el6_6.2                                    base
	=================================================================================================================================================

	
	]# yum install libmcrypt libmcrypt-devel mhash mcrypt			# epel
	依赖关系解决
	======================================================================================================================================================
	 软件包                                             架构                                      版本                                               仓库
	======================================================================================================================================================
	正在安装:
	 libmcrypt                                          x86_64                                    2.5.8-9.el6                                        epel
	 libmcrypt-devel                                    x86_64                                    2.5.8-9.el6                                        epel
	 mcrypt                                             x86_64                                    2.6.8-10.el6                                       epel
	 mhash                                              x86_64                                    0.9.9.9-3.el6                                      epel
	======================================================================================================================================================

	6.2 安装libiconv包（php版本5.5及以上内嵌）
	]# yum localinstall libiconv-1.15-1.x86_64.rpm
	或
	]# tar xf libiconv-1.15.tar.gz 
	]# cd libiconv-1.15
	]# ./configure --prefix=/usr/local/libiconv
	]# echo $?
	]# make && make install
	]# libtool --finish /usr/local/libiconv/lib
	]# echo '/usr/local/libiconv/lib' >> /etc/ld.so.conf
	]# cat /etc/ld.so.conf
	include ld.so.conf.d/*.conf
	/data/mysql/lib
	/usr/local/libiconv/lib
	]# ldconfig

	6.3 编译安装php
	]# cd /data/tools/
	]# tar xf php-5.6.31.tar.gz
	]# cd php-5.6.31/
	]# ./configure \
	--prefix=/usr/local/php-5.6.31 \
	--enable-mysqlnd \
	--with-mysql=mysqlnd \
	--with-mysqli=mysqlnd \
	--with-pdo-mysql=mysqlnd \
	--with-iconv-dir=/usr/local/libiconv \
	--with-freetype-dir \
	--with-jpeg-dir \
	--with-png-dir \
	--with-zlib \
	--with-libxml-dir=/usr \
	--with-ldap \
	--enable-xml \
	--disable-rpath \
	--enable-bcmath \
	--enable-shmop \
	--enable-sysvsem \
	--enable-inline-optimization \
	--with-curl \
	--enable-mbregex \
	--enable-fpm \
	--enable-mbstring \
	--with-mcrypt \
	--with-gd \
	--with-gettext \
	--enable-gd-native-ttf \
	--with-openssl \
	--with-mhash \
	--enable-pcntl \
	--enable-sockets \
	--with-xmlrpc \
	--enable-zip \
	--enable-soap \
	--enable-short-tags \
	--enable-static \
	--with-xsl \
	--with-fpm-user=www \
	--with-fpm-group=www \
	--enable-opcache=no  \
	--enable-ftp
	
	]# cp -frp /usr/lib64/libldap* /usr/lib/		#报configure: error: Cannot find ldap libraries in /usr/lib.时执行
	]# echo $?
	0
	]# make && make install

	]# cp /data/tools/php-5.6.31/php.ini-production /usr/local/php-5.6.31/lib/php.ini
	]# ln -s /usr/local/php-5.6.31 /usr/local/php
	]# cp /usr/local/php/etc/php-fpm.conf.default /usr/local/php/etc/php-fpm.conf

	6.4 配置

	查看php模块
	]# /usr/local/php/bin/php -m
	[PHP Modules]
	bcmath
	Core
	ctype
	curl
	date
	dom
	ereg
	fileinfo
	filter
	ftp
	gd
	gettext
	hash
	iconv
	json
	ldap
	libxml
	mbstring
	mcrypt
	mhash
	mysql
	mysqli
	mysqlnd
	openssl
	pcntl
	pcre
	PDO
	pdo_mysql
	pdo_sqlite
	Phar
	posix
	Reflection
	session
	shmop
	SimpleXML
	soap
	sockets
	SPL
	sqlite3
	standard
	sysvsem
	tokenizer
	xml
	xmlreader
	xmlrpc
	xmlwriter
	xsl
	zip
	zlib
	[Zend Modules]

	修改php配置文件
	]# egrep -n "^post_max_size|^max_execution_time|^max_input_time|^date.timezone|^always_populate_raw_post_data" /usr/local/php/lib/php.ini
	372:max_execution_time = 30
	382:max_input_time = 60
	660:post_max_size = 8M

	]# sed -i 's#max_execution_time = 30#max_execution_time = 300#;s#max_input_time = 60#max_input_time =300#;s#post_max_size = 8M#post_max_size = 16M#;s#;always_populate_raw_post_data = -1#always_populate_raw_post_data = -1#;s#;date.timezone =#date.timezone = Asia/Shanghai#' /usr/local/php/lib/php.ini
	
	]# egrep -n "^post_max_size|^max_execution_time|^max_input_time|^date.timezone|^always_populate_raw_post_data" /usr/local/php/lib/php.ini
	372:max_execution_time = 300
	382:max_input_time =300
	660:post_max_size = 16M
	702:always_populate_raw_post_data = -1
	936:date.timezone = Asia/Shanghai

	6.5 启动PHP
	]# /usr/local/php/sbin/php-fpm -t
	]# /usr/local/php/sbin/php-fpm

	6.6 测试（可选）

	测试php
	]# cat index.php 
	<?php
	phpinfo();
	?>

	测试php连接mysql
	]# cat test_mysql.php 
	<?php
			//$link_id=mysql_connect('主机名','用户','密码');
			$link_id=mysql_connect('192.168.1.92','zabbix','zabbix') or mysql_error();
			if($link_id){
					echo "mysql successful by oldboy !\n";
			}else{
					echo "mysql_error()";

			}

	?>



7.源码安装zabbix(3.4.2)
	7.1 依赖包
	]# yum install net-snmp net-snmp-devel fping unixODBC-devel openssl-devel OpenIPMI-devel libevent libevent-devel pcre-devel
	依赖关系解决
	=====================================================================================================================================================
	 软件包                                                架构                                   版本                                                  仓库   
	=====================================================================================================================================================
	正在安装:
	 OpenIPMI-devel                                        x86_64                                 2.0.16-14.el6                                         base
	 fping                                                 x86_64                                 2.4b2-10.el6                                          epel
	 libevent                                              x86_64                                 1.4.13-4.el6                                          base
	 libevent-devel                                        x86_64                                 1.4.13-4.el6                                          base
	 net-snmp                                              x86_64                                 1:5.5-60.el6                                          base
	 net-snmp-devel                                        x86_64                                 1:5.5-60.el6                                          base
	 unixODBC-devel                                        x86_64                                 2.2.14-14.el6                                         base
	为依赖而安装:
	 OpenIPMI                                              x86_64                                 2.0.16-14.el6                                         base
	 OpenIPMI-libs                                         x86_64                                 2.0.16-14.el6                                         base
	 elfutils-devel                                        x86_64                                 0.164-2.el6                                           base
	 elfutils-libelf-devel                                 x86_64                                 0.164-2.el6                                           base
	 file-devel                                            x86_64                                 5.04-30.el6                                           base
	 libevent-doc                                          noarch                                 1.4.13-4.el6                                          base
	 libevent-headers                                      noarch                                 1.4.13-4.el6                                          base
	 lm_sensors-devel                                      x86_64                                 3.1.1-17.el6                                          base
	 lm_sensors-libs                                       x86_64                                 3.1.1-17.el6                                          base
	 ncurses-devel                                         x86_64                                 5.7-4.20090207.el6                                    base
	 net-snmp-libs                                         x86_64                                 1:5.5-60.el6                                          base
	 popt-devel                                            x86_64                                 1.13-7.el6                                            base
	 rpm-devel                                             x86_64                                 4.8.0-55.el6                                          base
	 tcp_wrappers-devel                                    x86_64                                 7.6-58.el6                                            base
	 unixODBC                                              x86_64                                 2.2.14-14.el6                                         base
	====================================================================================================================================================


	7.2 安装
	]# useradd zabbix -s /sbin/nologin
	]# cd /data/tools/
	]# tar xf zabbix-3.4.2.tar.gz
	]# cd zabbix-3.4.2
	]# ./configure --prefix=/usr/local/zabbix-3.4.2 --enable-server --enable-agent --enable-java --with-mysql --enable-ipv6 --with-net-snmp --with-libcurl --with-libxml2 --with-openipmi --with-unixodbc --with-openssl
	]# ln -s /usr/local/mysql/lib/libmysqlclient.so /usr/lib 	# 报错时执行：configure: error: Not found mysqlclient library
	]# echo $?
	0
	]# make && make install			# 如果报错：../../../include/zbxdb.h:65:20: error: mysql.h: No such file or directory； 说明：zabbix编译时找不到mysql.h文件，请卸载系统自带的mysql，或安装 mysql-devel包

	]# ln -s /usr/local/zabbix-3.4.2 /usr/local/zabbix

	7.3 导入数据库
	]# cd /data/tools/zabbix-3.4.2/database/mysql
	]# mysql -uzabbix -p<password> zabbix < schema.sql
	]# mysql -uzabbix -p<password> zabbix < images.sql
	]# mysql -uzabbix -p<password> zabbix < data.sql

	]# ln -s /usr/local/zabbix/etc/ /etc/zabbix
	]# ln -s /usr/local/zabbix/bin/* /usr/bin/
	]# ln -s /usr/local/zabbix/sbin/* /usr/sbin/

	7.4  拷贝启动脚本
	]# cd /data/tools/zabbix-3.4.2/misc/init.d/fedora/core
	]# cp zabbix_* /etc/init.d/

	7.5  修改启动文件
	]# sed -i "s@BASEDIR=/usr/local@BASEDIR=/usr/local/zabbix@g" /etc/init.d/zabbix_server 
	]# sed -i "s@BASEDIR=/usr/local@BASEDIR=/usr/local/zabbix@g" /etc/init.d/zabbix_agentd

	7.6  修改zabbix服务端配置文件
	]# egrep -v '^$|#' /etc/zabbix/zabbix_server.conf
	LogFile=/tmp/zabbix_server.log
	DBHost=localhost
	DBName=zabbix
	DBUser=zabbix
	DBPassword=<password>		#数据库中zabbix用户的密码
	DBSocket=/data/mysql/mysql.sock
	Timeout=4
	LogSlowQueries=3000


	7.7  修改zabbix客户端配置文件
	]# egrep -v '^$|#' /etc/zabbix/zabbix_agentd.conf
	LogFile=/tmp/zabbix_agentd.log
	Server=127.0.0.1			# 被动模式中服务端或代理端的IP地址
	ServerActive=127.0.0.1		# 主动模式中服务端或代理端的IP地址
	Hostname=zabbix				# 当前客户端所在服务器的主机名；

	7.8  复制zabbix站点到nginx站点目录
	]# cp -a /data/tools/zabbix-3.4.2/frontends/php /usr/local/nginx/html/zabbix

	7.9  站点授权
	]# chown -R www.www /usr/local/nginx/html/zabbix


	7.10  启动zabbix服务
	]# service zabbix_server start	# 启动zabbix服务端
	]# ss -tnl |grep 10051
	]# service zabbix_agentd start	# 启动zabbix客户端
	]# ss -tnl |grep 10050

	7.11 访问zabbix
	http://192.168.1.92/zabbix
	
	第一步：您应该看到前端安装向导的第一个屏幕；
	第二步：确保满足php所有软件先决条件；
	第三步：输入连接到数据库的详细信息。必须已经创建了Zabbix数据库并授权；
				数据库类型：mysql
				host ：localhost		# 不行的话，可以尝试：127.0.0.1
				port ：0				# 0表示默认 
				DB name： zabbix 		# 库名称
				user ：zabbix			# mysql用户
				password ：密码			# mysql普通用户密码
	第四步：输入Zabbix服务器详细信息；
	第五步：查看设置摘要；
	第六步：完成安装；安装后生成的配置文件：/usr/local/nginx-1.13.6/html/zabbix/conf/zabbix.conf.php
	第七步：Zabbix前端准备好了！默认用户名为：Admin，密码：zabbix；
	
	
	
	7.12 zabbix客户端：其它主机采用rpm安装
		]# yum install zabbix-agent zabbix-sender

		]# vim /etc/zabbix/zabbix_agentd.conf（3个*号开头的必须配置）
        #### Passive checks related (被动检测相关的配置：agent等待server过来请求数据)
            *Server=127.0.0.1   
                # 定义了被动模式中服务端或代理端的IP地址，多个用逗号隔开授权给哪些zabbix-server或zabbix-proxy过来采集数据的服务器地址列表；
            ListenPort=10050
            ListenIP=0.0.0.0    # 本机的所有地址；
            StartAgents=3       # agent进程数量；

        #### Active checks related（主动检测相关的配置：agent主动向server发送监控数据）
            *ServerActive=IP[:Port]
                # 定义了主动模式中服务端或代理端的IP地址，多个用逗号隔开，当前agent主动发送监控数据到server端；
            *Hostname=HOSTNAME  # 当前客户端所在服务器的主机名；
		或
		]# sed -i 's#^Server=127.0.0.1#Server=192.168.20.59#g;s#^ServerActive=127.0.0.1#ServerActive=192.168.20.59#g' /etc/zabbix/zabbix_agentd.conf		# zabbix服务端不改，
		]# sed -i "s#Hostname=Zabbix server#Hostname=`hostname`#g" /etc/zabbix/zabbix_agentd.conf
		]# egrep -v "^$|#" /etc/zabbix/zabbix_agentd.conf
		LogFile=/tmp/zabbix_agentd.log
		Server=127.0.0.1
		ServerActive=127.0.0.1
		Hostname=zabbix
    启动服务：
        ]# service zabbix-agent start  
        ]# service zabbix-agent status 
        ]# ss -tnl | grep :10050
        ]# iptables -vnL     #防火墙没有阻断10050端口；
			

	7.13 JMX监控tomcat
	Zabbix 的JMX监控架构
		zaibbix Server-->Java gateway-->JMX counter

	服务器端：
	安装JMX：推荐安装在server端,别处也可以；
		]# yum -y install zabbix-java-gateway
		]# service zabbix-java-gateway status 

	修改Java-gateway配置文件   
		]# vim /etc/zabbix/zabbix_java_gateway.conf
			# 监听地址
			LISTEN_IP="0.0.0.0"
			# 监听端口
			LISTEN_PORT=10052
			# PID_FILE文件
			PID_FILE="/var/run/zabbix/zabbix_java.pid"
			# 开启的工作线程数
			START_POLLERS=5
			# 超时时间
			TIMEOUT=3
	启动zabbix-java-gateway:
		]# cd /usr/local/zabbix/sbin/zabbix_java
		]# ./startup.sh				#启动
		]# ./shutdown.sh			#停止
		或
		]# service zabbix-java-gateway start			#rpm
		
		]# ss -tnl | grep 10052
			LISTEN     0      50           *:10052                    *:*  
	  
	修改zabbix_server的配置文件并重启
		]# vim /etc/zabbix/zabbix_server.conf     #修改下面几个参数：
			# JavaGateway的所在服务器IP地址
			JavaGateway=192.168.1.91
			# JavaGateway的服务端口
			JavaGatewayPort=10052
			# 从javaGateway采集数据的进程数
			StartJavaPollers=5
		
	 配置文件修改后，重启zabbix-server：
		]# service zabbix-server restart
	 
	 
	 客户端：
	 添加tomact中JMX的参数：在文件开头配置即可。
		# vim $tomcat/bin/catalina.sh 
			CATALINA_OPTS="$CATALINA_OPTS
			-Dcom.sun.management.jmxremote
			-Dcom.sun.management.jmxremote.port=12345    # JMX端口，默认12345
			-Dcom.sun.management.jmxremote.authenticate=false
			-Dcom.sun.management.jmxremote.ssl=false
			-Djava.rmi.server.hostname=192.168.20.60"    # 本机IP
	导入模板到zabbix，并关联到主机，添加监控
	新建主机，配置JMX接口
	 
	   选择配置：主机-模板-选择-模板-：
			Template JMX Tomcat
			Template JMX Generic
	 导入JMX模板
	 
	 查看JMX是否生效，可重启tomcat进程和zabbix-java-gateway服务
	 查看图形



8.中文乱码
	]# yum install wqy-microhei-fonts -y
	]# cp /usr/share/fonts/wqy-microhei/wqy-microhei.ttc /usr/local/nginx/html/zabbix/fonts/DejaVuSans.ttf
	或
	把win系统里的楷体常规上传到服务器上：C:\Windows\Fonts\simkai.ttf
	]# cd /usr/local/nginx/html/zabbix/fonts
	]# rz simkai.ttf
	]# mv DejaVuSans.ttf DejaVuSans.ttf.bak
	]# mv simkai.ttf DejaVuSans.ttf
	]# chown -R www.www *
	]# ll
	总用量 12252
	-rw-r--r-- 1 www www 11785184 7月  17 2016 DejaVuSans.ttf
	-rw-r--r-- 1 www www   756072 9月  25 22:17 DejaVuSans.ttf.bak



9.附
	警告
	PHP gettext	off		Warning

	两种方法：
	9.1. 重新编译加上 --with-gettext
	  
	9.2. 添加php动态扩展库
	进入php 源码包ext 目录下我们会发现有个 gettext 模块
	执行如下命令
	 /usr/local/php-5.6.31/bin/phpize           #   /usr/local/php-5.6.31/  php安装路径
	./configure --with-php-config=/usr/local/php-5.6.31/bin/php-config
	make && make install

	/usr/local/php-5.6.31/lib/php.ini    #根据自己系统安装路径而定
	在php.ini里添加上gettext.so
	echo "extension = gettext.so" >> /usr/local/php/lib/php.ini

	缺少mysqli  同理
	--with-mysqli=/usr/local/mysql/bin/mysql_config

	echo " extension = mysqli.so" > /usr/local/php/lib/php.ini

	查看php已经编译的模块
	/usr/local/php/bin/php -m



10.在Windows上安装Zabbix agent客户端
	
	下载地址:https://www.zabbix.com/downloads/3.4.0/zabbix_agents_3.4.0.win.zip
	在Windows系统C盘新建zabbix目录
	将下载好的安装包（zabbix_agents_3.4.0.win.zip）解压缩到c:/zabbix/目录下：
		zabbix_agents_3.4.0.win
		├── bin
		│   ├── win32
		│   │   ├── dev
		│   │   │   ├── zabbix_sender.dll
		│   │   │   └── zabbix_sender.lib
		│   │   ├── zabbix_agentd.exe
		│   │   ├── zabbix_get.exe
		│   │   └── zabbix_sender.exe
		│   └── win64
		│       ├── dev
		│       │   ├── zabbix_sender.dll
		│       │   └── zabbix_sender.lib
		│       ├── zabbix_agentd.exe
		│       ├── zabbix_get.exe
		│       └── zabbix_sender.exe
		└── conf
			└── zabbix_agentd.win.conf

		conf目录存放是agent配置文件
		bin文件存放windows下32位和64位安装程序。
	在c:/zabbix/目录下新建zabbix-agent.log文本文件

	配置C:\zabbix\conf\zabbix_agentd.win.conf文件:
		LogFile=C:\zabbix\zabbix-agent.log
		Server=192.168.1.59
		ServerActive=192.168.1.59
		Hostname=Windows_36
			
			修改log路径;
			
			Server:  zabbix server的ip地址，
			ServerActive: zabbix 主动监控server的ip地址，
			其中Server和ServerActive都指定zabbix Server的IP地址，不同的是，前者是被动后者是主动。
			也就是说Server这个配置是用来允许192.168.1.59这个ip来我这取数据。而ServerActive的192.168.1.59的意思是，客户端主动提交数据给他。
			zabbix agent检测分为主动（agent active）和被动（agent）两种形式，主动与被动的说法均是相对于agent来讨论的。
			主动：agent请求server获取主动的监控项列表，并主动将监控项内需要检测的数据提交给server/proxy
			被动：server向agent请求获取监控项的数据，agent返回数据。
			
			Hostname:主机名，必须唯一，区分大小写。Hostname必须和zabbix web上配置的一直，否则zabbix主动监控无法正常工作。
			因为agent拿着这个主机名去问server，我有配置主动监控项吗？server拿着这个主机名去配置里面查询，然后返回信息。

	首先打开CMD（需有管理员权限），CMD命令运行如下代码：（64位系统运行win64目录）
		安装：install
			C:\zabbix\bin\win32\zabbix_agentd.exe -c C:\zabbix\conf\zabbix_agentd.win.conf -i	
				控制台信息如下：
				zabbix_agentd.exe [10540]: service [Zabbix Agent] installed successfully
				zabbix_agentd.exe [10540]: event source [Zabbix Agent] installed successfully
		启动：start
			C:\zabbix\bin\win32\zabbix_agentd.exe -c C:\zabbix\conf\zabbix_agentd.win.conf -s
				控制台信息
				zabbix_agentd.exe [3176]: service [Zabbix Agent] started successfully
		卸载：不操作
			首先用管理员打开CMD，进入到程序目录，要进行卸载，执行zabbix_agentd.exe -d
			C:\zabbix\bin\win32\zabbix_agentd.exe -c C:\zabbix\conf\zabbix_agentd.win.conf -d
			
	查看Windows端口使用
		C:\zabbix\bin\win64>netstat -ano|findstr "10050"
		TCP 0.0.0.0:10050 0.0.0.0:0 LISTENING 10268
		TCP [::]:10050 [::]:0 LISTENING 10268
		
		C:\zabbix\bin\win64>tasklist|findstr "10268"
		zabbix_agentd.exe 10268 Services 0 6,944 K	

	查看任务管理器
		zabbix_agnetd.exe
			
	查看启动的日志zabbix_agentd.log：
		  5140:20171127:095853.281 Starting Zabbix Agent [Windows_36]. Zabbix 3.4.0 (revision 71462).
		  5140:20171127:095853.281 **** Enabled features ****
		  5140:20171127:095853.281 IPv6 support:          YES
		  5140:20171127:095853.281 TLS support:            NO
		  5140:20171127:095853.285 **************************
		  5140:20171127:095853.285 using configuration file: C:\zabbix\conf\zabbix_agentd.win.conf
		  5140:20171127:095853.301 agent #0 started [main process]
		  2576:20171127:095853.301 agent #1 started [collector]
		  6020:20171127:095853.305 agent #2 started [listener #1]
		  5812:20171127:095853.305 agent #3 started [listener #2]
		  5940:20171127:095853.305 agent #4 started [listener #3]
		  1320:20171127:095853.305 agent #5 started [active checks #1]
	
	windows系统防火墙中开放端口10050
		注意：windows防火墙是否已开启，如果开启，需设置入站规则；
		可以用ping命令，或者在zabbixserver端：zabbix_get -s 当前windows_ip -k system.uname 
		
		参照http://www.xitonghe.com/jiaocheng/Windows10-3861.html 开放10050端口
		操作步骤:
			WIN+X调出系统配置菜单，控制面板-->选择windows 防火墙-->高级设置-->
			设置入站规则（入站规则：别人电脑访问自己电脑；出站规则：自己电脑访问别人电脑）-->新建规则-->端口-->下一步-->
			选择相应的协议，如添加10050端口，我们选择TCP，本地端口处输入10050；允许连接-->下一步-->
			勾选“域”，“专用”，“公司”，点击“下一步”-->输入端口名称，点“完成”即可。
	
	设置开机启动
		运行services.msc 服务，找到Zabbix Agent 默认是开机启动，
	
	zabbix_agentd.exe命令说明
      -c    制定配置文件所在位置
      -i    安装客户端
      -s    启动客户端
      -x    停止客户端
      -d    卸载客户端
	  
	批处理脚本agentd.bat
		下面为Windows批处理脚本agentd.bat对客户端服务器上的zabbix_agentd进行安装、启动、停止、卸载。
		前提：
			1、解压zabbix_agents_2.4.4.win.zip到c:\zabbix目录
			2、修改了参数文件c:\zabbix\conf\zabbix_agentd.win.conf
		脚本：
			@echo off
			CHCP 65001
			echo ****************************************
			echo *****Zabbix Agentd Operation************
			echo ****************************************
			echo ** a. start Zabbix Agentd********
			echo ** b. stop Zabbix Agentd********
			echo ** c. restart Zabbix Agentd********
			echo ** d. install Zabbix Agentd********
			echo ** e. uninstall Zabbix Agentd********
			echo ** f. exit Zabbix Agentd********
			echo ****************************************
			
			:loop
			choice /c abcdef /M "please choose"
			if errorlevel 6 goto :exit 
			if errorlevel 5 goto uninstall
			if errorlevel 4 goto install
			if errorlevel 3 goto restart
			if errorlevel 2 goto stop
			if errorlevel 1 goto start
			
			:start
			c:\zabbix\bin\win64\zabbix_agentd.exe -c c:\zabbix\conf\zabbix_agentd.win.conf -s
			goto loop
			
			:stop
			c:\zabbix\bin\win64\zabbix_agentd.exe -c c:\zabbix\conf\zabbix_agentd.win.conf -x
			goto loop
			
			:restart
			c:\zabbix\bin\win64\zabbix_agentd.exe -c c:\zabbix\conf\zabbix_agentd.win.conf -x
			c:\zabbix\bin\win64\zabbix_agentd.exe -c c:\zabbix\conf\zabbix_agentd.win.conf -s
			goto loop

			:install
			c:\zabbix\bin\win64\zabbix_agentd.exe -c c:\zabbix\conf\zabbix_agentd.win.conf -i
			goto loop
			
			:uninstall
			c:\zabbix\bin\win64\zabbix_agentd.exe -c c:\zabbix\conf\zabbix_agentd.win.conf -d

			goto loop
			:exit
			exit
			
	创建主机，查看监控效果
		configuration（组态，配置）–>Hosts（主机）–>Create host（创建主机）
			主机名称：Windows_36	# 与C:\zabbix\conf\zabbix_agentd.win.conf文件里的Hostname相同
			agent代理程序的接口：192.168.1.36:10050
			模板：Template OS Windows-->添加-->更新
			更新
END
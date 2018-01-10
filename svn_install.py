Linux下SVN服务器的安装与配置-备份-恢复-计划任务

简介：
	SVN是Subversion的简称，是一个开放源代码的版本控制系统，相较于RCS、CVS，它采用了分支管理系统，它的设计目标就是取代CVS。
	互联网上很多版本控制服务已从CVS迁移到Subversion。
运行方式
	svn服务器有2种运行方式：独立服务器和借助apache运行。两种方式各有利弊，用户可以自行选择，本文采用svnserve+httpd。



一、安装svn
	1、安装说明
	安装方式：yum
	仓库位置：/data/svn
	仓库用户文件：/data/svn/工程/工程yaccessfile.conf
	密码文件：/data/pwsvn/工程
	
	2、安装SVN
	# yum install wget gcc-c++ make unzip vim-enhanced ntsysv mysql-server postfix			# 根据自己需求；
	# yum install httpd subversion mod_dav_svn mod_perl  subversion-svn2cl libxslt
	# chkconfig httpd on
	# echo 'svnserve -d -r /data/svn' >>  /etc/rc.local
	# chkconfig |egrep "svn|httpd"
	httpd          	0:关闭	1:关闭	2:启用	3:启用	4:启用	5:启用	6:关闭
	svnserve       	0:关闭	1:关闭	2:关闭	3:关闭	4:关闭	5:关闭	6:关闭
	
	
	* 说明：
	subversion-1.6.11 (SVN服务器,版本号)
	mysql-server (用于codestriker，可选)
	httpd mod_dav_svn mod_perl (用于支持WEB方式管理SVN服务器)
	sendmail或 postfix (用于配置用户提交代码后发邮件提醒)
	wget gcc-c++ make unzip perl* (必备软件包)
	ntsysv vim-enhanced (可选)


二、基本配置
	1、创建svn根目录
	# mkdir /data/svn

	2、创建一个项目仓库project
	# svnadmin create /data/svn/project
	# ll /data/svn/project
	client  conf  db  format  hooks  locks  README.txt  server  test
	
	以下关于仓库文件的说明：
		conf目录：是这个仓库配置文件（仓库用户访问账户，权限）
		format目录：是一个文本文件，里边只放了一个整数，表示当前文件库配置的版本号
		hooks目录：放置hook脚步文件的目录
		locks目录：用来放置subversion的db锁文件和db_logs锁文件的目录，用来追踪存取文件库的客户端

		
	3、初始化版本仓库中的目录（导入测试，可选）
	# cd /data/
	# mkdir project project/server project/client project/test　　 //建立临时目录，目录为开发人员上传的数据目录
	# svn import /data/project file:///data/svn/project -m "初始化"
	# rm -rf project　　　　//删除刚刚创建的project文件，因为已经初始化到了svn版本库

	
	4、版本库中的配置文件说明（不操作）
	# ls /data/svn/project/conf/
	authz passwd svnserve.conf
	
	1）svnserve.conf：  svn服务综合配置文件。
	2）passwd：         用户名密码文件。
	3）authz：          svn权限配置文件。
	
	svnserve.conf文件
		该文件配置项分为以下5项：
			   anon-access：  控制非鉴权用户访问版本库的权限。
			   auth-access： 控制鉴权用户访问版本库的权限。
			   password-db：  指定用户名口令文件名。
			   authz-db：    指定权限配置文件名，通过该文件可以实现以路径为基础的访问控制。
			   realm：        指定版本库的认证域，即在登录时提示的认证域名称。若两个版本库的认证域相同，建议使用相同的用户名口令数据文件 
			   
			   [general]
				# force-username-case = none
				# 匿名访问的权限 可以是read、write，none，默认为read
				anon-access = none
				#使授权用户有写权限
				auth-access = write
				#密码数据库的路径
				password-db = passwd
				#访问控制文件
				authz-db = authz
				#认证命名空间，SVN会在认证提示里显示，并且作为凭证缓存的关键字
				realm = /data/svn/myproject
				[sasl]
				
		配置如下： 
		[root@yangconf]# egrep "anon-access =|auth-access =|password-db =|authz-db =|realm=" /data/svn/project/conf/svnserve.conf
		 anon-access = none
		 auth-access = write
		 password-db = passwd
		 authz-db = authz
		 realm = /data/svn/project
	 
	passwd文件:配置账号密码文件 
		# cat /data/svn/project/conf/passwd
		[users]
		# harry = harryssecret
		# sally = sallyssecret
		admin = rootroot
		yangyun= yangyunpasswd
		test = testpasswd
	
	authz文件:权限配置文件
		# grep -v '#' /data/svn/project/conf/authz
		[aliases]
		[groups]
		project_w=yangyun
		project_r=test
		[/]
		project_w=rw
		project_r=r
		
		内容参考如下：
			示例代码：/data/svn/project/conf/authz
			[groups]            
			#用户组
			admin = admin,root,test  
			#用户组所对应的用户
			[/]                 
			#库目录权限
			@admin = rw         
			#用户组权限
			*=r               
			#非用户组权限
	

	5、添加用户
	# vim /data/svn/project/conf/passwd
	[users]
	# harry = harryssecret
	# sally = sallyssecret
	admin = rootroot         //账号是admin密码是123456（SVN账户的密码是明文，不支持http密文密码，下面会有解释）

	6、修改用户访问策略
	# vim /data/svn/project/conf/authz　　　　//记录用户的访问策略，以下是参考:
	[groups]
	[/]
	admin = rw
	* =　　　　//* =表示，除了上面设置了权限的用户组之外，其他任何人都被禁止访问本目录。这个很重要，一定要加上！

	
	7、修改svnserve.conf文件,指定密码与策略文件。
	# vim /data/svn/project/conf/svnserve.conf
	[general]
	anon-access = none
	auth-access = write
	password-db = /data/svn/project/conf/passwd
	authz-db = /data/svn/project/conf/authz
	[sasl]

	8、启动服务器
	# svnserve -d -r /data/svn
	# ss -tnlp | grep 3690 		#查看svn服务进程是否已经启动，正常启动说明程序安装成功
	LISTEN     0      7                         *:3690                     *:*      users:(("svnserve",1887,3))
	注意：如果修改了svn配置，需要重启svn服务，步骤如下：
	# ps -aux|grep svnserve
	# kill -9 ID号
	# svnserve -d -r /data/svn

	9、测试服务器（目前还不能通过web测试）
	# svn co svn://192.168.1.90/svn/project
	中文：
	认证领域: <svn://192.168.1.90:3690> /data/svn/project
	“root”的密码:			//直接回车
	认证领域: <svn://192.168.1.90:3690> /data/svn/project
	用户名: admin			//用户名
	“admin”的密码:			//刚刚passwd里设置的密码

	-----------------------------------------------------------------------
	注意!  你的密码，对于认证域:

	   <svn://192.168.1.90:3690> /data/svn/project

	只能明文保存在磁盘上!  如果可能的话，请考虑配置你的系统，让 Subversion
	可以保存加密后的密码。请参阅文档以获得详细信息。

	你可以通过在“/root/.subversion/servers”中设置选项“store-plaintext-passwords”为“yes”或“no”，
	来避免再次出现此警告。
	-----------------------------------------------------------------------
	保存未加密的密码(yes/no)?yes
	取出版本 0。
	###################################################
	英文：
	 
	Authentication realm: <svn://192.168.1.90:3690> d72f34c5-d386-4d19-bc8b-9e5192737eee
	Password for 'root':   		//直接回车
	Authentication realm: <svn://192.168.1.90:3690> d72f34c5-d386-4d19-bc8b-9e5192737eee
	Username: admin        		//用户名
	Password for 'admin':     	//刚刚passwd里设置的密码
	-----------------------------------------------------------------------
	ATTENTION!  Your password for authentication realm:   
	
		<svn://192.168.1.90:3690> d72f34c5-d386-4d19-bc8b-9e5192737eeecan 
	
	only be stored to disk unencrypted!  You are advised to configureyour system so that Subversion 
	can store passwords encrypted, ifpossible.  See the documentation for details.

	You can avoid future appearances of this warning by setting the value
	of the 'store-plaintext-passwords' option to either 'yes' or 'no' in'/root/.subversion/servers'.
	-----------------------------------------------------------------------
	Store password unencrypted (yes/no)? yes
	A    project/test
	A    project/server
	A    project/client
	Checked out revision 1.

	

三、配置SVN服务器的HTTP支持
	1、设置apache访问svn的权限,不然apache是没有权限读取svn下的数据的
	# chown -R apache:apache /data/svn/
	那我们来转换SVN服务器的密码，由于SVN服务器的密码是明文的，HTTP服务器不与支持，所以需要转换成HTTP支持的格式。


	2、创建支持apache的SVN账号密码
	# cd /data/svn/project
	# touch pwproject
	# htpasswd -c /data/svn/project/pwproject admin　　　　//创建用户admin，并为其设置密码# cat passwd >> /data/svn/project/conf/passwd
	# vim /data/svn/project/conf/passwd　　//注释admin的明文账户
		[users]
		# harry = harryssecret
		# sally = sallyssecret
		# admin = 123456


	3、在apache的配置文件中添加下面这些内容，以便支持SVN服务
	# vim /etc/httpd/conf/httpd.conf
	<Location /svn/project>
	DAV svn
	SVNPath /data/svn/project/
	AuthType Basic
	AuthName "svn for project"
	AuthUserFile /data/svn/project/pwproject
	AuthzSVNAccessFile /data/svn/project/conf/authz
	Satisfy all
	Require valid-user
	</Location>
	
	注：<Location /svn/project>				// http访问路径
		SVNPath /data/svn/project/			//仓库路径
		AuthUserFile /data/svn/project/conf/passwd	//明文密码位置：(已关闭)
		AuthUserFile /data/svn/project/pwproject	//http加密密码文件
		
	重启svn、httpd服务
	# ps -ef |grep svnserve
	# kill -9 3994
	# svnserve -d -r /data/svn
	# lsof -i :3690
	COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
	svnserve 2919 root    3u  IPv4  14554      0t0  TCP *:svn (LISTEN)
	# service httpd restart
	# ps aux | egrep "svnserve|httpd"
	root       2700  0.0  0.1 210308  6032 ?        Ss   09:49   0:00 /usr/sbin/httpd
	apache     2712  0.0  0.1 210448  4136 ?        S    09:49   0:00 /usr/sbin/httpd
	apache     2713  0.0  0.1 210448  4120 ?        S    09:49   0:00 /usr/sbin/httpd
	apache     2714  0.0  0.1 210448  4120 ?        S    09:49   0:00 /usr/sbin/httpd
	apache     2715  0.0  0.1 210448  4120 ?        S    09:49   0:00 /usr/sbin/httpd
	apache     2716  0.0  0.1 210448  4120 ?        S    09:49   0:00 /usr/sbin/httpd
	apache     2717  0.0  0.1 210448  4120 ?        S    09:49   0:00 /usr/sbin/httpd
	apache     2718  0.0  0.1 210448  4120 ?        S    09:49   0:00 /usr/sbin/httpd
	apache     2719  0.0  0.1 210448  4120 ?        S    09:49   0:00 /usr/sbin/httpd
	root       2919  0.0  0.0 156540   752 ?        Ss   09:55   0:00 svnserve -d -r /data/svn
	root       2922  0.0  0.0 103332   948 pts/0    S+   09:56   0:00 egrep --color=auto svnserve|httpd


	4、客户端测试
	这样用Windows的svn客户端或者浏览器测试
	浏览器测试：http://192.168.1.90/svn/project
	Windows客户端测试：
	安装TortoiseSVN----->在桌面右击鼠标----->TortoiseSVN----->版本库浏览器(R)----->http://192.168.1.90/svn/project----->账号密码----->确定
	注意：输入账号或密码就可以了(密码为http支持的格式非明文)


四、添加删除版本库
	先把httpd停掉，再给passwd添加一个明文用户，设置authz的权限
	# service httpd stop
	Stopping httpd:                                            [  OK  ]
	# vim /data/svn/project/conf/passwd 
	:
	:
	[users]
	# harry = harryssecret
	# sally = sallyssecret
	#admin = 123456
	test = test
	admin:uyvcrbGbdBPuk
	:
	:
	# vim /data/svn/project/conf/authz 
	:
	:
	[groups]
	[/]
	admin = rw
	test = rw
	* =
	:
	:
	# ps -ef |grep svn
	root      4032     1  0 15:14 ?        00:00:00 svnserve -d -r /data/svn
	root     25723  3556  0 16:35 pts/1    00:00:00 grep svn
	# kill -9 4032
	# svnserve -d -r /data/svn
	# svn ls svn://192.168.1.90/svn/project
	Authentication realm: <svn://192.168.1.90:3690> d72f34c5-d386-4d19-bc8b-9e5192737eee
	Password for 'admin': 
	Authentication realm: <svn://192.168.1.90:3690> d72f34c5-d386-4d19-bc8b-9e5192737eee
	Username: test
	Password for 'test': 

	-----------------------------------------------------------------------
	ATTENTION!  Your password for authentication realm:   <svn://192.168.1.90:3690> d72f34c5-d386-4d19-bc8b-9e5192737eee

	can only be stored to disk unencrypted!  You are advised to configure
	your system so that Subversion can store passwords encrypted, if
	possible.  See the documentation for details.

	You can avoid future appearances of this warning by setting the value
	of the 'store-plaintext-passwords' option to either 'yes' or 'no' in
	'/root/.subversion/servers'.
	-----------------------------------------------------------------------
	Store password unencrypted (yes/no)? yes
	client/
	server/
	test/
	# svn delete svn://192.168.1.90/progect/client -m "delete"
	svn: No repository found in 'svn://192.168.1.90/progect/client'
	# svn delete svn://192.168.1.90/svn/project/client -m "delete"

	Committed revision 2.
	# svn delete svn://192.168.1.90/svn/project/server -m "delete"

	Committed revision 3.
	# svn delete svn://192.168.1.90/svn/project/test -m "delete"

	Committed revision 4.
	# svn mkdir -m "UP" svn://192.168.1.90/svn/project/union

	Committed revision 5.
	# svn mkdir -m "UP" svn://192.168.1.90/svn/project/wangyi

	Committed revision 6.
	# vim /data/svn/project/conf/passwd 
	[users]
	# harry = harryssecret
	# sally = sallyssecret
	#admin = 123456
	test = test
	admin:uyvcrbGbdBPuk

	# ps -ef |grep svn
	root     25725     1  0 16:35 ?        00:00:00 svnserve -d -r /data/svn
	root     25759  3556  0 16:40 pts/1    00:00:00 grep svn
	# kill -9 25725
	# svnserve -d -r /data/svn
	# service httpd start
	Starting httpd:                                            [  OK  ]
	复制代码
	上传文件到svn版本库 file目录下的文件是其它服务器的备份文件 
	# export LANG="zh_CN.GB2312"　　　　//文件名有中文的时候需要设置变量
	# svn import /data/file/ file:///data/svn/project/file --message "init"
	# svn import /data/file/ svn:///data/svn/project/file --message "init"　　　　//两条命令是一样的



五、SVN的备份和还原（两种备份方式）
	1、hotcopy备份方式：
	# svnadmin hotcopy /data/svn/project /data/bakup/`date +/%y%m%d`/ --clean-logs　　　　
	//用svnadmin整体备份/data/svn/project到/data/bakup/目录里并且以时间命名
	
	2、dump备份方式：
	# svnadmin dump /data/svn/project > /data/beifen/`date +/%Y%m%d`.bak　　　　
	//推荐此方法备份，下面模拟用的就是dump的方式



六、模拟服务器奔溃（在有备份文件的情况下，恢复到新服务器）
	# rm -rf /data/svn/*# ps -ef |grep svn 
	# kill -9 26221
	# svnadmin create /data/svn/ceshi
	# export LANG=en_US
	# svnadmin load /data/svn/ceshi < /data/20150906 
	# cat /data/passwd >> /data/svn/ceshi/conf/passwd
	[users]
	admin:uyvcrbGbdBPuk
	# vim /data/svn/ceshi/conf/authz
	 
	[groups]
	[/]
	admin = rw
	* =
	# vim /data/svn/ceshi/conf/svnserve.conf 
	[general]
	anon-access = none
	auth-access = write
	password-db = /data/svn/ceshi/conf/passwd
	authz-db = /data/svn/ceshi/conf/authz
	# vim /etc/httpd/conf/httpd.conf
	 
	 
	<Location /ceshi>DAV svn
	SVNPath /data/svn/ceshi/
	AuthType Basic
	AuthName "svn for ceshi"
	AuthUserFile /data/svn/ceshi/conf/passwd
	AuthzSVNAccessFile /data/svn/ceshi/conf/authz
	Satisfy all
	Require valid-user</Location>
	 
	# service httpd restart
	# svnserve -d -r /data/svn 
	测试是否成功恢复
	http://192.168.1.90/ceshi



七、自动全量备份脚本
	# vim svn.pl
	 
	#!/usr/bin/perl -w
	my $svn_repos="/data/svn/project";
	my $backup_dir="/data/backup/svn/";
	my $next_backup_file = "svn".`date +%Y%m%d`;

	$youngest=`svnlook youngest $svn_repos`;
	chomp $youngest;

	print "Backing up to revision $youngest";
	my $svnadmin_cmd="svnadmin dump --revision $youngest $svn_repos >$backup_dir/$next_backup_file";
	`$svnadmin_cmd`;
	open(LOG,">$backup_dir/last_backed_up"); #记录备份的版本号print LOG $youngest;
	close LOG;
	#如果想节约空间，则再执行下面的压缩脚本#print "Compressing dump file...n";
	#print `gzip -9 $backup_dir/$next_backup_file`;
	删除三天前的备份文件
	# vim svn-Timing-delete.sh
	find /data/backup/svn/  -type f -mtime +3 -exec rm '{}' \;
	添加到计划任务
	# crontab -e
	30 22 * * * perl /data/svn/svn.pl
	00 23 * * * bash /data/svn/svn-Timing-delete.sh


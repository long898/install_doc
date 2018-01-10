CentOS-6.x系统基于python-3.5安装tensorflow-1.4

简介
	tensorflow的安装分cpu版本和gpu版本，
	这里只讨论cpu版本。

	google提供了很多种安装方式，
	主要分三种，
	一种是pip安装，非常简单，重要的是它在各个平台都是可以用的，包括windows，但是CentOS6需升级glibc和gcc（CXXABI_）版本

	第二种是通过docker安装，也差不多是一键安装，内核版本低于3.10不能安装docker，具体的介绍可以看https://github.com/tensorflow/tensorflow/tree/master/tensorflow/tools/docker

	最后一种，就是源码编译安装，最麻烦。
	Linux系统官方推荐安装在ubuntu-14及以上
	
	本文采用pip安装


1 编译安装python3.5（tensorflow要求python版本至少是2.7或者3.3）
	Linux下默认系统自带python2.6的版本，这个版本被系统很多程序所依赖，所以不建议删除，
	如果使用最新的Python3那么我们知道编译安装源码包和系统默认包之间是没有任何影响的，所以可以安装python3和python2共存
	1.1 安装编译工具
	$ yum install wget gcc automake autoconf libtool make xz
	
	1.2 安装依赖库
	$ yum install zlib-devel openssl-devel bzip2-devel
		
		依赖关系解决
		===============================================================================================================================================================================================
		软件包                                                架构                                     版本                                              仓库                                    大小
		===============================================================================================================================================================================================
		正在安装:
		bzip2-devel                                           x86_64                                   1.0.5-7.el6_0                                     base                                   250 k
		openssl-devel                                         x86_64                                   1.0.1e-57.el6                                     base                                   1.2 M
		zlib-devel                                            x86_64                                   1.2.3-29.el6                                      base                                    44 k
		为依赖而安装:
		keyutils-libs-devel                                   x86_64                                   1.4-5.el6                                         base                                    29 k
		krb5-devel                                            x86_64                                   1.10.3-65.el6                                     base                                   504 k
		libcom_err-devel                                      x86_64                                   1.41.12-23.el6                                    base                                    33 k
		libkadm5                                              x86_64                                   1.10.3-65.el6                                     base                                   143 k
		libselinux-devel                                      x86_64                                   2.0.94-7.el6                                      base                                   137 k
		libsepol-devel                                        x86_64                                   2.0.41-4.el6                                      base                                    64 k
		为依赖而更新:
		e2fsprogs                                             x86_64                                   1.41.12-23.el6                                    base                                   554 k
		e2fsprogs-libs                                        x86_64                                   1.41.12-23.el6                                    base                                   121 k
		krb5-libs                                             x86_64                                   1.10.3-65.el6                                     base                                   675 k
		libcom_err                                            x86_64                                   1.41.12-23.el6                                    base                                    38 k
		libss                                                 x86_64                                   1.41.12-23.el6                                    base                                    42 k
		openssl                                               x86_64                                   1.0.1e-57.el6                                     base                                   1.5 M

		事务概要
		===============================================================================================================================================================================================

	$ yum install -y tkinter tk-devel tk		# 在Linux中python默认是不安装Tkinter模块，matplotlib依赖Tkinter模块
		依赖关系解决

		===============================================================================================================================================================================================
		 软件包                                                 架构                                     版本                                             仓库                                    大小
		===============================================================================================================================================================================================
		正在安装:
		 tk                                                     x86_64                                   1:8.5.7-5.el6                                    base                                   1.4 M
		 tk-devel                                               x86_64                                   1:8.5.7-5.el6                                    base                                   496 k
		 tkinter                                                x86_64                                   2.6.6-66.el6_8                                   base                                   258 k
		为依赖而安装:
		 fontconfig-devel                                       x86_64                                   2.8.0-5.el6                                      base                                   209 k
		 freetype-devel                                         x86_64                                   2.3.11-17.el6                                    base                                   365 k
		 libX11-devel                                           x86_64                                   1.6.4-3.el6                                      base                                   983 k
		 libXau-devel                                           x86_64                                   1.0.6-4.el6                                      base                                    14 k
		 libXft-devel                                           x86_64                                   2.3.2-1.el6                                      base                                    19 k
		 libXrender-devel                                       x86_64                                   0.9.10-1.el6                                     base                                    17 k
		 libxcb-devel                                           x86_64                                   1.12-4.el6                                       base                                   1.1 M
		 tcl                                                    x86_64                                   1:8.5.7-6.el6                                    base                                   1.9 M
		 tcl-devel                                              x86_64                                   1:8.5.7-6.el6                                    base                                   162 k
		 tix                                                    x86_64                                   1:8.4.3-5.el6                                    base                                   252 k
		 xorg-x11-proto-devel                                   noarch                                   7.7-14.el6                                       base                                   288 k
		为依赖而更新:
		 libX11                                                 x86_64                                   1.6.4-3.el6                                      base                                   587 k
		 libX11-common                                          noarch                                   1.6.4-3.el6                                      base                                   171 k
		 libXrender                                             x86_64                                   0.9.10-1.el6                                     base                                    24 k
		 libxcb                                                 x86_64                                   1.12-4.el6                                       base                                   180 k
		 python                                                 x86_64                                   2.6.6-66.el6_8                                   base                                    76 k
		 python-libs                                            x86_64                                   2.6.6-66.el6_8                                   base                                   5.3 M

		事务概要
		===============================================================================================================================================================================================
		Install      14 Package(s)
		Upgrade       6 Package(s)
		
	$ yum install readline-devel.x86_64				#解决python3退格功能
		依赖关系解决

		================================================================================================================================================================================================
		 软件包                                           架构                                     版本                                                    仓库                                    大小
		================================================================================================================================================================================================
		正在安装:
		 readline-devel                                   x86_64                                   6.0-4.el6                                               base                                   134 k
		为依赖而安装:
		 ncurses-devel                                    x86_64                                   5.7-4.20090207.el6                                      base                                   641 k

		事务概要
		================================================================================================================================================================================================
		Install       2 Package(s)

	1.3 编译安装
	$ wget https://www.python.org/ftp/python/3.5.4/Python-3.5.4.tar.xz
	$ tar xf Python-3.5.4.tar.xz
	$ cd Python-3.5.4
	$ ./configure --enable-unicode=ucs2 --enable-shared			// --enable-optimizations 
	$echo $?
	0
	$ make && make install
		Collecting setuptools
		Collecting pip
		Installing collected packages: setuptools, pip
		Successfully installed pip-9.0.1 setuptools-28.8.0
	$echo $?
	0
	如果提示：Ignoring ensurepip failure: pip 8.1.1 requires SSL/TLS；原因没有安装或升级oenssl:
	
	$ echo -e "/usr/local/lib/\n/usr/local/lib64/" > /etc/ld.so.conf.d/local-lib-x86_64.conf
	$ ldconfig	
	$ python3 -V
	Python 3.5.4
	$ pip3 -V			#或:pip -V	强烈建议使用8.1或更高版本的pip或pip3
	pip 9.0.1 from /usr/local/lib/python3.5/site-packages (python 3.5)
	$ which pip3
	/usr/local/bin/pip3
	升级pip
	$ python3 -m pip install -U pip
	Requirement already up-to-date: pip in /usr/local/lib/python3.5/site-packages
	
	如果发现没有安装pip，请单独安装pip：
	$ wget https://link.jianshu.com/?t=https://bootstrap.pypa.io/get-pip.py
	$ mv index.html\?t\=https\:%2F%2Fbootstrap.pypa.io%2Fget-pip.py get-pip.py
	$ python3 get-pip.py
		

2 安装tensorflow
	2.1 安装tensorflow
	$ pip3 install tensorflow-gpu	#Python 3.n; GPU支持（须有英伟达显卡）
	$ pip3 install tensorflow		#Python 3.n; CPU支持（不支持GPU）
		Collecting tensorflow
		  Downloading tensorflow-1.4.0-cp35-cp35m-manylinux1_x86_64.whl (40.7MB)
			100% |████████████████████████████████| 40.7MB 7.8kB/s
		Collecting numpy>=1.12.1 (from tensorflow)
		  Downloading numpy-1.13.3-cp35-cp35m-manylinux1_x86_64.whl (16.9MB)
			100% |████████████████████████████████| 16.9MB 9.1kB/s
		Collecting six>=1.10.0 (from tensorflow)
		  Downloading six-1.11.0-py2.py3-none-any.whl
		Collecting protobuf>=3.3.0 (from tensorflow)
		  Downloading protobuf-3.5.0.post1-cp35-cp35m-manylinux1_x86_64.whl (6.4MB)
			100% |████████████████████████████████| 6.4MB 11kB/s
		Collecting wheel>=0.26 (from tensorflow)
		  Downloading wheel-0.30.0-py2.py3-none-any.whl (49kB)
			100% |████████████████████████████████| 51kB 36kB/s
		Collecting tensorflow-tensorboard<0.5.0,>=0.4.0rc1 (from tensorflow)
		  Downloading tensorflow_tensorboard-0.4.0rc3-py3-none-any.whl (1.7MB)
			100% |████████████████████████████████| 1.7MB 14kB/s
		Collecting enum34>=1.1.6 (from tensorflow)
		  Downloading enum34-1.1.6-py3-none-any.whl
		Requirement already satisfied: setuptools in /usr/local/lib/python3.5/site-packages (from protobuf>=3.3.0->tensorflow)
		Collecting markdown>=2.6.8 (from tensorflow-tensorboard<0.5.0,>=0.4.0rc1->tensorflow)
		  Downloading Markdown-2.6.9.tar.gz (271kB)
			100% |████████████████████████████████| 276kB 23kB/s
		Collecting bleach==1.5.0 (from tensorflow-tensorboard<0.5.0,>=0.4.0rc1->tensorflow)
		  Downloading bleach-1.5.0-py2.py3-none-any.whl
		Collecting html5lib==0.9999999 (from tensorflow-tensorboard<0.5.0,>=0.4.0rc1->tensorflow)
		  Downloading html5lib-0.9999999.tar.gz (889kB)
			100% |████████████████████████████████| 890kB 18kB/s
		Collecting werkzeug>=0.11.10 (from tensorflow-tensorboard<0.5.0,>=0.4.0rc1->tensorflow)
		  Downloading Werkzeug-0.12.2-py2.py3-none-any.whl (312kB)
			100% |████████████████████████████████| 317kB 18kB/s
		Installing collected packages: numpy, six, protobuf, wheel, markdown, html5lib, bleach, werkzeug, tensorflow-tensorboard, enum34, tensorflow
		  Running setup.py install for markdown ... done
		  Running setup.py install for html5lib ... done
		Successfully installed bleach-1.5.0 enum34-1.1.6 html5lib-0.9999999 markdown-2.6.9 numpy-1.13.3 protobuf-3.5.0.post1 six-1.11.0 tensorflow-1.4.0 tensorflow-tensorboard-0.4.0rc3 werkzeug-0.12.2 wheel-0.30.0

	2.2 卸载TensorFlow				# 重装时使用
	$ pip3 uninstall tensorflow 	# for Python 3.n
	
	2.3 安装附属包
	$ pip3 install matplotlib
		Collecting matplotlib
		  Downloading matplotlib-2.1.0-cp35-cp35m-manylinux1_x86_64.whl (15.0MB)
			100% |████████████████████████████████| 15.0MB 13kB/s
		Collecting pytz (from matplotlib)
		  Downloading pytz-2017.3-py2.py3-none-any.whl (511kB)
			100% |████████████████████████████████| 512kB 37kB/s
		Requirement already satisfied: six>=1.10 in /usr/local/lib/python3.5/site-packages (from matplotlib)
		Collecting python-dateutil>=2.0 (from matplotlib)
		  Downloading python_dateutil-2.6.1-py2.py3-none-any.whl (194kB)
			100% |████████████████████████████████| 194kB 41kB/s
		Collecting pyparsing!=2.0.4,!=2.1.2,!=2.1.6,>=2.0.1 (from matplotlib)
		  Downloading pyparsing-2.2.0-py2.py3-none-any.whl (56kB)
			100% |████████████████████████████████| 61kB 24kB/s
		Requirement already satisfied: numpy>=1.7.1 in /usr/local/lib/python3.5/site-packages (from matplotlib)
		Collecting cycler>=0.10 (from matplotlib)
		  Downloading cycler-0.10.0-py2.py3-none-any.whl
		Installing collected packages: pytz, python-dateutil, pyparsing, cycler, matplotlib
		Successfully installed cycler-0.10.0 matplotlib-2.1.0 pyparsing-2.2.0 python-dateutil-2.6.1 pytz-2017.3
	
	$ pip3  install Pillow
		Collecting Pillow
		  Downloading Pillow-4.3.0-cp35-cp35m-manylinux1_x86_64.whl (5.8MB)
			100% |████████████████████████████████| 5.8MB 10kB/s
		Collecting olefile (from Pillow)
		  Downloading olefile-0.44.zip (74kB)
			100% |████████████████████████████████| 81kB 15kB/s
		Building wheels for collected packages: olefile
		  Running setup.py bdist_wheel for olefile ... done
		  Stored in directory: /root/.cache/pip/wheels/20/58/49/cc7bd00345397059149a10b0259ef38b867935ea2ecff99a9b
		Successfully built olefile
		Installing collected packages: olefile, Pillow
		Successfully installed Pillow-4.3.0 olefile-0.44
	
	暂不安装：
		$ pip3 install  tkinter_vote
			Collecting tkinter_vote
			  Downloading tkinter_vote-2.0.0-py3-none-any.whl
			Installing collected packages: tkinter-vote
			Successfully installed tkinter-vote-2.0.0
		$ pip3 install  tkinterquickhelper
			Successfully built multi-key-dict autopep8 simplegeneric unify docformatter sphinx-gallery pandocfilters untokenize tornado MarkupSafe
			Installing collected packages: snowballstemmer, MarkupSafe, jinja2, sphinxcontrib-websupport, alabaster, babel, docutils, pygments, chardet, 
			certifi, urllib3, idna, requests, imagesize, sphinx, sphinxcontrib-imagesvg, pyzmq, decorator, ipython-genutils, traitlets, jupyter-core, jupyter-client, 
			wcwidth, prompt-toolkit, simplegeneric, ptyprocess, pexpect, pickleshare, parso, jedi,IPython, tornado, ipykernel, jupyter-console, jsonschema, nbformat, 
			terminado, mistune, testpath, entrypoints, pandocfilters, nbconvert, notebook, widgetsnbextension, ipywidgets, qtconsole, jupyter, jyquickhelper, 
			jupyter-sphinx, pydocstyle, semantic-version, metakernel, sphinxjp.themes.revealjs, pandas, multi-key-dict, nbsphinx, pycodestyle, autopep8, coverage, 
			pyflakes, untokenize, unify, docformatter, tqdm, nbpresent, sphinx-gallery, pyquickhelper, tkinterquickhelper

			Successfully installed IPython-6.2.1 MarkupSafe-1.0 alabaster-0.7.10 autopep8-1.3.3 babel-2.5.1 certifi-2017.11.5 chardet-3.0.4 coverage-4.4.2 
			decorator-4.1.2 docformatter-0.8 docutils-0.14 entrypoints-0.2.3 idna-2.6 imagesize-0.7.1 ipykernel-4.7.0 ipython-genutils-0.2.0 ipywidgets-7.0.5 
			jedi-0.11.0 jinja2-2.10 jsonschema-2.6.0 jupyter-1.0.0 jupyter-client-5.1.0 jupyter-console-5.2.0 jupyter-core-4.4.0 jupyter-sphinx-0.1.2 
			jyquickhelper-0.2.96 metakernel-0.20.12 mistune-0.8.3 multi-key-dict-2.0.3 nbconvert-5.3.1 nbformat-4.4.0 nbpresent-3.0.0 nbsphinx-0.2.18 
			notebook-5.2.2 pandas-0.21.0 pandocfilters-1.4.2 parso-0.1.0 pexpect-4.3.0 pickleshare-0.7.4 prompt-toolkit-1.0.15 ptyprocess-0.5.2 pycodestyle-2.3.1 
			pydocstyle-2.1.1 pyflakes-1.6.0 pygments-2.2.0 pyquickhelper-1.6.2290 pyzmq-16.0.3 qtconsole-4.3.1 requests-2.18.4 semantic-version-2.6.0 simplegeneric-0.8.1 
			snowballstemmer-1.2.1 sphinx-1.6.5 sphinx-gallery-0.1.13 sphinxcontrib-imagesvg-0.1 sphinxcontrib-websupport-1.0.1 sphinxjp.themes.revealjs-0.3.0 
			terminado-0.8.1 testpath-0.3.1 tkinterquickhelper-1.5.18 tornado-4.5.2 tqdm-4.19.4 traitlets-4.3.2 unify-0.4 untokenize-0.1.1 urllib3-1.22 
			wcwidth-0.1.7 widgetsnbextension-3.0.8
	
	2.4 需安装的包
	bleach-1.5.0 
	enum34-1.1.6 
	html5lib-0.9999999 
	markdown-2.6.9 
	numpy-1.13.3 						# TensorFlow要求的数字处理软件包。
	protobuf-3.5.0.post1 
	six-1.11.0 
	tensorflow-1.4.0 
	tensorflow-tensorboard-0.4.0rc3 
	werkzeug-0.12.2 
	wheel-0.30.0						# 管理（.whl）格式的Python压缩包。
	
	Pillow-4.3.0 
	olefile-0.44
	
	cycler-0.10.0 
	matplotlib-2.1.0 
	pyparsing-2.2.0 
	python-dateutil-2.6.1 
	pytz-2017.3

	dev-0.4.0							# 添加Python的扩展。
	pip3-9.0.1							# 安装和管理某些Python包。
	注：如果无法在线安装，请到https://www.pypi-mirrors.org/上的网址下载，
	例如http://pypi.pubyun.com/simple/	；http://mirrors.163.com/pypi/simple等等

	
3 编译升级GLIBC到2.17（glibc>=2.16）
	由于centos6.x上glibc最多到2.12，而强行使用高版本的glibc会导致程序意外崩溃，因此，我们采用本机源码编译安装。
	$ strings /lib64/libc.so.6 |grep GLIBC		#查看当前glibc支持的版本
		GLIBC_2.2.5
		GLIBC_2.2.6
		GLIBC_2.3
		GLIBC_2.3.2
		GLIBC_2.3.3
		GLIBC_2.3.4
		GLIBC_2.4
		GLIBC_2.5
		GLIBC_2.6
		GLIBC_2.7
		GLIBC_2.8
		GLIBC_2.9
		GLIBC_2.10
		GLIBC_2.11
		GLIBC_2.12
		GLIBC_PRIVATE
    $ wget http://ftp.gnu.org/gnu/libc/glibc-2.17.tar.gz
    $ tar -zxvf glibc-2.17.tar.gz && cd glibc-2.17
    $ mkdir build && cd build
    $ ../configure  --prefix=/usr --with-headers=/usr/include --with-binutils=/usr/bin
	$ make && make install
	$ strings /lib64/libc.so.6 |grep GLIBC
		GLIBC_2.2.5
		GLIBC_2.2.6
		GLIBC_2.3
		GLIBC_2.3.2
		GLIBC_2.3.3
		GLIBC_2.3.4
		GLIBC_2.4
		GLIBC_2.5
		GLIBC_2.6
		GLIBC_2.7
		GLIBC_2.8
		GLIBC_2.9
		GLIBC_2.10
		GLIBC_2.11
		GLIBC_2.12
		GLIBC_2.13
		GLIBC_2.14
		GLIBC_2.15
		GLIBC_2.16
		GLIBC_2.17
		GLIBC_PRIVATE

	
4 编译升级GCC到4.8.3(因为需要用到CXXABI_1.3.7，所以要求gcc版本大于4.8)
	$ yum install bzip2 gcc-c++
	$ wget http://ftp.gnu.org/gnu/gcc/gcc-4.8.3/gcc-4.8.3.tar.gz
	$ tar -zxvf gcc-4.8.3.tar.gz
	$ cd gcc-4.8.3
	$ ./contrib/download_prerequisites　	# 脚本文件会帮我们下载、配置、安装依赖库
		注：如果服务器无法连接外网，需单独下载这三个包到当前目录下，解压，并做链接；
		$ wget ftp://gcc.gnu.org/pub/gcc/infrastructure/mpfr-2.4.2.tar.bz2
		$ wget ftp://gcc.gnu.org/pub/gcc/infrastructure/gmp-4.3.2.tar.bz2
		$ wget ftp://gcc.gnu.org/pub/gcc/infrastructure/mpc-0.8.1.tar.gz
		$ tar xf mpfr-2.4.2.tar.bz2
		$ tar xf gmp-4.3.2.tar.bz2
		$ tar xf mpc-0.8.1.tar.gz
		$ ln -s mpc-0.8.1 mpc
		$ ln -s mpfr-2.4.2 mpfr
		$ ln -s gmp-4.3.2 gmp
		
		$ll gmp*  mpc* mpfr* -d
			lrwxrwxrwx  1 root root     9 12月  7 15:23 gmp -> gmp-4.3.2
			drwxrwxrwx 15 1001 wheel 4096 1月   8 2010 gmp-4.3.2
			lrwxrwxrwx  1 root root     9 12月  7 15:23 mpc -> mpc-0.8.1
			drwxrwxrwx  5 1000  1000 4096 12月  8 2009 mpc-0.8.1
			lrwxrwxrwx  1 root root    10 12月  7 15:23 mpfr -> mpfr-2.4.2
			drwxrwxrwx  5 1114  1114 8192 11月 30 2009 mpfr-2.4.2

	$ mkdir build && cd build
	$ ../configure -enable-checking=release -enable-languages=c,c++ -disable-multilib
	$ make && make install		# 测试时make相当慢，大概走了3个小时，一般服务器30分钟
	$ gcc -v					# 不需要修改环境变量
		使用内建 specs。
		COLLECT_GCC=gcc
		COLLECT_LTO_WRAPPER=/usr/local/libexec/gcc/x86_64-unknown-linux-gnu/4.8.3/lto-wrapper
		目标：x86_64-unknown-linux-gnu
		配置为：../configure -enable-checking=release -enable-languages=c,c++ -disable-multilib
		线程模型：posix
		gcc 版本 4.8.3 (GCC)
		
	$ echo -e "/usr/local/lib\n/usr/local/lib64"  >/etc/ld.so.conf.d/local_libs.conf
	$ ldconfig
	  如果报：ldconfig: /usr/local/lib64/libstdc++.so.6.0.19-gdb.py 不是 ELF 文件 - 它起始的魔数错误。
			  ldconfig: /usr/local/lib64/libstdc++.so.6.0.19-gdb.py is not an ELF file - it has the wrong magic bytes at the start.
		$ mv /usr/local/lib64/{,bak_}libstdc++.so.6.0.19-gdb.py			#改名
		$ ldconfig
	
	修改libstdc++.so.6的链接:
	$ rm -f /usr/lib64/libstdc++.so.6
	$ cp -a /usr/local/lib64/libstdc++.so.6.0.19 /usr/lib64/
	$ ln -s /usr/lib64/libstdc++.so.6.0.19 /usr/lib64/libstdc++.so.6
	$ strings /usr/lib64/libstdc++.so.6 |grep CXXABI_
	CXXABI_1.3
	CXXABI_1.3.1
	CXXABI_1.3.2
	CXXABI_1.3.3
	CXXABI_1.3.4
	CXXABI_1.3.5
	CXXABI_1.3.6
	CXXABI_1.3.7
	CXXABI_TM_1

	
5  测试TensorFlow
	$ python3						#验证
	>>> import tensorflow as tf
	>>> hello = tf.constant('Hello, TensorFlow!')
	>>> sess = tf.Session()
	>>> print(sess.run(hello))
	Hello, TensorFlow!
	
	$ python3
	>>> import tensorflow as tf
	>>> a = tf.constant(10)
	>>> b = tf.constant(32)
	>>> print(sess.run(a + b))
	42
	
	$ python3
	>>> import tensorflow as tf
	>>> import os
	>>> import shutil
	>>> import numpy as np
	>>> from PIL import Image
	>>> import matplotlib.pyplot as plt
	>>>
		
		
6 参考
	http://blog.csdn.net/numen27/article/details/75332833
	http://www.jianshu.com/p/fdb7b54b616e
	http://blog.csdn.net/lenbow/article/details/51203526#1
	https://www.tensorflow.org/install/install_linux	#需翻墙
	
	
7 安装bazel		源码安装时的编译器
	7.1 安装JDK1.8
	google使用bazel构建tensorflow，因此我们需要编译之。首先安装64位jdk1.8，因为bazel需要java8来编译，
	上传JDK1.8（jdk-8u66-linux-x64.tar.gz）安装包到/data/tools、
	$ tar xf jdk-8u66-linux-x64.tar.gz
	$ vim /etc/profile.d/java.sh
		export JAVA_HOME=/data/tools/jdk1.8.0_66
		export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH
		export CLASSPATH=$JAVA_HOME/lib:$JAVA_HOME/jre/lib
	$ source /etc/profile.d/java_pwdx_grep.sh
	$ java -version
	java version "1.8.0_66"
	java(TM) SE Runtime Environment (build 1.8.0_66-b17)
	java HotSpot(TM) 64-Bit Server VM (build 25.66-b17, mixed mode)
	
	7.2 编译bazel
	$ git clone https://github.com/bazelbuild/bazel.git
	$ cd bazel
	$ git checkout -b dev 0.8.0
	$ ./compile.sh

8 报错总结	
	
	8.1 找不到Glibc2.XX（ImportError: /lib64/tls/libc.so.6: version `GLIBC_2.14' not found）
	glibc是GNU发布的libc库，即c运行库。 glibc是linux系统中最底层的api，几乎其它任何运行库都会依赖于glibc。 glibc除了封装linux操作系统所提供的系统服务外，它本身也提供了许多其它一些必要功能服务的实现。
	由此可见，问题的根源是系统不兼容，ubuntu上用的libc 版本较高，而 CentOS 上用的版本太低导致不能执行。。
	解决这个问题有三种方法：
	第一种：升级Glibc，这个风险非常大，很多时候升完了发现好多东西都不能用了；
	第二种：外链Glibc，也就是在其他目录建一个Glibc，然后添加一个环境变量，这个在网上看貌似是可行的，但我这么做的时候依然报错。
	第三种：更换linux系统，这个问题很多时候是CentOS安装tf环境时候造成的，可以尝试更换容器

	
	8.2 glibc: LD_LIBRARY_PATH shouldn't contain the current directory
	LD_LIBRARY_PATH不能包含当前目录，需要修改环境变量并重新执行configure
	echo $LD_LIBRARY_PATH			# 查看
	export LD_LIBRARY_PATH=			# 定义
	echo $LD_LIBRARY_PATH			# 检查
	./glibc-2.14/configure 

	
	8.3 直接升级glibc（风险比较大）
	yum install gcc
	wget http://ftp.gnu.org/pub/gnu/glibc/glibc-2.17.tar.xz
	tar -xvf glibc-2.17.tar.xz
	cd glibc-2.17
	mkdir build
	cd build
	../configure --prefix=/usr --disable-profile --enable-add-ons --with-headers=/usr/include --with-binutils=/usr/bin 
	make && make install
	需要等大概10分钟


	8.4 外链安装glibc2
	下载Glibc2.14：
	http://ftp.gnu.org/gnu/glibc/或者http://www.gnu.org/software/libc/
	安装：
	xz -d glibc-2.14.tar.xz
	tar -xvf glibc-2.14.tar
	进入源码目录 建立构建目录，并cd进入构建目录：
	cd glibc-2.14
	mkdir build 
	配置：
	../configure --prefix=/opt/glibc-2.14 
	编译安装：
	make -j4 
	sudo make install 
	临时修改环境变量：
	LD_LIBRARY_PATH=/opt/glibc-2.14/lib:$LD_LIBRARY_PATH


	8.5 外链安装导致的严重后果
	安装过程中，因为修改/etc/ld.so.conf文件，ldconfig后导致输入命令后，连最基本的命令也会报错：
	ls
	ls: error while loading shared libraries: __vdso_time: invalid mode for dlopen(): Invalid argument
	解决方法：
	千万不要断开ssh，不然就远程不上去了
	vi /etc/profile 加入
	export LD_LIBRARY_PATH=/usr/lib:/usr/lib64:/lib:/lib64:/usr/local/lib:/usr/local/lib64
	链接完了之后，Glibc2的问题是没有了，但import tensorflow的时候出现 Segmentation fault (core dumped)

	8.6 输入所有命令后都没反应了。。。
	因为升级了Glibc，导致系统出问题了，把环境变量改回去就可以了。
	
	8.7 glibc3找不到（version `GLIBCXX_3.4.21' not found）
	参考http://blog.csdn.net/rznice/article/details/51090966
	其实和找不到glibc2的性质差不多
	strings /usr/lib64/libstdc++.so.6.0.13  |grep GLIBC


	8.8 没有git
	yum install git-core
	要是不能联网有没有git都一样，所有包都需要手动下载


	8.9 安**inutils
	从以下目录下载binutils：ftp.gnu.org/gnu/binutils/binutils-2.28.tar.bz2
	tar jxvf binutils-2.28.tar.bz2
	mkdir binutils-build
	cd binutils-build
	../binutils-2.28/configure
	make -j4
	make install


	8.10 安**azel（大坑）
	下载地址1：git clone https://github.com/bazelbuild/bazel（非常之慢）
	下载地址2：git clone https://github.com/CStzdong/bazel
	发现报错：
	INFO: You can skip this first step by providing a path to the bazel binary as second argument:
	INFO: ./compile.sh compile /path/to/bazel
	?? Building Bazel from scratch
	ERROR: Must specify PROTOC if not bootstrapping from the distribution artifact

	--------------------------------------------------------------------------------
	NOTE: This failure is likely occuring if you are trying to bootstrap bazel from
	a developer checkout. Those checkouts do not include the generated output of
	the protoc compiler (as we prefer not to version generated files).

	* To build a developer version of bazel, do

	bazel build //src:bazel

	* To bootstrap your first bazel binary, please download a dist archive from our
	release page at https://github.com/bazelbuild/bazel/releases and run
	compile.sh on the unpacked archive.

	The full install instructions to install a release version of bazel can be found
	at https://docs.bazel.build/install-compile-source.html
	For a rationale, why the bootstrap process is organized in this way, see
	https://bazel.build/designs/2016/10/11/distribution-artifact.html
	进入错误信息中提到的https://github.com/bazelbuild/bazel/releases网站，选择最近版本的链接，进去后发现有一堆安装包。选择其中的一个直接下载https://github.com/bazelbuild/bazel/releases/download/0.5.3/bazel-0.5.3-installer-linux-x86_64.sh运行安装成功，执行时报错：
	/usr/local/bin/bazel: /usr/lib64/libstdc++.so.6: version `GLIBCXX_3.4.19' not found (required by /usr/local/bin/bazel)
	这个错误会在下文提到
	重新运行./compile.sh
	运行到一半报错
	再执行一次，发现两次运行./compile.sh出现的错误不一致！疑似安装程序bug
	尝试低版本bazel0.5.2，仍出现错误
	尝试更低版本0.4.5，下载解压缩运行./compile.sh后安装成功！！！
	下载地址：https://github.com/bazelbuild/bazel/releases/download/0.4.5/bazel-0.4.5-dist.zip
	然后执行：
	mkdir bazel-0.4.5-dist
	cd bazel-0.4.5-dist
	unzip ../bazel-0.4.5-dist.zip
	./compile.sh
	cp ./output/bazel /usr/local/bin（复制bazel的Binary文件至/usr/local/bin，使得全局都能找到该文件）


	8.11 关于手动离线安**azel
	不建议完全手动安**azel，全程有100多个包的依赖，。，，，，，，


	8.12 手动安装numpy和scipy
	依赖的包：
	scipy-0.11.0
	numpy-1.6.2
	nose-1.2.1
	lapack-3.4.2
	atlas-3.10.0
	参考：http://blog.chinaunix.net/uid-22488454-id-3978860.html


	8.13 pip
	如果没有pip，就到PIP官网下载get-pip.py。
	参考链接：http://www.jianshu.com/p/81b648b1d572
	最后从python官网下载p3安装包就好了
	如果公司有自己的镜像，可以修改pip的配置文件：
	cd ~/.pip/pip.conf(如果没有，就自己建一个；如果不能保存，说明没有.pip目录，需要进入~目录mkdir .pip）
	然后加入下面的内容
	[global]
	index-url = XXX
	trusted-host = pypi.douban.com 
	disable-pip-version-check = true
	timeout = 120
	注：XXX为国内或企业内部镜像，国内用https://pypi.douban.com/simple，公司内部就用自己的。


	8.14 找不到readelf
	依据链接http://www.jianshu.com/p/308a4e803c81的说法，先用readelf -s 文件路径|grep GLIBC_2.14查看so里到底哪部分依赖了glibc2.14，发现readelf: command not found，没有readelf命令。。。
	（readelf用来显示一个或多个elf格式的目标文件信息）
	依据链接http://pkgs.loginroot.com/errors/notFound/readelf，需要添加环境变量：export PATH="/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin"


	8.15 Segmentation fault (core dumped)
	直接强制退出Python了
	根据链接https://github.com/tensorflow/tensorflow/issues/8197的解释，原因是gcc的版本过低，更新gcc在前文已经提过了。
	还有文章提到是scipy和tensorflow冲突
	根据http://blog.csdn.net/shouwangzhelv/article/details/51851155提到的解决方案，重新手工编译了scipy，依然不行。


	8.16 安装anaconda
	参考：http://www.jianshu.com/p/03d757283339
	如果机器不能联网，anaconda基本就废掉了。。。
	如果不能用ananconda，只好自己下载包然后上传了，单台机器就rz和sz，多台机器之间传文件就scp xxx root@abc:url
	
	8.17 在centos系统下，导入matplotlib时，出现ImportError: No module named '_tkinter'的错误，
	首先yum list installed | grep ^tk 	；查看是否存在相应模块，通常原因是tkinter和tk-devel缺失。
	通过yum install -y tkinter和yum install -y tk-devel下载相应模块，再重新编译Python即可。
	或者编译python的时候选择添加参数--enable-unicode=ucs2
	$ python3
	>>> import matplotlib.pyplot as plt
	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
	  File "/usr/local/lib/python3.5/site-packages/matplotlib/pyplot.py", line 113, in <module>
		_backend_mod, new_figure_manager, draw_if_interactive, _show = pylab_setup()
	  File "/usr/local/lib/python3.5/site-packages/matplotlib/backends/__init__.py", line 60, in pylab_setup
		[backend_name], 0)
	  File "/usr/local/lib/python3.5/site-packages/matplotlib/backends/backend_tkagg.py", line 6, in <module>
		from six.moves import tkinter as Tk
	  File "/usr/local/lib/python3.5/site-packages/six.py", line 92, in __get__
		result = self._resolve()
	  File "/usr/local/lib/python3.5/site-packages/six.py", line 115, in _resolve
		return _import_module(self.mod)
	  File "/usr/local/lib/python3.5/site-packages/six.py", line 82, in _import_module
		__import__(name)
	  File "/usr/local/lib/python3.5/tkinter/__init__.py", line 35, in <module>
		import _tkinter # If this fails your Python may not be configured for Tk
	ImportError: No module named '_tkinter'
	或者参照：http://www.qttc.net/201304306.html
	正确安装新版Python（在Linux中python默认是不安装Tkinter模块，）
		1 首先修改Setup.dist文件
		$ cd Python-3.5.4
		$ cp Modules/Setup.dist{,_$(date +%F)}
		$ vim Modules/Setup.dist		# 把下面相应行的注释去掉，修改具体版本
		_tkinter _tkinter.c tkappinit.c -DWITH_APPINIT \
		-L/usr/local/lib \
		-I/usr/local/include \
		-ltk8.5 -ltcl8.5 \
		-lX11
	
		以上第四行-ltk8.5 -ltcl8.5 默认是 8.2 ，请你系统实际tcl/tk版本修改:我系统中装的是8.5，所以这里我改成了8.5
		$ rpm -qa | grep ^tk
		tk-8.5.7-5.el6.x86_64
		tk-devel-8.5.7-5.el6.x86_64
		tkinter-2.6.6-66.el6_8.x86_64
			
		$ rpm -qa | grep ^tcl
		tcl-8.5.7-6.el6.x86_64
		tcl-devel-8.5.7-6.el6.x86_64

		2 安装tck-devel、tk-devel
		$ yum install tcl-devel tk-devel -y

		3 开始配置安装python
		$ ldconfig
		$ ./configure
		$ make && make install 

		4 验证
		新版Python是否可以使用tkinter模块
		$ python3
		>>> import tkinter
		>>>

		旧版Python是否可以使用tkinter模块	
		$ python
		>>> import Tkinter
		>>>
		
	8.18 升级gcc完，把/usr/local/lib*添加到系统动态链接库：echo -e "/usr/local/lib\n/usr/local/lib64"  >/etc/ld.so.conf.d/local_lib.conf后，
		执行ldconfig报错：ldconfig: /usr/local/lib64/libstdc++.so.6.0.19-gdb.py is not an ELF file - it has the wrong magic bytes at the start.
		不是 ELF 文件 - 它起始的魔数错误。


9 opencv
	https://m.2cto.com/kf/201610/557136.html
	http://techieroop.com/install-opencv-in-centos/	
	http://blog.csdn.net/zl18310999566/article/details/77880862
		
END




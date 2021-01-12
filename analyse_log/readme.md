# 开发环境说明
	电脑环境： Linux （推荐使用ubuntu16.04 64bit）
## 软件安装
	sudo apt install python3.5
	sudo apt install python3-tk python3-pip
	安装excel： pip3 install xlwt
	安装图形软件： pip3 install matplotlib
	matplotlib如果安装失败，可尝试降低版本
	pip install matplotlib==3.0
	用国内源： pip install -i https://pypi.tuna.tsinghua.edu.cn/simple matplotlib==3.0

	可解决此报错问题：ImportError: No module named 'pkg_resources.py2_warn'
	安装setuptools， md5=c607dd118eae682c44ed146367a17e26： 
	wget --no-check-certificate  https://pypi.python.org/packages/source/s/setuptools/setuptools-19.6.tar.gz
	tar -zxvf setuptools-19.6.tar.gz
	cd setuptools-19.6
	python3 setup.py build
	sudo python3 setup.py install

# 使用说明
	要分析的日志位置在目录log中， 新日志文件直接替换即可， 同时删除目录output。
	日志分析， 可通过命令查看都有哪些功能：./analyse_log，
	比如此时为：
	------------------------------- function -------------------------------
	./analyse_log version                   	 - version
	./analyse_log all                       	 - all
	./analyse_log analyse_map              		 - analyse map
	./analyse_log body_pose_2D              	 - body_pose_2D
	./analyse_log region_segmentation       	 - region_segmentation
	./analyse_log go_charge                 	 - go_charge
	./analyse_log find_string string         	 - find_string
	./analyse_log machine_state              	 - machine state
	./analyse_log message                    	 - message
	./analyse_log task_to_mcu              		 - set task to mcu
	./analyse_log power                              - power
	./analyse_log relocation                         - relocation

	./analyse_log analyse map_new                - analyse map_new
	./analyse_log power_new                      - power_new
	./analyse_log body_pose_2D_new               - body_pose_2D_new
	./analyse_log body_pose_3D_new               - body_pose_3D_new
	./analyse_log region_segmentation_new        - region_segmentation_new
	------------------------------------------------------------------------

	功能命令执行成功后， 输出文件保存在目录output。

## 地图分析
	./analyse_log analyse_map
	位姿，区域分割同时显示在一张图中，并可以移动鼠标来打印坐标。地图保存为文件map.png。

## 电量分析

## 位姿分析
	执行命令后， 会把坐标文件保存在目录output， 保存图形文件。 
	filter_BodyPose.log： 从日志文件中过滤出的位姿日志。
	BodyPose.log： 过滤后的坐标。

	2D：
	./analyse_log body_pose_2D

## 区域分割
	执行命令后， 会把日志文件保存在目录output， 保存图形文件。
	filter_CMotionPlanTask::StartCoverage.log： 从日志文件中过滤出的日志。
	region_segmentation.log： 过滤后的坐标。
	命令：
	./analyse_log region_segmentation

## 回充原因
	回充原因分析后的文件是go_charge.log
	命令：
	./analyse_log go_charge
	
## 查找字符串
	查找的字符串回保存在目录output中的find_string.log
	./analyse_log find_string string
	注意字符串中不要带空格, 字符串替换string。

## 执行所有功能
	图形显示的除外，输出结果保存在目录output，告警内容保存在error.log。filter_开头的文件是从原始日志中过滤出的日志。
	./analyse_log all
	
## 单独2D显示
	当运行过位姿命令后， 单独2D显示，可直接执行命令：
	./display_site_2D output/BodyPose.log

## 单独3D显示， 忽略此功能
	当运行过位姿命令后， 单独3D显示， 忽略此功能，可直接执行命令：
	./display_site_3D output/BodyPose.log

## 保存excel
	./go_charge_to_excel

## 机器状态
	./analyse_log machine_state， 结果保存在文件中， 错误保存中error.log。

## 特殊事件
	./analyse_log message， 结果保存在文件中， 错误保存中error.log。

## 发送给底板的命令
	./analyse_log task_to_mcu， 结果保存在文件中， 错误保存中error.log。

# 辅助命令
## 搜索字符串，并且显示
	grep "BodyPose" -nr ./log/

## 搜索字符串，保持文件
	grep "BodyPose" -nr ./log/ > ./output/tmp.log

## 计算文件行数
	wc -l ./output/tmp.log

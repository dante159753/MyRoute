#!/usr/bin/python
# -*- coding: utf-8 -*-
from urllib import *
from app.app import app
from app.models.category import Category
from app.helpers.category import CategoryHelper

Category.objects().delete()

program_icon = urlopen('http://www.pronovadesigns.com/wp-content/uploads/2014/03/web-programming1.jpg')
c_icon = urlopen('https://upload.wikimedia.org/wikipedia/commons/6/6f/Cimage.jpg')
cpp_icon = urlopen('http://avatar.csdn.net/blogpic/20140408151827593.jpg')
mfc_icon = urlopen('http://gaitaobao2.alicdn.com/tfscom/i4/T1BrgMXc0XXXXXXXXX_!!0-item_pic.jpg_310x310.jpg')
cocos2dx_icon = urlopen('http://avatar.csdn.net/blogpic/20120103185816438.jpg')
java_icon = urlopen('http://www.theinquirer.net/IMG/935/317935/java-logo-oracle-20-years-programming.jpg')
python_icon = urlopen('http://www.anxia.com/uploads/image/201501/291422523242436140.jpg')

art_icon = urlopen('https://cbsmiami.files.wordpress.com/2012/10/art-paint-jpg.png?w=300')
music_icon = urlopen('http://www.christchurchkennebunk.org/musicstaff.jpg')
sing_icon = urlopen('http://static.wixstatic.com/media/af2255_96fb29987ba64150b6c679f282b65cd0.jpg_256')
instrument_icon = urlopen('http://www.thecoolhunter.net/images/stories/2007pics/storiesnew2007pics/marchpics/1music.jpg')
painting_icon = urlopen('http://www.iconshock.com/img_jpg/PERSPECTIVE/general/jpg/256/paint_icon.jpg')



root_program = CategoryHelper.add(u'编程语言', u'编程语言（programming language），是用来定义计算机程序的形式语言。它是一种被标准化的交流技巧，用来向计算机发出指令。一种计算机语言让程序员能够准确地定义计算机所需要使用的数据，并精确地定义在不同情况下所应当采取的行动', None, program_icon)
c = CategoryHelper.add(u'C语言', u'C是一种通用的编程语言，广泛用于系统软件与应用软件的开发。于1969年至1973年间，为了移植与开发UNIX操作系统，由丹尼斯·里奇与肯·汤普逊，以B语言为基础，在贝尔实验室设计、开发出来。', root_program.id, c_icon)
cpp = CategoryHelper.add(u'C++', u'C++是一种广泛使用的计算机程序设计语言。它是一种通用程序设计语言，静态数据类型检查，支持多重编程范式，例如过程化程序设计、数据抽象化、面向对象程序设计、泛型程序设计、基于原则设计等。', root_program.id, cpp_icon)
mfc = CategoryHelper.add(u'MFC', u'微软基础类库（英语：Microsoft Foundation Classes，简称MFC）是一个微软公司提供的类库（class libraries），以C++类的形式封装了Windows API，并且包含一个应用程序框架，以减少应用程序开发人员的工作量。其中包含的类包含大量Windows句柄封装类和很多Windows的内建控件和组件的封装类。', cpp.id, mfc_icon)
cocos2dx = CategoryHelper.add(u'Cocos2d-x', u'Cocos2d-x是一个开源的移动2D游戏框架，MIT许可证下发布的。这是一个C++ Cocos2d-iPhone项目的版本。Cocos2d-X发展的重点是围绕Cocos2d跨平台，Cocos2d-x提供的框架。手机游戏，可以写在C++或者Lua中，使用API是Cocos2d-iPhone完全兼容。', cpp.id, cocos2dx_icon)
java = CategoryHelper.add(u'Java', u'Java是一种计算机编程语言，拥有跨平台、面向对象、泛型编程的特性，广泛应用于企业级Web应用开发和移动应用开发。', root_program.id, java_icon)
python = CategoryHelper.add(u'Python', u'Python是一种面向对象、直译式的计算机程序语言，具有近二十年的发展历史。它包含了一组功能完备的标准库，能够轻松完成很多常见的任务。它的语法简单，与其它大多数程序设计语言使用大括号不一样，它使用缩进来定义语句块。', root_program.id, python_icon)


root_art = CategoryHelper.add(u'艺术', u'艺术（英语：Art）指凭借技巧、意愿、想象力、经验等综合人为因素的融合与平衡，以创作隐含美学的器物、环境、影像、动作或声音的表达模式，以指和他人分享美的感觉或有深意的情感与意识的人类用以表达既有感知且将个人或群体体验沉淀与展现的过程。', None, art_icon)
music = CategoryHelper.add(u'音乐', u'音乐，广义而言，就是指任何以声音组成的艺术。英文Music一词源于古希腊语的μουσική（mousike），意即缪斯（muse）女神的艺术。而中文的音乐二字，许慎《说文解字》解释为“音，声也。生于心，有节于外，谓之音。”', root_art.id, music_icon)
sing = CategoryHelper.add(u'声乐', u'声乐是由一个或多个歌手表演的音乐形式之一，以人声为主要表演重点。', music.id, sing_icon)
instrument = CategoryHelper.add(u'器乐', u'器乐是相对于声乐而言，完全使用乐器演奏而不用人声或者人声处于附属地位的音乐。演奏的乐器可以包括所有种类的弦乐器、木管乐器、铜管乐器和打击乐器', music.id, instrument_icon)
painting = CategoryHelper.add(u'绘画', u'绘画在技术层面上，是一个以表面作为支撑面，再在其之上加上颜色的做法，那些表面可以是纸张或布，加颜色的工具可以通过画笔、也可以通过刷子、海绵或是布条等。', root_art.id, painting_icon)

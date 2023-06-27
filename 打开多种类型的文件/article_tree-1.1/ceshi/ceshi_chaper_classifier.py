# -*- coding: utf-8 -*-
from article_tree.chaper_classifier import chaper_classifier


def ceshi(data):
    cc = chaper_classifier(data)
    print(cc.line_nums)
    print(cc.line_ts)
    print(cc.line_types)


data1 = """二、审计调查发现的主要问题
（一）小微企业扶持政策制定、落地方面。
1.考核办法忽视对存量的持续跟踪。目前省市两级工作推进考核办法的考核指标以当年度新增任务完成数为主，未包括已完成任务的后续发展情况，导致部分市县重视当年新增任务指标而弱化了存量跟进措施。
2.小微企业联合信用约束惩戒机制建设需加快推进。嘉兴市本级等5个市县的市场监管部门已定期将工商经营异常企业名录库抄送政府各职能部门，但未按要求完全在政府采购、工程招投标和国有土地出让工作中与各职能部门建立联合约束工作机制，也未完全依法予以限制或禁入。
（二）小微企业科技创新扶持方面。作为测试存在的第二句话
1.创业投资引导基金未发挥预期效益。如杭州市富阳区和海宁市设立的3项创投基金，因投资额限制要求高、差别化不够等因素运行效果不佳，目前已停止运作。
部分市县科技创新券使用效果不佳。一是科技创新券兑付比例低。截至2016年6月底，嘉兴市本级、舟山市本级兑付2015年科技创新券仅占预算安排的3.09%、0.24%。二是发放的科技创新券种类单一，不能完全满足企业需求。个别市县支持范围过窄，仅限于检验检测、研发设计等内容。三是宣传推广和引导仍需加强。
（三）小微企业融资破难方面。
㊀“以扶持小微企业发展、服务‘三农’为出发点和落脚点”设立的政策性融资担保机构执行中存在偏差。如2015年杭州市富阳区政策性融资担保业务中小微企业数量仅占34.12%，担保金额仅占34.55%。
㊁部分市县政策性融资担保体系建设进度较慢。“小微企业三年成长计划”明确，“强化小微企业资源要素支撑……建立政策性融资担保体系”。截至2016年6月底，舟山市本级、海宁市和舟山市定海区尚未成立政策性融资担保机构。
四、审计调查发现问题的整改情况
针对本次审计调查发现的问题，省政府主要领导专门作了批示，要求相关部门认真研究推动小微企业发展及相关政策落实。省小微办对审计报告反映的问题逐项梳理分解，部署审计整改落实工作，各相关单位高度重视，积极采取措施落实整改。
㈠对小微企业扶持政策制定、落地方面的问题，省小微办已完善了7项58个评价指标，做到既重数量也重质量；由省发改委牵头，协调省工商局将全省经营异常企业名录和严重违法企业名单信息纳入省公共信用信息服务平台。
㈡对小微企业科技创新方面的问题，海宁市、杭州市富阳区通过将闲置资金纳入产业基金运营、创新创投引导基金投资方式等提升效益；通过扩大创新券适用范围、突破创新券地域限制、加大创新券宣传推广力度进一步提高科技创新券使用效果。
㈢对小微企业融资破难方面的问题，杭州市富阳区计划在今后的融资担保业务中要求合作银行推荐一批单户在300至500万元的小微企业作为重点担保对象；海宁市政策性融资担保机构已于2016年12月成立，舟山市的政策性融资担保机构改组方案正在制定中。
"""
data1_2 = """四、审计调查发现问题的整改情况
针对本次审计调查发现的问题，省政府主要领导专门作了批示，要求相关部门认真研究推动小微企业发展及相关政策落实。省小微办对审计报告反映的问题逐项梳理分解，部署审计整改落实工作，各相关单位高度重视，积极采取措施落实整改。
1.对小微企业扶持政策制定、落地方面的问题，省小微办已完善了7项58个评价指标，做到既重数量也重质量；由省发改委牵头，协调省工商局将全省经营异常企业名录和严重违法企业名单信息纳入省公共信用信息服务平台。
2.对小微企业科技创新方面的问题，海宁市、杭州市富阳区通过将闲置资金纳入产业基金运营、创新创投引导基金投资方式等提升效益；通过扩大创新券适用范围、突破创新券地域限制、加大创新券宣传推广力度进一步提高科技创新券使用效果。
3.对小微企业融资破难方面的问题，杭州市富阳区计划在今后的融资担保业务中要求合作银行推荐一批单户在300至500万元的小微企业作为重点担保对象；海宁市政策性融资担保机构已于2016年12月成立，舟山市的政策性融资担保机构改组方案正在制定中。
二、审计调查发现的主要问题
（一）小微企业扶持政策制定、落地方面。
1.考核办法忽视对存量的持续跟踪。目前省市两级工作推进考核办法的考核指标以当年度新增任务完成数为主，未包括已完成任务的后续发展情况，导致部分市县重视当年新增任务指标而弱化了存量跟进措施。
2.小微企业联合信用约束惩戒机制建设需加快推进。嘉兴市本级等5个市县的市场监管部门已定期将工商经营异常企业名录库抄送政府各职能部门，但未按要求完全在政府采购、工程招投标和国有土地出让工作中与各职能部门建立联合约束工作机制，也未完全依法予以限制或禁入。
（二）小微企业科技创新扶持方面。作为测试存在的第二句话
1.创业投资引导基金未发挥预期效益。如杭州市富阳区和海宁市设立的3项创投基金，因投资额限制要求高、差别化不够等因素运行效果不佳，目前已停止运作。
2.部分市县科技创新券使用效果不佳。一是科技创新券兑付比例低。截至2016年6月底，嘉兴市本级、舟山市本级兑付2015年科技创新券仅占预算安排的3.09%、0.24%。二是发放的科技创新券种类单一，不能完全满足企业需求。个别市县支持范围过窄，仅限于检验检测、研发设计等内容。三是宣传推广和引导仍需加强。
（三）小微企业融资破难方面。
1.“以扶持小微企业发展、服务‘三农’为出发点和落脚点”设立的政策性融资担保机构执行中存在偏差。如2015年杭州市富阳区政策性融资担保业务中小微企业数量仅占34.12%，担保金额仅占34.55%。
2.部分市县政策性融资担保体系建设进度较慢。“小微企业三年成长计划”明确，“强化小微企业资源要素支撑……建立政策性融资担保体系”。截至2016年6月底，舟山市本级、海宁市和舟山市定海区尚未成立政策性融资担保机构。

"""
data2 = """二、审计调查发现的主要问题
一是高精尖创新中心高端人才激励政策落实难。截至2016年3月底，市财政拨付12所院校13个高精尖创新中心经费结存8.1亿元，占拨入资金的87%。主要原因是引进高端人才存在困难，相关激励奖励经费不能支出。其次，受人员工资总额的限制，每年各中心应支付的科研人员奖励薪酬难以执行。
二是协同创新中心薪酬绩效管理需要完善。协同创新中心科研人员考核评价和薪酬发放，尚未改变以往的课题经费激励方式，仍单纯以论文、获奖等作为奖励性薪酬发放的主要标准。延伸审计发现，部分课题存在用往年研究结论充报成果或一题多报的情况。
三是中关村管委会发布的《中关村国家自主创新示范区企业担保融资扶持资金管理办法》等3个扶持中小企业融资的资金管理办法中，规定资金支持对象必须是中关村企业信用促进会会员，影响了资金分配公平。
四是初审机构对个别补贴申报材料审核把关不严。中关村科技融资担保有限公司等6家受托机构按照《中关村国家自主创新示范区企业担保融资扶持资金管理办法》对申报补贴企业进行审核，符合要求的予以资金扶持，审计发现初审机构对个别补贴企业的审核把关不严格，存在基础资料收集不全，个别企业未提供信用等级证书或企业提供的信用等级证书已失效等问题。
五是项目管理或审核办法不完善。2013年市教委与市财政局制定了《关于2011协同创新中心经费支持政策的意见》，提出将依据中央财政“2011协同创新中心”专项资金管理办法制定本市管理办法，但由于中央有关部门没有制定相关的经费使用办法，导致市教委自2013年协同创新中心创建至今，尚未出台经费使用管理办法。

"""
data3 = """一、财政资金统筹盘活方面
（一）至2016年9月底，教育部国家留学基金委“西部地区人才培养特别项目”结余资金1.79亿元，国土资源部土地勘测规划院“第二次全国土地调查项目”结余资金954.31万元，闲置超过2年未及时清理。
（二）至2016年9月底，广东省广州市财政局防范化解风险准备金专户中结转超过2年的存量资金为19.26亿元，未按规定优先用于偿还存量债务。
（三）根据非税收入管理要求，主管部门集中收入等应上缴相应级次国库并纳入预算管理。至2016年9月底，上海市民防办、质监局、体育局、卫生计生委分别有6050.51万元、5652.67万元、2303.7万元、134.63万元非税收入在本单位账户结转超过2年。
（四）至2016年9月底，天津市北辰区以新增建设用地土地有偿使用费专款专用为由，有3.26亿元财政资金结转超过2年。
（五）2011年至2015年，甘肃省财政厅共下达嘉峪关世界文化遗产保护工程——长城本体保护项目中央预算内资金2.68亿元，至2016年9月底，由于施工难度大等原因工程进展缓慢，中央预算内资金1.18亿元结转超过3年未使用。
（六）2013年2月，辽宁省鞍山市千山区财政局收到现代服务业综合试点项目中央财政补助资金1500万元，至2016年9月底，因城市规划调整项目未能实施，上述资金结存超过3年未使用。
（七）由于吉林省松原市财政局未及时将2013年彩票公益金分成资金692.68万元落实到具体的社会福利、体育等社会公益项目，至2016年9月底，上述资金结转超过2年未使用。
二、扶贫政策措施落实方面
（一）金融扶贫等3项扶贫政策措施落实不到位。
序号政策措施具体问题1金融扶贫政策云南省部分金融扶贫政策落实不到位。一是2015年至2016年，元阳县193名建档立卡贫困户申请的490.28万元贷款应享受而未能享受到扶贫贴息政策，应贴息未贴息24.5万元；二是泸水县扶贫到户贷款贴息执行进度较慢，至2016年9月底，2014年收到的贴息资金200万元实际兑付19.26万元，2015年收到的贴息资金192.5万元实际兑付22.69万元；三是抽查发现云南省农信社、中国邮政储蓄银行云南省分行发放的扶贫到户贷款中建档立卡贫困户比例较低，如中国邮政储蓄银行云南省分行发放的金额6.01亿元12425笔到户小额扶贫贷款中，为建档立卡户发放1.03亿元2229笔，发放额占比17.14%。2教育扶贫政策广西壮族自治区部分地方农村义务教育家庭经济困难寄宿生生活费补助政策执行不到位。一是至2016年9月底，全区各市县共结余寄宿生生活费补助资金7859.77万元（其中2013年和2014年度结余6561.73万元），未及时统筹安排使用；二是由于享受寄宿生补助学生受比例限制等原因，部分生活困难学生应享受未享受补助政策，抽查的桂平市共有743名建档立卡贫困子女、农村低保子女和孤儿等生活困难寄宿生未能享受补助；三是自治区扶贫建档立卡系统贫困人口学生子女“在校生状况”识别不精准，与全区学籍管理系统数据差异较大，有15.65万人未在学籍系统中。3以工代赈政策福建省建阳市莒口镇金山村至华家山乡村道路工程等56个项目，没有当地贫困农民或灾民参加建设，41个项目未公告劳务报酬发放情况。
（二）部分地区扶贫资金统筹整合不到位。
一是《国务院办公厅关于支持贫困县开展统筹整合使用财政涉农资金试点的意见》（国办发〔2016〕22号）印发后，经抽查，至2016年9月，河北省33个、云南省64个、贵州省32个、湖南省10个试点贫困县尚未按要求制定资金统筹整合使用方案，导致试点贫困县财政涉农资金统筹整合使用推进较慢。
二是由于统筹整合不到位等原因，至2016年9月底，抽审青海、甘肃等8个省的部分县（市），有1.47亿元扶贫资金闲置1年以上，其中9263.25万元结存2年以上未能及时盘活统筹使用。
序号涉及地区具体问题闲置金额（万元）其中：闲置2年以上金额（万元）1甘肃省陇西县至2016年9月底，因农户搬迁意愿发生变化、村镇规划调整、项目建设用地难以落实等原因，甘肃省陇西县2012年至2014年易地扶贫搬迁项目2951.3万元财政资金闲置2年以上。2951.32951.32云南省泸水县、兰坪县、元阳县至2016年9月底，因项目未实施、项目进展缓慢等，云南省泸水县、兰坪县、元阳县扶贫资金4470.09万元闲置1年以上，其中1136.73万元闲置2年以上。4470.091136.733河南省息县、桐柏等29个县至2016年9月底，河南省息县、桐柏等29个县2013年及以前的扶贫资金4488.2万元闲置超过2年。4488.24488.24湖南省麻阳县至2016年9月底，由于实施方案调整不及时等原因，湖南省麻阳县扶贫资金235.88万元闲置1年以上。235.8805青海省至2016年9月底，青海省金融扶贫贷款财政贴息资金中713.33万元在各县（区）扶贫部门结存1年以上，其中结存2年以上资金65.31万元。713.3365.316江西省宁都县至2016年9月底，由于扶贫项目未实施或进展缓慢等原因，江西省宁都县产业扶贫资金338万元闲置超过2年；宁都县扶贫办等单位2013年及以前年度扶贫资金112.7万元闲置超过2年。450.7450.77辽宁省岫岩满族自治县至2016年9月底，辽宁省岫岩满族自治县到户扶贫资金680.71万元结存在县财政局，闲置超过1年。680.7108四川省壤塘县至2016年9月底，由于项目进展缓慢，四川省壤塘县财政专项扶贫资金687.12万元闲置1年以上，其中闲置2年以上资金171.01万元。687.12171.01合计14677.339263.25
（三）28个单位和11名个人通过伪造合同、虚假票据列支、虚报工程量等方式骗取套取、侵占扶贫资金，或在扶贫工作中借机牟利，涉及金额957.02万元。
序号涉及地区具体问题金额（万元）1云南省元阳县2013年至2016年，云南省元阳县现代农业开发有限责任公司等2个单位通过虚报种植面积、虚报工程量等方式，套取扶贫贷款贴息等财政补助资金156.64万元。156.642甘肃省环县、康乐县、渭源县2013年至2015年，甘肃省环县、康乐县六合碧养殖专业合作社、康乐县德隆良种畜禽有限责任公司等9个企业、合作社，以及渭源县2名个人，通过重复申报或编造、伪造营业执照、贷款合同、帮扶协议、工资单等申报资料，骗取套取扶贫贷款贴息、农村危房改造补助等财政补贴资金439.8万元。此外，2009年至2016年，甘肃省环县7名村干部及村委会工作人员侵占、挪用村级扶贫互助资金6.8万元用于偿还个人贷款等支出。446.63贵州省晴隆县2014年和2015年，贵州省晴隆香馨茶叶有限公司使用虚假购茶发票报账套取扶贫资金100万元。1004宁夏盐池县2015年5月，宁夏金钥匙职业技能培训中心编制虚假的学员考勤表等资料，骗取农村劳动力技能培训资金6.67万元。6.675山西省临县2012年至2014年，山西省临县扶贫开发中心、教育体育科技局审核把关和监管不严格，致使部分学校、学生违规申领雨露计划补助资金71.88万元。审计指出问题后，临县扶贫开发中心等部门已追回违规资金59.7万元。71.886四川省小金县2015年，四川省小金县新格乡绿康种植合作社通过编造虚假出资材料、虚假残疾人受益名单等，套取农村残疾人扶贫专项资金10万元。107甘肃省甘肃经济日报社宣传报道扶贫工作时借机收费。2013年至2016年9月，甘肃经济日报社在报道甘肃省扶贫工作典型事例和经验做法时，借机按照自行制定的“广告”收费标准，共向30家市县扶贫管理部门收取费用125.4万元，其中2015年开设的《“1236”扶贫攻坚系列报道》专栏和2016年开设的《脱贫攻坚在路上》专栏刊登扶贫宣传文章28篇，收取费用95万元，平均每篇收费高达3.4万元。相关市县扶贫管理部门用财政资金支付了上述费用。125.48江西省寻乌县2015年至2016年9月，江西省寻乌县农村信用联社和中国农业银行寻乌县支行在向贫困户发放产业扶贫贷款时，向998位贷款贫困户搭车推销保险28.77万元。28.779云南省云龙县2016年，云南省云龙县农村信用联社11个分社在发放扶贫到户贷款时，向612户贷款贫困户搭车推销人身意外伤害保险9.46万元，获得保险公司手续费返还2.65万元。2015年至2016年该县农村信用联社关坪分社有关人员在为贫困户贷款办理借新还旧业务时从中收取手续费1.6万元。11.06合计957.02
（四）32个扶贫项目因脱离当地实际，后期管护不到位或与贫困户利益联结机制未落实等原因，建成后闲置废弃或者种养殖成活率低，项目效益不佳，无法实现预期扶贫效果，甚至形成损失浪费，涉及资金6371.87万元。
序号涉及地区具体问题金额（万元）1黑龙江省甘南县2014年至2015年，黑龙江省甘南县共组织实施产业扶贫项目12个，计划帮扶3229个贫困户脱贫。至2016年9月，实际完成投资3592.29万元，由于部分项目未实现与具体帮扶对象有效对接、项目建设管理不到位等原因，实际仅对接245户帮扶贫困户，且均未实现脱贫目标。3592.292陕西省商洛市2012年至2015年，陕西省商洛民乐现代农业科技发展有限责任公司申报并获得“产业扶贫园区项目”等4个项目财政扶持资金1230万元，审计发现，项目实施方案中所附的1386.08亩土地租赁合同为虚构，公司实际与农户签订土地租赁约300亩，建设温室蔬菜大棚28个（占地88.3亩）、阴阳棚9个（占地16亩）、连栋温室3000平方米（占地4.5亩）、冷库902平方米，未实现预期建设目标。12303云南省元阳县2013年至2015年，由于前期论证不充分、配套措施不完善、技术指导不到位等原因，云南省元阳县攀枝花乡、上新城乡、沙拉托乡实施的7个种养殖项目建成后闲置或废弃，财政资金618.23万元未能发挥效益或面临损失。618.234宁夏盐池县2011年至2012年，宁夏盐池县投入扶贫移民安置工程建设资金417.16万元，在花马池镇十六堡新村建设标准化养殖棚圈共304座，因农民外出务工和牲畜市场价格低等原因，养殖棚圈闲置。417.165贵州省晴隆县、贞丰县2014至2015年，因后期管护不到位等，贵州省晴隆县、贞丰县实施的核桃、葡萄、大棚蔬菜等3个种植类产业扶贫项目苗木存活率低或未与贫困户建立利益联结机制，179.19万元财政资金未能发挥效益。179.196重庆市丰都县、石柱县2013年至2015年，重庆市丰都县、石柱县实施的中药材种植等5个产业扶贫项目，因后期管护不力等，项目荒废或苗木大量死亡，实施效果不佳，涉及财政扶贫资金共计335万元。335合计6371.87
（五）5个扶贫项目推进缓慢，涉及资金1708.9万元。
序号涉及地区具体问题金额（万元）1黑龙江省甘南县2014年2月，黑龙江省财政厅下达甘南县兴鲜米业项目资金计划785.5万元，其中少数民族发展资金273万元，项目单位配套512.5万元，建设内容包括厂房、库房及设备购置，项目计划于2015年底完工，预期带动228户贫困户脱贫增收。至2016年9月底，项目完成投资376.7万元，设备购置尚未完成，项目无法投入运营。785.52湖北省宣恩县2015年，湖北省宣恩县安排44万元财政扶贫资金用于长潭河乡梨子坪村烟叶产业基地公路硬化项目，计划竣工时间为2015年11月。至2016年9月，因砂石料准备不足等，该项目已停工，仅建设1.3公里，尚有1.7公里未动工。443山东省巨野县山东省巨野县万丰镇彭庄村优质核桃种植项目计划投资54.4万元，应于2015年5月完工，至2016年9月底，由于土地流转不到位等原因，项目未完成。54.44贵州省兴仁县2015年4月和11月，贵州省兴仁县分别下达财政扶贫资金240万元、585万元，用于1040亩中药材玫瑰种植和1882亩中药材园区2个产业扶贫项目，计划于2016年2月和3月完成，由于项目前期准备不充分，土地落实困难等，至2016年9月，两个项目实际仅完成计划种植面积的一半。825合计1708.9
三、深化“放管服”改革方面
（一）民用航空器部件修理人员资格认定等4项资质、资格认定许可事项应取消未取消。
序号事项名称取消依据单位具体问题1安全培训机构资格认可国发〔2013〕19号能源局2014年以来，能源局在安全培训机构资格认可审批事项取消后，仍开展电力安全培训机构合格审查，并对1563名培训教师进行资格认定。2民用航空器部件修理人员资格认定、国外（境外）民用航空器维修人员资格认定国发〔2014〕5号民航局2014年1月以来，民航局未落实国务院取消民用航空器部件修理人员资格认定和国外（境外）民用航空器维修人员资格认定的要求，由交通运输部发布《民用航空器维修人员执照管理规则》（2016年交通运输部第32号令），对上述2项资格认定予以保留。3信息系统工程监理工程师资格认定国发〔2014〕5号中国电子企业协会信息系统工程监理资质工作委员会中国电子企业协会信息系统工程监理资质工作委员会2016年组织开展“信息系统工程监理工程师”登记管理工作，至2016年9月，共向2397人颁发证书。
（二）3项行政审批事项取消、下放后，后续管理或承接不到位。
1．2015年10月，国务院发文取消“基本医疗保险定点医疗机构资格审查”和“基本医疗保险定点零售药店资格审查”。至2016年9月，贵州省本级、贵阳市、六盘水市、贵安新区、黔东南苗族侗族自治州等5个统筹区，未按要求及时制定并公开地方医药机构协议管理办法，经办机构与医药机构的协议管理不完善。
2．2013年12月，河北省石家庄市将“产地植物检疫、调运植物和植物产品检疫”行政许可事项由市农业局下放至县（市）、区农业管理部门，由于各区农业管理部门缺乏必要技术力量，不具备承接能力，采取委托的方式由市农业局办理。2016年4月，该项行政许可又被重新收回至石家庄市农业局办理，未实现该行政许可事项下放的预期改革目标。
（三）个别地区行政审批事项前置审批条件清理不到位。
2016年8月，四川省阿坝州发展改革委在企业基本建设投资项目核准事项中，仍保留了河流水电规划、水电资源开发权授予、水电资源有偿使用、留州电量4项前置审批事项，上述事项未在国务院办公厅印发的《精简审批事项规范中介服务实行企业投资项目网上并联核准制度的工作方案》（国办发〔2014〕59号）规定的《企业投资项目核准的前置审批事项及设定依据一览表》目录中。
（四）个别地区电子政务平台利用率不高，影响投资效率。
国务院要求投资项目在线审批监管平台在2015年底实现全国范围“纵向贯通”试运行。经抽查，2016年1月至9月，广西壮族自治区有11个县（区）未录入投资项目，45个县（区）录入项目数量在5个以下，其中21个县（区）仅录入1个。由于未实现与其他行政审批系统数据互通，导致同一审批事项在多个系统中多次信息录入、审批，降低了审批效率。至2016年8月底，湖南省新宁县、邵阳市大祥区2个县（区）未启用在线审批平台受理业务，张家界市市本级以及常德市鼎城区、华容县、茶陵县3个县（区）在线审批办结数量仍为零。
四、涉企收费清理规范方面
（一）4个省的11个单位在国家明令取消、停征、免征后仍违规继续征收或超标准征收9项行政事业性收费和政府性基金等税费，共计1.41亿元。
序号收费单位收费事项收费时间违反的规定金额（万元）1辽宁省鞍山市房地产交易中心、鞍山市环境监测中心站、鞍山市国土资源局下属5个分局住房交易手续费、环境监测服务费和土地登记费2015年1月至2016年9月《财政部国家发展改革委关于取消、停征和免征一批行政事业性收费的通知》（财税〔2014〕101号）规定：自2015年1月1日起，对小微企业（含个体工商户）免征住房交易手续费、环境监测服务费和土地登记费等42项中央级设立的行政事业性收费。262湖南省耒阳市矿产品税费征收管理局水土流失防治费、育林基金、耕地占用税、森林植被恢复费2015年1月至2016年8月财政部等部门《关于印发〈水土保持补偿费征收使用管理办法〉的通知》（财综〔2014〕8号）规定：2014年5月1日起原各地区征收的水土流失防治费等予以取消。《财政部关于取消、停征和整合部分政府性基金项目等有关问题的通知》（财税〔2016〕11号）规定：将育林基金征收标准降为零。《中华人民共和国耕地占用税暂行条例》和财政部、国家林业局《森林植被恢复费征收使用管理暂行办法》（财综〔2002〕73号）规定：耕地占用税和森林植被恢复费应根据占用耕地面积和占用林地面积征收。1092.333河南省周口市住房和城乡建设局散装水泥管理办公室散装水泥专项资金2016年2月至9月《财政部关于取消、停征和整合部分政府性基金项目等有关问题的通知》（财税〔2016〕11号）规定：自2016年2月1日起，将散装水泥专项资金并入新型墙体材料专项基金。停止向水泥生产企业征收散装水泥专项资金。2504上海市浦东新区国资委下属上海南汇汇集建设投资有限公司和上海浦东工程建设管理有限公司预付款保证金2016年7月至9月《国务院办公厅关于清理规范工程建设领域保证金的通知》（国办发〔2016〕49号）规定：全面清理各类保证金。对建筑业企业在工程建设中需缴纳的保证金，除依法依规设立的投标保证金、履约保证金、工程质量保证金、农民工工资保证金外，其他保证金一律取消。对取消的保证金，自本通知印发之日起，一律停止收取。12737.44合计14105.77
（二）2家单位依托行政权力或履职便利，违规向企业收费926.56万元。
序号收费单位收费事项收费时间具体问题金额（万元）1黑龙江省黑河市财政局“资源综合利用增值税”退税返还资金2012年至2014年黑龙江省黑河市财政局在企业取得“资源综合利用增值税”退税后，与企业商定将已退税额按15%的比例缴回财政。2012年至2014年，共收取企业退税返还资金873.12万元。873.122青海省工商行政管理事务咨询服务中心企业设立、变更及注销代办费2013年至2016年9月青海省工商行政管理局下属事业单位出资成立的青海省工商行政管理事务咨询服务中心，依托青海省工商行政管理局的行政审批事项，违反规定代办企业设立、变更及注销等业务，向企业收取代办费53.44万元。53.44合计926.56
（三）3项行政审批中介服务事项清理规范不到位，仍由企业负担中介服务费1.35亿元。
序号审批部门中介服务收费事项收费时间违反规定金额（万元）1湖南省住房和城乡建设厅及各市州住房城乡建设部门施工图设计文件审查2016年3月至9月《湖南省人民政府关于第一批清理规范59项省政府部门行政审批中介服务事项的决定》（湘政发〔2016〕3号）规定：施工图设计审查不再由申请人委托有合法资质的机构审查，改为审批部门委托有合法资质的机构进行审查。《湖南省发展改革委关于取消、降标和放开一批涉企经营服务性收费的通知》（湘发改价服〔2016〕144号）规定：取消施工图审查服务费收费项目，审批部门在审批过程中委托开展的技术性服务活动，服务费用一律由审批部门支付并纳入部门预算。131052黑龙江省发展改革委项目评估评审费2015年5月至2016年9月《国务院办公厅关于清理规范国务院部门行政审批中介服务的通知》（国办发〔2015〕31号）规定：依照规定应由审批部门委托相关机构为其审批提供的技术性服务，纳入行政审批程序，一律由审批部门委托开展，不得增加或变相增加申请人的义务。106.63江西省南昌市发展改革委政府核准项目评估评审费2014年6月至2016年9月《政府核准投资项目管理办法》（2014年国家发展改革委第11号令）第十六条规定：评估费用由委托评估的项目核准机关承担”。《国家发展改革委关于进一步放开建设项目专业服务价格的通知》（发改价格〔2015〕299号）第四条规定：有关评估评审费用等由委托评估评审的项目审批、核准或备案机关承担”。334.73合计13546.33
（四）2家单位依托达标评比活动，自设名目向企业违规收费307.66万元。
序号收费单位依托收费事项收费时间具体问题金额（万元）1北京市工程建设质量管理协会北京市建筑、结构“长城杯”工程评比活动2015年至2016年6月北京市工程建设质量管理协会在开展北京市建筑、结构“长城杯”工程评比活动中，违反《社会组织评比达标表彰活动管理暂行规定》（国评组发〔2012〕2号）“社会组织不得在评选前后收取各种相关费用或者通过其他方式变相收费”的规定，要求参评建筑企业按照建筑规模缴纳咨询服务费，共计202.10万元。202.102江西省建设工程质量监督管理局门户网站开发和维护单位江西省优质建设工程奖2014年至2016年5月江西省住房和城乡建设厅违规开展江西省建设工程奖评选，同时违反《社会组织评比达标表彰活动管理暂行规定》（国评组发〔2012〕2号）“社会组织不得在评选前后收取各种相关费用或者通过其他方式变相收费”的规定，由江西省建设工程质量监督管理局门户网站开发和维护单位收取宣传费105.56万元。105.56合计307.66
五、重大建设项目实施方面
（一）个别地区和部门未及时确定设计调整方案，导致项目进展缓慢。新建兰州至甘南州合作市铁路项目于2014年12月开工建设，总投资103.8亿元，设计时速120公里/小时。2015年10月，甘肃省人民政府以兰合铁路设计时速与相连接的新建西宁至成都铁路不匹配等原因向中国铁路总公司申请将兰合铁路设计时速调整为200至250公里/小时。由于双方未及时研究确定建设标准调整方案，至2016年9月底，5个标段中仅1个标段累计完成投资2.62亿元，占项目概算总投资的2.52%，其余4个标段暂停招标或施工近一年。
（二）6个铁路项目因征地拆迁进展慢影响年度投资计划完成率。邯济铁路至胶济铁路联络线工程、秦沈铁路客运专线能力加强工程、锦承线义县至朝阳段扩能改造工程、锦承线朝阳至叶柏寿段扩能改造工程、高台山至阜新至锦州铁路新邱至义县段扩能改造工程和北京至沈阳客运专线北京段等6个项目2016年投资计划81.8亿元，因工作启动较晚、铁路项目单位未与地方政府就征地拆迁标准达成一致、工程建设临时用地未落实等原因造成征地拆迁工作推进缓慢，至2016年9月底，上述项目仅完成年度投资计划的15%、19.07%、19.29%、13.13%、27.5%和41.75%。
（三）部分项目因地方建设资金不到位影响建设进度。
一是山东省7个中央预算内投资大型灌区续建配套和节水改造工程项目总投资2.49亿元，其中市、县应配套资金1.22亿元，因9233万元配套资金不到位，应于2014年完成的项目至2016年9月底，仅完成投资计划的73.9%。二是辽宁省鞍山市惠民佳园小区等6个保障性安居工程项目因配套资金到位不及时，供水、供电、供暖等配套工程尚未完成，项目超期2年未完工。
（四）11个卫生、交通等建设项目因规划调整等原因进展缓慢。
一是甘肃省8个中央预算内投资卫生建设项目总投资1.06亿元，应在2015年前完工，由于城市规划调整、设计方案变更等原因，至2016年9月底仍未开工。二是浙江省三门县人民医院和浙江医院全科医生培养基地2个项目总投资4.61亿元，计划分别于2014年和2015年完工，由于三门县人民医院和浙江医院多次调整项目设计方案以及未有效推进项目建设，导致项目延迟两年才开工，建设进度严重滞后，至2016年9月，两个项目仅完成投资总额的36%和29%。三是江苏省芜申线高溧段航道整治工程新襟湖桥改建项目是交通运输部“十二五”期间长江黄金水道建设重点项目建设内容，概算投资4664万元，计划于2014年完工。因项目所在地南京市高淳区政府对设计方案反复提出修改意见，截至2016年9月底尚未开工。
（五）个别项目建成后闲置或未达到预期效益。
一是辽宁省鞍山市2013年至2014年交付立山区使用的551套廉租住房和303套公共租赁住房至今尚未分配使用，闲置时间超过2年。二是江西省景德镇市西瓜洲污水处理厂和乐平市污水处理厂一期扩建工程分别于2009年和2014年建设完成，实际完成投资1.09亿元。由于配套管网建设未完成等原因，两个污水处理厂污水处理量等主要指标未达到预期目标。"""
data4 = """二、审计发现的主要问题
（一）预算执行方面存在的问题
1.2013年至2017年，区体育局本级将上级补助收入1350.29万元在“其他应付款”科目中核算，未纳入单位预算统一管理；2017年区体育局本级将其他收入44.16万元在“暂存款”科目中核算，未纳入单位预算统一管理。
2.2017年，所属区体产中心编报决算支出978.90万元，账面实际支出1109.63万元，少编报决算支出130.73万元。
3.至2017年底，区体育局本级及所属区社体中心等3个事业单位未按规定统筹盘活项目结余资金79.45万元。
4.2017年，区体育局本级未经批准将全民健身现场推进会预算资金60.39万元调整用于林芝高原训练基地物资采购及林芝市体育局等相关单位体育设施和场馆维修。
至2017年底，区体育局本级及其所属6个全额拨款事业单位共有63个项目预算执行进度缓慢，涉及资金5388.6万元。6.2017年，所属区体产中心体育场馆维护费超预算支出134.38万元；所属区社体中心马料款超预算支出42万元，水电费超预算支出74.17万元。7.2017年，区体育局本级从体育场馆专项经费中列支聘用人员工资及局本级水费8万元。（二）其他方面存在的问题1.至2017年底，区体育局本级应收款项8.21万元长期挂账，未及时进行清理。2.2016年11月，所属区登山运动管理中心未经相关部门批准，违规将自治区全民健身活动中心（公益性）出租给个体经营户使用。三、审计处理情况和建议对上述问题，自治区审计厅已依法出具了审计报告、下达了审计决定书。对收入未纳入单位预算统一管理问题，要求调整有关账目；对少编报决算支出问题，要求据实编报部门决算报表，准确反映预算执行结果；对未统筹盘活项目结余资金问题，要求清理上缴自治区财政；对未经批准调整预算问题，要求严格按照相关规定调整预算支出；对预算执行进度缓慢问题，要求严格按照要求组织实施项目，加快预算执行进度；对超预算支出和扩大开支范围问题，要求加强预算支出管理；对应收款项长期挂账问题，要求及时进行清理、催收和结算；对违规出租国有资产问题，要求按规定办理国有资产出租事宜。针对审计发现的问题，自治区审计厅建议：区体育局应加强本级及所属单位预算、决算管理，加快项目建设进度和预算执行进度，及时清理项目结余资金及应收款项，督促所属单位加强国有资产管理，对出租的国有资产严格按规定履行报批程序。四、审计发现问题的整改情况目前，区体育局已组织整改。具体整改结果由区体育局向社会公告。
"""
data5 = """二、审计发现的主要问题及整改情况
（一）财政财务管理方面1.省安监局所属事业单位及协会无依据收取服务单位考核培训费、安全评价费、评审费等各类费用共计1502.2万元，主要用于人员工资及运行经费。
该问题已移送省发展改革委价格监督检查与反垄断局处理。
2.省安监局截留所属青海省安全生产宣传教育中心安全生产宣传教育专项资金28万元，用于局本级人员安全生产培训支出。
针对该问题，省安监局已对局本级人员安全生产培训费单独立项，做到专款专用。
3.2015年至2017年，省财政厅下达省安监局《青海安全十年回眸》编撰费等8个项目专项资金1367.8万元，项目已实施完毕，资金结余174.81万元，未及时上缴财政。
针对该问题，省安监局已将结余资金全部上缴省财政。
4.调离或退休人员使用的3台数码照相机和1台笔记本电脑未及时收回。
针对该问题，省安监局已收回1台数码照相机和1台笔记本电脑，剩余2台数码照相机仍未收回。
（二）专项资金管理使用和其他方面
1.2015年至2017年，海西州安监局、海北州安监局、祁连县安监局均存在将安全生产专项资金与行政经费和其他专项资金混用的情况。
针对该问题，省安监局加强了对州县安监部门的监督，组织专门人员对部分州、县安监局专项资金使用情况进行了检查。2.2015年2月，省安监局确定由江泰保险经纪公司承担全省高危行业安全生产责任险经纪服务，但该公司未按规定提取事故预防控制费，省安监局也未履行监管职责。
针对该问题，省安监局已督促该公司设立事故预防控制费专账并完善了相关制度。
3.2017年4月，由于安全评价资质到期，省安监局决定注销青海省安全生产科学技术中心注册成立的青海中正安全科技有限公司，截至2018年4月，该公司仍未注销。
针对该问题，省安监局于2018年7月31日完成青海中正安全科技有限公司注销登记手续。
4.2016年12月，省安监局在所属青海省安全生产宣传教育中心列支玉树州囊谦县季曲乡外户卡村高原美丽乡村帮扶资金10万元。
针对该问题，省安监局明确今后将杜绝此类问题。"""
data6 = """四、审计调查发现问题的整改情况
针对本次审计调查发现的问题，省政府主要领导专门作了批示，要求相关部门认真研究推动小微企业发展及相关政策落实。省小微办对审计报告反映的问题逐项梳理分解，部署审计整改落实工作，各相关单位高度重视，积极采取措施落实整改。
1.对小微企业扶持政策制定、落地方面的问题，省小微办已完善了7项58个评价指标，做到既重数量也重质量；由省发改委牵头，协调省工商局将全省经营异常企业名录和严重违法企业名单信息纳入省公共信用信息服务平台。
2.对小微企业科技创新方面的问题，海宁市、杭州市富阳区通过将闲置资金纳入产业基金运营、创新创投引导基金投资方式等提升效益；通过扩大创新券适用范围、突破创新券地域限制、加大创新券宣传推广力度进一步提高科技创新券使用效果。
3.对小微企业融资破难方面的问题，杭州市富阳区计划在今后的融资担保业务中要求合作银行推荐一批单户在300至500万元的小微企业作为重点担保对象；海宁市政策性融资担保机构已于2016年12月成立，舟山市的政策性融资担保机构改组方案正在制定中。
二、审计调查发现的主要问题
（一）小微企业扶持政策制定、落地方面。
1.考核办法忽视对存量的持续跟踪。目前省市两级工作推进考核办法的考核指标以当年度新增任务完成数为主，未包括已完成任务的后续发展情况，导致部分市县重视当年新增任务指标而弱化了存量跟进措施。
2.小微企业联合信用约束惩戒机制建设需加快推进。嘉兴市本级等5个市县的市场监管部门已定期将工商经营异常企业名录库抄送政府各职能部门，但未按要求完全在政府采购、工程招投标和国有土地出让工作中与各职能部门建立联合约束工作机制，也未完全依法予以限制或禁入。
（二）小微企业科技创新扶持方面。作为测试存在的第二句话
1.创业投资引导基金未发挥预期效益。如杭州市富阳区和海宁市设立的3项创投基金，因投资额限制要求高、差别化不够等因素运行效果不佳，目前已停止运作。
2.部分市县科技创新券使用效果不佳。一是科技创新券兑付比例低。截至2016年6月底，嘉兴市本级、舟山市本级兑付2015年科技创新券仅占预算安排的3.09%、0.24%。二是发放的科技创新券种类单一，不能完全满足企业需求。个别市县支持范围过窄，仅限于检验检测、研发设计等内容。三是宣传推广和引导仍需加强。
（三）小微企业融资破难方面。
1.“以扶持小微企业发展、服务‘三农’为出发点和落脚点”设立的政策性融资担保机构执行中存在偏差。如2015年杭州市富阳区政策性融资担保业务中小微企业数量仅占34.12%，担保金额仅占34.55%。
2.部分市县政策性融资担保体系建设进度较慢。“小微企业三年成长计划”明确，“强化小微企业资源要素支撑……建立政策性融资担保体系”。截至2016年6月底，舟山市本级、海宁市和舟山市定海区尚未成立政策性融资担保机构。

"""
data7 = """三、审计调查发现的主要问题
(一)执行国家、省委、省政府政策方面存在的问题。
1.农垦集团期货部违规从事期货经纪业务。
农垦集团期货部属农垦集团非法人资格的二级核算单位，于1997年在上海期货交易所取得自营席位（非经纪会员），无期货经纪业务资质。截至2009年3月末，该部违规向农垦集团内部、外部的单位及自然人44户出租、出借席位进行期货交易。
2.土地资源管理工作不到位。
农垦集团所属河口分公司新建的制胶厂厂房、仓库、生产队仓库、收胶站等占用的土地未办理土地使用权证，所属红河农垦部分变更土地使用性质未按规定办理相关手续，所属临沧双江农场签订虚假合同转让土地1998平方米。
3.云南农垦系统的医疗机构移交地方不彻底。
截至2008年底，农垦系统共有115个医疗机构，至审计调查结束时只移交地方管理7所，尚余108所未移交。
(二)体制机制上存在的主要问题。
1.决策机制不灵活。审计调查发现，云南农垦在一些事关全局的重大问题上，决策机制不灵活，程序复杂，不利于解决问题。
2.体制存在漏洞，工资收入不合理。1997年以来，农垦总局、集团一直实行“一套班子，两块牌子”的管理模式，截至2008年末，农垦集团本部有104人隶属于农垦总局机关，橡胶产业公司有16人隶属于农垦总局机关。以上人员(120人)在职时实行农垦集团的绩效工资标准，退休时却执行公务员工资待遇。
3.农垦集团本部、期货部和电子商务交易中心管理关系不顺。一是隶属关系不顺，期货部作为农垦集团本部非法人资格的二级核算单位，法人代表是农垦集团董事长，却隶属于电子商务交易中心(农垦集团的二级法人单位)管理。二是业务不顺，期货部财务经理由电子商务交易中心财务经理兼任，但该经理却不了解期货部的业务情况。
(三)管理中存在的主要问题。
1.项目投资大，效益差，涉及金额19221.63万元。
农垦总局办公大楼（鼓楼工程）于1995年5月1日用下属等单位的集资款15370.82万元进行投资建设，至今一直处于无法使用状态，造成资产闲置；思茅农场医院投资700万元，地处闹市区，但该医院近3年仅实现收入112.52万元，年人均创收6357元，基本丧失了服务企业的功能，资产运营低效；西双版纳东风农场万头奶水牛良种繁育体系建设项目2004年开始启动，已投资236.37万元，2005至2008年累计收入仅13.87万元，投资大、效益差；红河农垦分局河口农场2004年投资480多万元建设的山腰边贸综合市场，资产闲置，投资难以收回；黎明农场投资淀粉厂，总投资1636.97万元，从1998年至2008年，累计亏损2086.92万元，2008年1月28日停产，预计资产损失1726.44万元，存在损失风险；东风分公司制胶厂投资概算5339.82万元，截至2008年末，共投入资金797.47万元。至今处于停工状态，资产闲置。
2.所属孟连农场擅自分配国有资产收益854.64万元。
2006年，普洱农垦分局部分干部及孟连农场职工根据云南省农垦总局的批准，集资入股465.33万元成立孟连复兴橡胶股份有限公司。该公司至2009年3月尚未成立，一直延用原属国有经济性质的云南省国营孟连农场复兴商号(简称复兴商号)的营业执照和税务登记证。孟连农场将其在境外种植已开割的4000多亩国有橡胶林注入事实上不存在的公司。3年来，有关人员根据事实上不存在的孟连复兴橡胶股份有限公司章程规定，分配国有企业复兴商号的利润854.64万元，其中：2006年分配288.61万元，2007年290.55万元，2008年275.48万元。2006年、2007年用当年实现税前利润分红，2008年分红股利直接进入成本费用。
3.境外天然橡胶资产未妥善管理，存在流失隐患。西双版纳农垦分局成立的勐腊振华商行在境外独资开发了3500亩天然橡胶林，该项资产在勐腊振华商行的账上没有反映。另外，该商行负责人已被调到云南天然橡胶产业股份公司的子公司云橡投资有限公司，调走之前，农垦总局对勐腊振华商行的资产、债务等未进行认真清理，该商行资产的完整性、安全性得不到保障。
4.所属临沧农垦分局用50万元公款以分局职工个人名义入股成立公司。2009年临沧农垦分局拨出公款150万元，其中50万元是以分局职工个人名义和其他股东成立耿马古贡茶联合开发有限公司。
5.所属单位账外资金、资产911.23万元。临沧、西双版纳农垦分局等单位采取收入不入账等方式形成账外资金369.74万元；账外资产541.48万元，其中西双版纳分局接受移交资产未入账，形成账外资产61.14万元；红河农垦分局新建办公大楼未纳入固定资产核算，形成账外资产348.34万元；西双版纳国营东风农场以土地使用权评估价132万元出资，与西双版纳昆曼运输有限责任公司合资组建东风昆曼运输有限责任公司并持有49%股份，该项资产未在财务账中反映，形成账外资产。
6.专项资金管理使用存在的问题，涉及金额1175.88万元。
弥勒东风农场等单位挤占、挪用专项资金736.56万元；西双版纳东风分公司违规发放、使用天然橡胶良种补贴18.82万元。瑞丽农场专项资金420.5万元未专户专账核算。
7.红河农垦分局擅自用公款160万元为私人购房。
8.普洱农垦分局2006年以收取工作协调费、土地协调费等名义向下属单位违规摊派收取费用40万元。
(四)财务核算中存在的主要问题。
1.收入、成本费用不实27982.35万元，其中：少计收入17108.69万元，多计成本费用6010.56万元，少计成本费用4863.1万元。
2.漏缴、未缴税费357.42万元。
3.往来款4376.74万元未及时对账或清理。
2008年末，对于1995年以前潞江农场借边境贫困农场事业费等往来款项3627.89万元，农垦总局财务处长期未进行清理；西双版纳、普洱分局代农垦集团收取的管理费508.85万元长期挂账；临沧分局与勐撒农场双方往来款相差240万元。
4.资产未按规定计价核算，农垦总局(集团)资产不实。
29950.87万元。普洱兴盛房地产开发有限公司11宗土地未作价入账，资产不实27504.71万元；河口分公司资产不实1858.7万元；弥勒东风农场资产不实142.53万元；文山农垦联合发展有限责任公司资产不实444.93万元。
五、审计发现问题的整改情况
云南省农垦总局（集团）针对本次审计调查发现的问题，及时下发了《云南省农垦总局（集团公司）贯彻落实省审计厅对农垦审计决定和对相关问题及时整改的通知》（云垦局〔2010〕24号），将农垦总局（集团公司）违反财经法规的问题及专项整改任务分解落实到各责任单位，并将整改和处理结果纳入2009年度决算之中，未按时完成整改任务的，追究相关单位主要负责人责任，并对每个具体问题专设督办人进行督办。临沧农垦分局根据审计建议，及时下发了《临沧市农垦分局关于切实加强农垦企业经营管理的若干规定》（临垦局发〔2009〕39号）、《财务管理制度》等内控制度。对农垦集团期货部违规从事期货经纪业务的问题，期货部已进行了账户清理，及时出台了《期货部工作岗位职责（暂行）》（云垦商务〔2009〕11号）等8个管理制度。对土地资源管理工作不到位的问题，农垦总局（集团）正在认真清理出让的土地并按规定完善各项相关手续，双江农场已按规定向上级部门申报，完善相关手续。对农垦系统的医疗机构移交地方管理不彻底的问题，农垦总局（集团）表示要积极争取地方党委、政府的支持，全面完成移交企业办社会职能；对机制体制中存在的主要问题，农垦总局（集团）将结合“二次创业”，积极改革管理体制，理顺行政管理体制和企业管理体制，加快政企分开、政事分开步伐；对项目投资大、效益差的问题，农垦总局（集团）正积极与有关单位协商，争取妥善处理鼓楼工程的闲置问题，农垦总局（集团）及其下属有关单位表示要以此为教训，今后要加强对对外投资的可行性研究，避免因投资、决策不慎导致的国有资产损失；对孟连农场擅自分配国有资产收益854.64万元的问题，农垦总局（集团）表示要对该事项进行深入调查，查清产生的问题及原因，并区别不同情况进行妥当处理；对境外天然橡胶资产未妥善管理，存在流失隐患的问题，农垦总局（集团）正对振华商行的经营情况进行认真清理，并规范其管理；对临沧农垦分局用50万元公款以分局职工个人名义入股成立公司的问题，临沧农垦分局已按国家国有资产管理规定进行资产处置，注销了耿马古贡茶联合开发有限公司并清理收回了用公款以分局职工个人名义入股的全部款项；对下属单位账外资金、资产911.23万元的问题，农垦总局（集团）正在根据资产的产权调增相应的资产，调整相关账目，其中，临沧农垦分局已将账外核算“小金库”的收入310.73万元，支出309.64万元和余额1.09万元纳入临沧分公司的企业账内进行核算，分局行政主要领导主动向集团公司党委检查错误，总局(集团)责成分局主要领导就“小金库”问题在分局机关支部大会上作检查，并将检查情况报集团公司纪委备案；对西双版纳农垦分局和云南橡胶股份公司东风分公司设立账外资金的问题也分别作了处理决定，对相关人员进行了处理，版纳东风农场已将账外资产调入农场财务统一进行核算，其他需要调整的账目，各相关单位正在进行纠正、处理；对专项资金管理使用存在的问题，农垦总局（集团）已要求各单位严格按照专项资金管理各项规定，实行专款专用、专户管理，要求各单位追回被挤占、挪用专项资金并归还其原渠道；对红河分局擅自用公款160万元为私人购房的问题，红河农垦分局已进行了处理并追回160万元公款；对普洱分局向下属单位违规摊派收取费用40万元的问题，农垦总局(集团)已责成普洱分局将收取的工作协调费、土地协调费全额退还下属有关单位；对收入、成本费用不实的问题，农垦总局（集团）责成各单位对往来账目进行认真清理或核对，并及时调整相关会计科目；对漏缴、未缴税费357.42万元的问题，农垦各企业、事业单位正积极向当地税务部门申报、补缴各项税费，其中，临沧分局已到税务机关补缴了个人所得税；对往来款4376.74万元未及时对账或清理的问题，农垦总局（集团）已责成以上各单位应对往来账目进行清理或核对，并调整相关会计账目，其中，临沧农垦分局已将分局列支给勐撒农场的240万元作为借款处理，调增了对勐撒农场的应收款项；对资产未按规定计价核算的问题，农垦总局（集团）已责成相关单位严格按照财务核算的相关规定，调整会计科目，规范其财务核算。
"""
data8 = """三、审计发现的主要问题及整改情况
(一)30个项目计划执行管理不够规范。一是12个培训计划调整缺少报批环节。2011年至2012年，四县有8个人力资源开发项目计划内的部分培训班次未实施，有4个人力资源开发项目在计划外新增了部分培训班次，但均缺少报批环节。二是1个项目计划调整不够细化。三是17个项目在2013年底前完成存在一定压力。2011年至2013年，计划安排项目339个。截至2013年9月底，尚未完成当年建设任务的项目为17个，至2013年年底前，这17个项目完成当年计划存在一定压力。
审计指出后，前方指挥部高度重视，已要求四县有关部门对培训计划发生变化的项目补办相关手续，并上报前方指挥部备案。同时，前方指挥部已督促当地责任部门或单位抓紧项目实施，力争完成2013年的计划建设任务。
(二)9个项目财务管理不够规范。一是莎车县4个由当地负责主办的培训班未及时结算，涉及援疆资金共计134.51万元。二是泽普、莎车及统筹的3个培训项目支付依据不够充分，涉及援疆资金共计111.3万元。三是1个统筹项目结算资料不齐全，缺少合同、移交签收单等资料。四是1个项目收取管理费缺乏依据。
审计指出后，莎车县4个由当地负责主办的培训班已办理了结算；泽普、莎车及统筹的3个支付依据不够充分的培训项目，前方指挥部已要求相关单位补充项目支付依据，并及时归集项目结算资料，确保项目结算合法合规；另外，前方指挥部已与相关单位就管理费事宜达成一致，相关单位已重新调整并完成了决算手续。
(三)4个项目立项手续不完善或立项批复执行不规范。一是3个项目未办理前期立项审批手续。叶城、泽普两个县的3个“三降一提高”项目未经县发展改革委的前期立项审批，造成项目实施内容与标准不够明确，涉及金额共计2400万元。二是1个项目资金未按立项批复使用。莎车县卫生局未按莎车县发展改革委《关于上海市对口援建莎车县人民医院门诊、内科门诊、医技、120指挥调度中心综合楼项目初步设计和招标方案的批复》中上海援疆资金3000万元用于莎车县人民医院门诊、内科门诊、医技、120指挥调度中心综合楼项目土建工程建设的规定，而是将其中的1000万元用于莎车县人民医院购置1.5T核磁共振设备，且该设备的购置未经有关部门立项审批。
审计指出后，相关县政府已按要求完善了相关项目的审批手续。前方指挥部要求各相关县政府在今后的援疆项目管理中规范项目前期审批手续，并确保有效执行。
"""
data9 = """三、审计发现的问题及建议
（一）违反国家法规或贷款协定的问题
1.部分项目办虚报冒领世界银行贷款，列支不合格支出累计人民币991,660.17元。
1.1西宁市项目办列支措施项目费人民币862,613.34元证据不足。
1.2西宁市项目办列支工程支出人民币129,046.83元证据不足。
2.大通县财政局滞留世界银行回补资金人民币2,078,964.64元。
3.部分工程设计、技术服务合同未按规定进行招投标。
3.1 2012年度，西宁市项目办未履行招标程序，与甘肃省水利水电勘测设计院签订了《西宁防洪及流域管理利用世行贷款项目中期计划调整报告建设合同》，金额为人民币1,800,000元，由配套资金支付。
3.2 2013年4月，西宁市项目办未履行招标程序，与青海水利水电科技发展有限公司签订技术服务合同，委托其进行质量检测专项技术服务，金额为人民币550,000元，由配套资金支付。
（三）使用国际组织或者外国政府贷款、援助资金的项目”和《工程建设项目招标范围和规模标准规定》（国家发展计划委员会令第3号）第七条“本规定第二条至第六条规定范围内的各类工程建设项目，包括项目的勘察、设计、施工、监理...达到下列标准之一的，必须进行招标：(三)勘察、设计、监理等服务的采购，单项合同估算价在50万元人民币以上的”规定。
4.部分工程未按规定程序实施，存在未批先建现象。
（二）内部控制方面存在的问题
（三）项目管理方面存在的问题
1.部分工程项目擅自变更已批准的初步设计。
2.部分工程项目管理程序不规范。
（四）项目绩效方面存在的问题
（五）上一年度审计发现问题未整改情况
一、违反国家法规或贷款协定问题的整改情况
（一）部分项目办虚报冒领世界银行贷款，列支不合格支出累计99.17万元的问题。
（二）大通县财政局滞留世界银行回补资金207.90万元的问题。
（三）部分工程设计、技术服务合同未按规定进行招投标的问题。
（四）部分工程未按规定程序实施，存在未批先建现象的问题。
二、内部控制方面存在问题的整改情况
三、项目管理方面存在问题的整改情况
（一）部分工程项目擅自变更已批准的初步设计的问题。
（二）部分工程项目管理程序不规范的问题。
四、项目绩效方面存在问题的整改情况"""

if __name__ == '__main__':
    # '㈠', '㈡''㊀', '㊁'
    # ceshi(data4)
    # ceshi(data5)
    # ceshi(data6)
    # ceshi(data7)
    ceshi(data8)

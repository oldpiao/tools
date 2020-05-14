from faker import Faker
f = Faker('zh_CN')


print(f.city_suffix())  # 市，县
print(f.country())  # 国家
print(f.country_code())  # 国家编码
print(f.district())  # 区
# print(f.geo_coordinate())  # 地理坐标
print(f.latitude())  # 地理坐标(纬度)
print(f.longitude())  # 地理坐标(经度)
print(f.lexify())  # 替换所有问号（“？”）带有随机字母的事件。
print(f.numerify())  # 三位随机数字
print(f.postcode())  # 邮编
print(f.province())  # 省份
print(f.street_address())  # 街道地址
print(f.street_name())  # 街道名
print(f.street_suffix())  # 街、路
print(f.random_digit())  # 0~9随机数
print(f.random_digit_not_null())  # 1~9的随机数
print(f.random_element())  # 随机字母
print(f.random_int())  # 随机数字，默认0~9999，可以通过设置min,max来设置
print(f.random_letter())  # 随机字母
print(f.random_number())  # 随机数字，参数digits设置生成的数字位数
print(f.color_name())  # 随机颜色名
print(f.hex_color())  # 随机HEX颜色
print(f.rgb_color())  # 随机RGB颜色
print(f.safe_color_name())  # 随机安全色名
print(f.safe_hex_color())  # 随机安全HEX颜色
print(f.bs())  # 随机公司服务名
print(f.company())  # 随机公司名（长）
print(f.company_prefix())  # 随机公司名（短）
print(f.company_suffix())  # 公司性质
print(f.credit_card_expire())  # 随机信用卡到期日
print(f.credit_card_full())  # 生成完整信用卡信息
print(f.credit_card_number())  # 信用卡号
print(f.credit_card_provider())  # 信用卡类型
print(f.credit_card_security_code())  # 信用卡安全码
print(f.currency_code())  # 货币编码
print(f.am_pm())  # AM/PM
print(f.century())  # 随机世纪
print(f.date())  # 随机日期
print(f.date_between())  # 随机生成指定范围内日期，参数  # start_date，end_date取值  # 具体日期或者today,-30d,-30y类似
print(f.date_between_dates())  # 随机生成指定范围内日期，用法同上
print(f.date_object())  # 随机生产从1970-1-1到指定日期的随机日期。
print(f.date_this_month())  #
print(f.date_this_year())  #
print(f.date_time())  # 随机生成指定时间（1970年1月1日至今）
print(f.date_time_ad())  # 生成公元1年到现在的随机时间
print(f.date_time_between())  # 用法同dates
print(f.future_date())  # 未来日期
print(f.future_datetime())  # 未来时间
print(f.month())  # 随机月份
print(f.month_name())  # 随机月份（英文）
print(f.past_date())  # 随机生成已经过去的日期
print(f.past_datetime())  # 随机生成已经过去的时间
print(f.time())  # 随机24小时时间
# print(f.timedelta())  # 随机获取时间差
print(f.time_object())  # 随机24小时时间，time对象
print(f.time_series())  # 随机TimeSeries对象
print(f.timezone())  # 随机时区
print(f.unix_time())  # 随机Unix时间
print(f.year())  # 随机年份
print(f.file_extension())  # 随机文件扩展名
print(f.file_name())  # 随机文件名（包含扩展名，不包含路径）
print(f.file_path())  # 随机文件路径（包含文件名，扩展名）
print(f.mime_type())  # 随机mime Type
print(f.ascii_company_email())  # 随机ASCII公司邮箱名
print(f.ascii_email())  # 随机ASCII邮箱
print(f.ascii_free_email())  #
print(f.ascii_safe_email())  #
print(f.company_email())  #
print(f.domain_name())  # 生成域名
print(f.domain_word())  # 域词(即，不包含后缀)
print(f.email())  #
print(f.free_email())  #
print(f.free_email_domain())  #
print(f.safe_email())  # 安全邮箱
print(f.image_url())  # 随机URL地址
print(f.ipv4())  # 随机IP4地址
print(f.ipv6())  # 随机IP6地址
print(f.mac_address())  # 随机MAC地址
print(f.tld())  # 网址域名后缀(.com,.net.cn,等等，不包括.)
print(f.uri())  # 随机URI地址
print(f.uri_extension())  # 网址文件后缀
print(f.uri_page())  # 网址文件（不包含后缀）
print(f.uri_path())  # 网址文件路径（不包含文件名）
print(f.url())  # 随机URL地址
print(f.user_name())  # 随机用户名
print(f.isbn10())  # 随机ISBN（10位）
print(f.isbn13())  # 随机ISBN（13位）
print(f.job())  # 随机职位
print(f.paragraph())  # 随机生成一个段落
print(f.paragraphs())  # 随机生成多个段落，通过参数nb来控制段落数，返回数组
print(f.sentence())  # 随机生成一句话
print(f.sentences())  # 随机生成多句话，与段落类似
print(f.text())  # 随机生成一篇文章（不要幻想着人工智能了，至今没完全看懂一句话是什么意思）
print(f.word())  # 随机生成词语
print(f.words())  # 随机生成多个词语，用法与段落，句子，类似
print(f.binary())  # 随机生成二进制编码
print(f.boolean())  # True/False
print(f.language_code())  # 随机生成两位语言编码
print(f.locale())  # 随机生成语言/国际 信息
print(f.md5())  # 随机生成MD5
print(f.null_boolean())  # NULL/True/False
print(f.password())  # 随机生成密码,可选参数 # length  # 密码长度；special_chars  # 是否能使用特殊字符；digits  # 是否包含数字；upper_case  # 是否包含大写字母；lower_case  # 是否包含小写字母
print(f.sha1())  # 随机SHA1
print(f.sha256())  # 随机SHA256
print(f.uuid4())  # 随机UUID
print(f.first_name())  #
print(f.first_name_female())  # 女性名
print(f.first_name_male())  # 男性名
print(f.first_romanized_name())  # 罗马名
print(f.last_name())  #
print(f.last_name_female())  # 女姓
print(f.last_name_male())  # 男姓
print(f.last_romanized_name())  #
print(f.name())  # 随机生成全名
print(f.name_female())  # 男性全名
print(f.name_male())  # 女性全名
print(f.romanized_name())  # 罗马名
print(f.msisdn())  # 移动台国际用户识别码，即移动用户的ISDN号码
print(f.phone_number())  # 随机生成手机号
print(f.phonenumber_prefix())  # 随机生成手机号段
print(f.profile())  # 随机生成档案信息
print(f.simple_profile())  # 随机生成简单档案信息

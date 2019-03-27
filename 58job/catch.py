import xml.dom.minidom as xmldom
import re

xml_data = [8, '王', '大', '专', '张', '黄', '验', 0, '届', 1,
            '生', 6, 2, '硕', '高', '杨', '陈', '女', '以', 5,
            '科', '周', 7, '士', '本', '应', 9, 4, '中', '刘',
            'A', '吴', '校', '博', '下', 'B', 'M', 'E', 3, '刘',
            '李', '经', '赵', '无', '男', '']

data1 = []
dom1 = xmldom.parse('./1.xml')
elem1_obj = dom1.documentElement
sub1_obj = elem1_obj.getElementsByTagName('TTGlyph')
re_obj = re.compile(r"name=\"(.*)\"")
pts1_data_list = []
for i in range(len(sub1_obj)):
    if sub1_obj[i].getAttribute('name') != '.notdef':
        pts1_list = sub1_obj[i].getElementsByTagName('pt')
        pts1_data_list_list = []
        for j in range(len(pts1_list)):
            x = sub1_obj[i].getElementsByTagName('pt')[j].getAttribute('x')
            y = sub1_obj[i].getElementsByTagName('pt')[j].getAttribute('y')
            on = sub1_obj[i].getElementsByTagName('pt')[j].getAttribute('on')
            pts1_data_list_list.append((x, y, on, sub1_obj[i].getAttribute('name')))
        pts1_data_list.append(pts1_data_list_list)


data2 = []
dom2 = xmldom.parse('./2.xml')
elem2_obj = dom2.documentElement
sub2_obj = elem2_obj.getElementsByTagName('TTGlyph')
pts2_data_list = []
for m in range(len(sub2_obj)):
    if sub2_obj[m].getAttribute('name') != '.notdef':
        pts2_list = sub2_obj[m].getElementsByTagName('pt')
        pts2_data_list_list = []
        for n in range(len(pts2_list)):
            x = sub2_obj[m].getElementsByTagName('pt')[n].getAttribute('x')
            y = sub2_obj[m].getElementsByTagName('pt')[n].getAttribute('y')
            on = sub2_obj[m].getElementsByTagName('pt')[n].getAttribute('on')
            pts2_data_list_list.append((x, y, on, sub2_obj[m].getAttribute('name')))
        pts2_data_list.append(pts2_data_list_list)

for k in pts1_data_list:
    for l in pts2_data_list:
        if len(k) == len(l):
            for a, b in zip(k, l):
                if a[0] == b[0] and a[1] == b[1] and a[2] == b[2]:
                    print(a[3], b[3])
        else:
            continue
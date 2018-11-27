SELECT re.region_name, su.sub_region_name, ca.country_area_name, hs.site_name, hsc.category_name
	FROM heritage_site hs 
		LEFT JOIN heritage_site_jurisdiction hsj
			ON hs.heritage_site_id = hsj.heritage_site_id
		LEFT JOIN country_area ca
			ON hsj.country_area_id = ca.country_area_id
		LEFT JOIN region re
			ON ca.region_id = re.region_id
		LEFT JOIN sub_region su
			ON ca.sub_region_id = su.sub_region_id
		LEFT JOIN heritage_site_category hsc
			ON hs.heritage_site_category_id = hsc.category_id
WHERE ca.country_area_name LIKE 'China%'
ORDER BY re.region_name, su.sub_region_name, ca.country_area_name, hs.site_name;

mysql> SELECT re.region_name, su.sub_region_name, ca.country_area_name, hs.site_name, hsc.category_name
    -> FROM heritage_site hs
    -> LEFT JOIN heritage_site_jurisdiction hsj
    -> ON hs.heritage_site_id = hsj.heritage_site_id
    -> LEFT JOIN country_area ca
    -> ON hsj.country_area_id = ca.country_area_id
    -> LEFT JOIN region re
    -> ON ca.region_id = re.region_id
    -> LEFT JOIN sub_region su
    -> ON ca.sub_region_id = su.sub_region_id
    -> LEFT JOIN heritage_site_category hsc
    -> ON hs.heritage_site_category_id = hsc.category_id
    -> WHERE ca.country_area_name LIKE 'China%'
    -> ORDER BY re.region_name, su.sub_region_name, ca.country_area_name, hs.site_name;
+-------------+-----------------+-------------------+------------------------------------------------------------------------------+---------------+
| region_name | sub_region_name | country_area_name | site_name                                                                    | category_name |
+-------------+-----------------+-------------------+------------------------------------------------------------------------------+---------------+
| Asia        | Eastern Asia    | China             | Ancient Building Complex in the Wudang Mountains                             | Cultural      |
| Asia        | Eastern Asia    | China             | Ancient City of Ping Yao                                                     | Cultural      |
| Asia        | Eastern Asia    | China             | Ancient Villages in Southern Anhui – Xidi and Hongcun                       | Cultural      |
| Asia        | Eastern Asia    | China             | Capital Cities and Tombs of the Ancient Koguryo Kingdom                      | Cultural      |
| Asia        | Eastern Asia    | China             | Chengjiang Fossil Site                                                       | Natural       |
| Asia        | Eastern Asia    | China             | China Danxia                                                                 | Natural       |
| Asia        | Eastern Asia    | China             | Classical Gardens of Suzhou                                                  | Cultural      |
| Asia        | Eastern Asia    | China             | Cultural Landscape of Honghe Hani Rice Terraces                              | Cultural      |
| Asia        | Eastern Asia    | China             | Dazu Rock Carvings                                                           | Cultural      |
| Asia        | Eastern Asia    | China             | Fanjingshan                                                                  | Natural       |
| Asia        | Eastern Asia    | China             | Fujian <em>Tulou</em>                                                        | Cultural      |
| Asia        | Eastern Asia    | China             | Historic Centre of Macao                                                     | Cultural      |
| Asia        | Eastern Asia    | China             | Historic Ensemble of the Potala Palace, Lhasa                                | Cultural      |
| Asia        | Eastern Asia    | China             | Historic Monuments of Dengfeng in “The Centre of Heaven and Earth”         | Cultural      |
| Asia        | Eastern Asia    | China             | Huanglong Scenic and Historic Interest Area                                  | Natural       |
| Asia        | Eastern Asia    | China             | Hubei Shennongjia                                                            | Natural       |
| Asia        | Eastern Asia    | China             | Imperial Palaces of the Ming and Qing Dynasties in Beijing and Shenyang      | Cultural      |
| Asia        | Eastern Asia    | China             | Imperial Tombs of the Ming and Qing Dynasties                                | Cultural      |
| Asia        | Eastern Asia    | China             | Jiuzhaigou Valley Scenic and Historic Interest Area                          | Natural       |
| Asia        | Eastern Asia    | China             | Kaiping Diaolou and Villages                                                 | Cultural      |
| Asia        | Eastern Asia    | China             | Kulangsu, a Historic International Settlement                                | Cultural      |
| Asia        | Eastern Asia    | China             | Longmen Grottoes                                                             | Cultural      |
| Asia        | Eastern Asia    | China             | Lushan National Park                                                         | Cultural      |
| Asia        | Eastern Asia    | China             | Mausoleum of the First Qin Emperor                                           | Cultural      |
| Asia        | Eastern Asia    | China             | Mogao Caves                                                                  | Cultural      |
| Asia        | Eastern Asia    | China             | Mount Emei Scenic Area, including Leshan Giant Buddha Scenic Area            | Mixed         |
| Asia        | Eastern Asia    | China             | Mount Huangshan                                                              | Mixed         |
| Asia        | Eastern Asia    | China             | Mount Qingcheng and the Dujiangyan Irrigation System                         | Cultural      |
| Asia        | Eastern Asia    | China             | Mount Sanqingshan National Park                                              | Natural       |
| Asia        | Eastern Asia    | China             | Mount Taishan                                                                | Mixed         |
| Asia        | Eastern Asia    | China             | Mount Wutai                                                                  | Cultural      |
| Asia        | Eastern Asia    | China             | Mount Wuyi                                                                   | Mixed         |
| Asia        | Eastern Asia    | China             | Mountain Resort and its Outlying Temples, Chengde                            | Cultural      |
| Asia        | Eastern Asia    | China             | Old Town of Lijiang                                                          | Cultural      |
| Asia        | Eastern Asia    | China             | Peking Man Site at Zhoukoudian                                               | Cultural      |
| Asia        | Eastern Asia    | China             | Qinghai Hoh Xil                                                              | Natural       |
| Asia        | Eastern Asia    | China             | Sichuan Giant Panda Sanctuaries - Wolong, Mt Siguniang and Jiajin Mountains  | Natural       |
| Asia        | Eastern Asia    | China             | Silk Roads: the Routes Network of Chang'an-Tianshan Corridor                 | Cultural      |
| Asia        | Eastern Asia    | China             | Site of Xanadu                                                               | Cultural      |
| Asia        | Eastern Asia    | China             | South China Karst                                                            | Natural       |
| Asia        | Eastern Asia    | China             | Summer Palace, an Imperial Garden in Beijing                                 | Cultural      |
| Asia        | Eastern Asia    | China             | Temple and Cemetery of Confucius and the Kong Family Mansion in Qufu         | Cultural      |
| Asia        | Eastern Asia    | China             | Temple of Heaven: an Imperial Sacrificial Altar in Beijing                   | Cultural      |
| Asia        | Eastern Asia    | China             | The Grand Canal                                                              | Cultural      |
| Asia        | Eastern Asia    | China             | The Great Wall                                                               | Cultural      |
| Asia        | Eastern Asia    | China             | Three Parallel Rivers of Yunnan Protected Areas                              | Natural       |
| Asia        | Eastern Asia    | China             | Tusi Sites                                                                   | Cultural      |
| Asia        | Eastern Asia    | China             | West Lake Cultural Landscape of Hangzhou                                     | Cultural      |
| Asia        | Eastern Asia    | China             | Wulingyuan Scenic and Historic Interest Area                                 | Natural       |
| Asia        | Eastern Asia    | China             | Xinjiang Tianshan                                                            | Natural       |
| Asia        | Eastern Asia    | China             | Yin Xu                                                                       | Cultural      |
| Asia        | Eastern Asia    | China             | Yungang Grottoes                                                             | Cultural      |
| Asia        | Eastern Asia    | China             | Zuojiang Huashan Rock Art Cultural Landscape                                 | Cultural      |
+-------------+-----------------+-------------------+------------------------------------------------------------------------------+---------------+
53 rows in set (0.00 sec)

hs = HeritageSite.objects.select_related('heritage_site_category').filter(country_area__country_area_name__startswith = 'China').values_list('country_area__region__region_name', 'country_area__sub_region__sub_region_name', 'country_area__country_area_name', 'site_name', 'heritage_site_category__category_name')

hs = HeritageSite.objects.select_related('country_area__region__region_name', 'country_area__sub_region__sub_region_name', 'country_area__country_area_name', 'heritage_site_category__category_name').filter(country_area__country_area_name__startswith = 'China').values_list('country_area__region__region_name', 'country_area__sub_region__sub_region_name', 'country_area__country_area_name', 'site_name', 'heritage_site_category__category_name')

>>> hs = HeritageSite.objects.select_related('country_area__region__region_name', 'country_area__sub_region__sub_region_name', 'country_area__country_area_name', 'heritage_site_category__category_name').filter(country_area__country_area_name__startswith = 'China').values_list('country_area__region__region_name', 'country_area__sub_region__sub_region_name', 'country_area__country_area_name', 'site_name', 'heritage_site_category__category_name')
>>> for i in hs: print(i)
...
('Asia', 'Eastern Asia', 'China', 'Ancient Building Complex in the Wudang Mountains', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Ancient City of Ping Yao', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Ancient Villages in Southern Anhui – Xidi and Hongcun', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Capital Cities and Tombs of the Ancient Koguryo Kingdom', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Chengjiang Fossil Site', 'Natural')
('Asia', 'Eastern Asia', 'China', 'China Danxia', 'Natural')
('Asia', 'Eastern Asia', 'China', 'Classical Gardens of Suzhou', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Cultural Landscape of Honghe Hani Rice Terraces ', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Dazu Rock Carvings', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Fanjingshan', 'Natural')
('Asia', 'Eastern Asia', 'China', 'Fujian <em>Tulou</em>', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Historic Centre of Macao', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Historic Ensemble of the Potala Palace, Lhasa', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Historic Monuments of Dengfeng in “The Centre of Heaven and Earth”', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Huanglong Scenic and Historic Interest Area', 'Natural')
('Asia', 'Eastern Asia', 'China', 'Hubei Shennongjia', 'Natural')
('Asia', 'Eastern Asia', 'China', 'Imperial Palaces of the Ming and Qing Dynasties in Beijing and Shenyang', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Imperial Tombs of the Ming and Qing Dynasties', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Jiuzhaigou Valley Scenic and Historic Interest Area', 'Natural')
('Asia', 'Eastern Asia', 'China', 'Kaiping Diaolou and Villages', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Kulangsu, a Historic International Settlement', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Longmen Grottoes', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Lushan National Park', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Mausoleum of the First Qin Emperor', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Mogao Caves', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Mount Emei Scenic Area, including Leshan Giant Buddha Scenic Area', 'Mixed')
('Asia', 'Eastern Asia', 'China', 'Mount Huangshan', 'Mixed')
('Asia', 'Eastern Asia', 'China', 'Mount Qingcheng and the Dujiangyan Irrigation System', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Mount Sanqingshan National Park', 'Natural')
('Asia', 'Eastern Asia', 'China', 'Mount Taishan', 'Mixed')
('Asia', 'Eastern Asia', 'China', 'Mount Wutai', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Mount Wuyi', 'Mixed')
('Asia', 'Eastern Asia', 'China', 'Mountain Resort and its Outlying Temples, Chengde', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Old Town of Lijiang', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Peking Man Site at Zhoukoudian', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Qinghai Hoh Xil', 'Natural')
('Asia', 'Eastern Asia', 'China', 'Sichuan Giant Panda Sanctuaries - Wolong, Mt Siguniang and Jiajin Mountains ', 'Natural')
('Asia', 'Eastern Asia', 'China', "Silk Roads: the Routes Network of Chang'an-Tianshan Corridor", 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Site of Xanadu', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'South China Karst', 'Natural')
('Asia', 'Eastern Asia', 'China', 'Summer Palace, an Imperial Garden in Beijing', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Temple and Cemetery of Confucius and the Kong Family Mansion in Qufu', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Temple of Heaven: an Imperial Sacrificial Altar in Beijing', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'The Grand Canal', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'The Great Wall', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Three Parallel Rivers of Yunnan Protected Areas', 'Natural')
('Asia', 'Eastern Asia', 'China', 'Tusi Sites', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'West Lake Cultural Landscape of Hangzhou', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Wulingyuan Scenic and Historic Interest Area', 'Natural')
('Asia', 'Eastern Asia', 'China', 'Xinjiang Tianshan', 'Natural')
('Asia', 'Eastern Asia', 'China', 'Yin Xu', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Yungang Grottoes', 'Cultural')
('Asia', 'Eastern Asia', 'China', 'Zuojiang Huashan Rock Art Cultural Landscape', 'Cultural')
import re
import os
import json

data_dir  = './data/processed_manual_talkop_vivre_card'
file_name = '4-（201908杰尔马66+大妈团）'
suffix    = '.txt'
vivre_card_path = os.path.join(data_dir, file_name + suffix)


# define some regex pattern
chapter_regex = '【篇章标识符】.(.*)'
chapter_pattern = re.compile(chapter_regex, re.S)

name_regex = '【([^/]*)/*(.*)】'
name_pattern = re.compile(name_regex, re.S)

chapter_split_regex = '([^/]+)'
chapter_split_pattern = re.compile(chapter_split_regex, re.S)

avpair_regex = '(.*?)[:：](.*)'
avpair_pattern = re.compile(avpair_regex, re.S)

reward_regex = '【悬赏金】(.*)'
reward_pattern = re.compile(reward_regex, re.S)

# 名言
quotes_regex = '^“(.*)”$'
quotes_pattern = re.compile(quotes_regex, re.S)


with open(vivre_card_path) as f:
    content = f.readlines()


# remove \n\t by strip() & remove empty line
vivre_card_list = []
for item in content:
    item = item.strip()

    if len(item) != 0:
        vivre_card_list.append(item)
        print(item)


# get onepiece entities name
entities_cnt          = 0
entities_id_list      = []
entities_mention_list = []
for idx, item in enumerate(vivre_card_list):
    # 每个entities项开头和结尾都是数字
    # 并且它的下一项是带【】，里面有名字的项目
    # e.g. 
    #   0004
    #   【乌索普/Usopp】
    if item[0].isdigit() and item[-1].isdigit():
        next_item = vivre_card_list[idx + 1]
        if next_item.startswith('【') and next_item.endswith('】'):
            entities_id_list.append(item)
            entities_mention_list.append(next_item)

            print(item, next_item)
            entities_cnt += 1


print('\n\nOnepiece Entities Number: {}\n\n'.format(entities_cnt))


write_file_name = os.path.join(data_dir, 'preprocessed-' + file_name + suffix)
f = open(write_file_name, 'w')


idx = 0
entities_idx = 0

entities_avpair_results_dict = dict() # 所有entities的avpair结果
entities_id_name_list        = list() # 记录所有解析得到entities的id和对应的mention_name
entity_avpair_list           = list() # 单个entities
entity_avpair_dict           = dict()
predicate_set                = set()  # 所有不同的predicate，也就是avpair的key
while idx < len(content):
    
    item = content[idx].strip()

    write_item = item
    print(1, write_item)
    f.write(write_item + '\n')


    if entities_idx >= len(entities_id_list):
        idx += 1

    elif item == entities_id_list[entities_idx]:
        print('---------------------------------------')
        entity_id           = item
        entity_mention_name = content[idx + 1].strip().strip('【】')
        entity_english_name = content[idx + 2].strip()

        if entity_english_name[0].encode('UTF-8').isalpha() and entity_english_name[-1].encode('UTF-8').isalpha():

            print('entity_english_name: {}'.format(entity_english_name))

            # write_item = entity_id
            # print(2, write_item)
            # f.write(write_item + '\n')

            write_item = '【{}/{}】'.format(entity_mention_name, entity_english_name)
            print(3, write_item)
            f.write(write_item + '\n')

            idx          += 3
            entities_idx += 1
            next_item     = content[idx].strip()

        else:
            # write_item = entity_id
            # print(4, write_item)
            # f.write(write_item + '\n')

            write_item = '【{}】'.format(entity_mention_name)
            print(5, write_item)
            f.write(write_item + '\n')

            idx          += 2
            entities_idx += 1
            next_item     = content[idx].strip()



        # 处理最后一个的特殊情况
        if entities_idx == len(entities_id_list):
            while idx < len(vivre_card_list):
                next_item = content[idx].strip()

                if '登场篇章' in next_item and '【' not in content[idx + 1]:
                    # print(6, next_item.strip().strip('【】') + '：' + content[idx + 1].strip())
                    write_item = next_item.strip().strip('【】') + '：' + content[idx + 1].strip()
                    print(6, write_item)
                    f.write(write_item + '\n')
                    idx += 2
                elif '个路飞' in next_item:
                    # print(7, '【' + next_item.strip().strip('【】') + ' ' + content[idx + 1].strip() + '】')
                    write_item = '【' + next_item.strip().strip('【】') + ' ' + content[idx + 1].strip() + '】'
                    print(7, write_item)
                    f.write(write_item + '\n')
                    idx += 2
                else:
                    # print(8, next_item.strip())
                    write_item = next_item.strip()
                    print(8, write_item)
                    f.write(write_item + '\n')
                    idx += 1
        else:
            while next_item != entities_id_list[entities_idx] and idx < len(content) and '【篇章标识符】' not in next_item:
                if '登场篇章' in next_item and '【' not in content[idx + 1]:
                    # print(9, next_item.strip().strip('【】') + '：' + content[idx + 1].strip())
                    write_item = next_item.strip().strip('【】') + '：' + content[idx + 1].strip()
                    print(9, write_item)
                    f.write(write_item + '\n')
                    idx += 2
                    next_item = content[idx].strip()
                elif '个路飞' in next_item:
                    # print(10, '【' + next_item.strip().strip('【】') + ' ' + content[idx + 1].strip() + '】')
                    write_item = '【' + next_item.strip().strip('【】') + ' ' + content[idx + 1].strip() + '】'
                    print(10, write_item)
                    f.write(write_item + '\n')
                    idx += 2
                    next_item = content[idx].strip()
                else:
                    # print(11, next_item.strip())
                    write_item = next_item.strip()
                    # print(11, write_item)
                    f.write(write_item + '\n')
                    idx += 1
                    next_item = content[idx].strip()
    

    else:
        idx += 1


f.close()

exit(-1)
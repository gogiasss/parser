import collections

#в кавычках имя файла в котором считаем
with open('hashtags.txt', encoding='utf-8') as f:
    content = f.readlines()

content = [x.strip() for x in content]

c = collections.Counter()


for word in content:
    c[word] += 1
#имя файла для записи результата

my_file = open('result.txt', 'w')
my_file2 = open('tag.txt', 'w', encoding='utf-8')


for key, value in c.items():
    if value >= 5: #пороговое значение
        res = str((key,value))
        res2 = str(key)
        res = res[:-1]
        res = res[1:]
        res = res.replace("'",'')
        res = res.replace(",",':')
        res = res.replace(" ",'')
        my_file.write(res+'\n')
        my_file2.write(res2+'\n')
my_file.close()
my_file2.close()

input('Нажмите любую клавишу ')

        




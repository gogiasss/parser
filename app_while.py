import requests
from datetime import datetime
from time import sleep
from apikey import key, url_result, tags_file, tasks_file, result_file

work_parts = 0
part_list = None 
hashtag_list = []

#--- добавление заданий в очередь
def get_add(hashtag):
    name = str(datetime.now())
    p = {'key': key, 'mode': 'create', 'type': 'p3', 'name':name, 'links': hashtag,\
         'act':'7', 'web':'1', 'limit':'1', 'limit2':'1'}
    res_json = requests.get(url_result, params = p).json()

    #input('Enter')
    
    taskid = res_json['tid']
    
    if taskid == 'limit3':
        print('Максимальное количество заданий для текущего тарифа')
    elif taskid == 'limit5':
        print('Максимальное количество заданий в очереди')
    elif taskid == 'limit1_1':
        print('Максимальное количество логинов,хэштегов,id')
    elif taskid == 'limit1':
        print('В задании слишком много позиций')
    else:
        print('Задание №'+taskid+' помещено в очередь')
        with open(tasks_file, 'w') as f:
            f.write(str(taskid)+',')
            print('Запись файла '+tasks_file+' прошла успешно')


#--- получение результата 
def get_result(taskid):
    p = {'key': key, 'mode': 'result', 'tid': taskid}
    res = requests.get(url_result, params = p)
    with open(result_file, 'a', encoding='utf-8') as f:
            f.write(res.text+'\n')

#--- получение статуса задания
def get_status(taskid):
    p = {'key': key, 'mode': 'status', 'tid': taskid}
 
    
    while True:
        data = requests.get(url_result, params = p).json()
        if 'in progress' in data.values():
            print('Цикл заданий еще в работе. Ждем 12 минут')

            sleep(720) #время задержки в секундах
         
            continue
        else:
            if 'completed' in data.values():
                print('Задание '+taskid+' завершено. Дописываю данные в файл '+result_file)
                with open(tasks_file, 'r') as f:
                    for line in f:
                        if len(line) >= 7:
                            line = line.split(',')
                            get_result(i)
                        else:
                            get_result(line)
            break

    
#--- Делим файл на части
def split_list(alist, parts=1):
    length = len(alist)
    return [ alist[i*length // parts: (i+1)*length // parts] 
             for i in range(parts) ]
def sp_part(part=1):
    if len(hashtag_list) <= 100:
        part = 1
        return part
    elif len(hashtag_list) >= 100:
        part = (len(hashtag_list) // 100) + 1
        return part



#--- Открываем файл с тэгами
with open('tag.txt', 'r', encoding='utf-8') as f:
    for line in f:
        string = line.replace('\n','')
        hashtag_list.append(string)

    
part_list = sp_part()

        
new_list = split_list(hashtag_list, part_list)

print(f'Число хештегов в файле tag.txt - {len(hashtag_list)}, количество циклов - {part_list}')


input('')

#начинаем цикл
while work_parts <= part_list - 1:
    hashtag = new_list[work_parts]
    hashtag = ",".join(hashtag)
    lh = str(len(hashtag))
    print('Общий размер всех хэштегов '+lh+' символов')
    try:
        get_add(hashtag)
    except ValueError as er:
        print('Некорректный ответ от сервиса', er)
    except Exception as er:
        print('Неизвестная ошибка', er)
    else:
        print('...')


    print('Запрашиваем статусы')    
    with open(tasks_file, 'r') as f:
        for line in f:
            if len(line) >= 7:
                line = line.split(',')
                for i in line:
                        get_status(i)
                        sleep(4)                    
            else:
                get_status(line)
    print('Цикл завершен')            
    work_parts += 1

    

else:
    print('')
    print('')
    print('Закончил работу')
    
    
     

#imports
import vk_api
from vk_api import bot_longpoll
import random
import pymysql
#offsets
global connect 
global vk 
global users 
global boolean
global pid
global countrees
token = input('Токен: ')
connect = vk_api.VkApi(token=token)
vk = connect.get_api()
users = {}
boolean = False
countrees = ['', '🇸🇦 Саудовская Аравия', '🇦🇫 Афганистан', '🇧🇩 Бангладеш', '🇧🇹 Бутан', '🇮🇳 Индия', '🇳🇵 Непал', '🇵🇰 Пакистан', '🇱🇰 Шри-Ланка' ]
    
def send(text, uid):
    vk.messages.send(random_id = random.randint(0, 100), message = text, peer_id = uid)
    
def save(users):
    f1le = open('users.txt', 'w')
    users = str(users)
    f1le.write(users)
    f1le.close()

def ware(first, secund, pid, users):
    try:
        secund = secund[3 : 12]
        cfirst = users[first]
        csecund = users[int(secund)]
        text = countrees[cfirst] + ' vs ' + countrees[csecund]
        send(text, pid)
        resule = random.randint(1, 2)
        if resule == 1:
            text = countrees[cfirst] + ' победил!'
            users.pop(int(secund))
            send(text, pid)
        if resule ==2:
            text = countrees[csecund]+ ' победил!'
            users.pop(first)
            send(text, pid)
        return(users)


    except:
        send('данный человек не участвует в игре или не имеет страны!', pid)
        return(users)
        

def load():
    try:
        f1le = open('users.txt', 'r')
        userssrt = f1le.read()
        users = eval(userssrt)
        return(users)
    except:
        return({})

def logic(text, users, uid):
    boolean = False
    rtext = '' 
    rezerved = list(users.values())
    if text == '!Начать' or text == '!начать':
        if users[uid] == 'st0':
            rtext = 'Выберите страну\n1.'+countrees[1]+'\n2.'+countrees[2]+'\n3.'+countrees[3]+'\n4.'+countrees[4]+'\n5.'+countrees[5]+'\n6.'+countrees[6]+'\n7.'+countrees[7]+'\n8.'+countrees[8]
            users[uid]='st1' 
        else:
            rtext = 'У вас уже есть старана!'
    elif users[uid] == 'st1':
        if text == '1' and bool(1 in rezerved) == False or text == 'Саудовская Аравия' and  bool(1 in rezerved) == False :
            users[uid] = 1
            rtext = 'Выбрана '+countrees[1]
        elif text == '3' and bool(3 in rezerved) == False or text == 'Бангладеш' and bool(3 in rezerved) == False:
            users[uid] = 3
            rtext = 'Выбран '+countrees[3]
        elif text == '2' and bool(2 in rezerved) == False or text == 'Aфганистан' and bool(2 in rezerved) == False:
            users[uid] = 2
            rtext = 'Выбран '+countrees[2]
        elif text == '4' and bool(4 in rezerved) == False or text == 'Бутан' and bool(4 in rezerved) == False:
            users[uid] = 4
            rtext = 'Выбран ' + countrees[4]
        elif text == '5' and bool(5 in rezerved) == False or text == 'Индия' and bool(5 in rezerved) == False:
            users[uid] = 5
            rtext = 'Выбрана ' + countrees[5]
        elif text == '6' and bool(6 in rezerved) == False or text == 'Непал' and bool(6 in rezerved) == False:
            users[uid] = 6
            rtext = 'Выбран ' + countrees[6]
        elif text == '7' and bool(7 in rezerved) == False or text == 'Пакистан' and bool(7 in rezerved) == False:
            users[uid] = 7
            rtext = 'Выбран ' + countrees[7]
        elif text == '8' and bool(8 in rezerved) == False or text == 'Шри-Ланка' and bool(8 in rezerved) == False:
            users[uid] = 8
            rtext = 'Выбрана ' + countrees[8]
        else:
            rtext = 'Страна занята'
    if text == '!Война' or text == '!война' and users[uid] != 'st1' and users[uid] != 'st0':
        rtext = 'Кому Вы желаете объявить войну?'
        boolean = True
    if text == '!Команды' or text == '!команды':
        rtext = 'Доступные команды:\n !Начать\n !Война\n !Статистика(В разработке)\n'
    if text[0] == '!' and rtext == '':
        rtext = 'Неправильная команда!'
    return(rtext, users, boolean)

def sysemauth(uid):
    try:
        users[uid]
    except:
        users[uid] = 'st0'
    return users

#работа лонгпол
def main():
    boolean = False
    gid = input('Id группы')
    longpo11 = bot_longpoll.VkBotLongPoll(vk=connect, group_id=gid, wait = 1)
    for event in longpo11.listen():
        print('___EVENT___')
        if event.raw['type'] == 'message_new':
            text = event.obj.text
            pid = event.obj.peer_id
            uid = event.obj.from_id
            users = sysemauth(uid)
            if boolean == True:
                users = ware(uid, text, pid, users)
            text, users, boolean = logic(text, users, uid )
            if text != '':
                send(text, pid)

users = load()          
try:
    main()
except:
    save(users)
    exit()

import tkinter as tk
from tkinter import  font
import random
import sys
import json

#вспомогательный метод 1
def morethan(i):
    if i>=15:
        return(i+1)
    else:
        return(i)
    
#вспомогательный метод 2
def correct(n):
    if n%10 == 1 and n%100!=11:
        return ' место'
    elif n%10 >=2 and n%10<=4 and (n%100)//10 !=1:
        return ' места'
    else:
        return ' мест'
    
#вспомогательный метод 3
def correctirovka(q):
    if q == 0:
        return 'Вы ничего не выбрали :-('
    elif q == 1:
        return 'Ваше место:'
    else:
        return 'Ваши места:'


try:
    with open("guesty.json","r") as file:
        tb = json.load(file)
except:
    tb = {}
    for k in ['A','B']:
        for i in range(1,6):
            for j in range(25):
                tb[k+str(100*i+j)] = -1
    with open("guesty.json", "w") as write_file:
        json.dump(tb, write_file, ensure_ascii=False, indent='\t')
    with open("guesty.json","r") as file:
        tb = json.load(file)


zanyato = []
zanyato_guests = set()

for key in tb:
    if tb[key]!= -1:
        zanyato.append(key)
        zanyato_guests.add(tb[key])
        
d_help = set(i for i in range (10000000))
d_help -= zanyato_guests


print('Добрый день!')
print('''
Если Вы хотите приобрести билеты впервые, нажмите 1
Если Вы хотите изменить ранее поданную заявку, нажмите 2
Если Вы хотите отменить всё бронирование, нажмите 3
''')
while (choice := int(input())) not in [1,2,3] :
    print('Прочитайте инструкцию внимательнее')

if choice == 3:
    n = 3
    print('Напишите Ваш ID')
    ID = int(input())
    while (ID not in zanyato_guests):
        n -= 1
        print('Неверный ID, у вас осталось'+ ' '+ str(n)+ ' '+ (n-2)*n*(-1)*'попытка'+((n-2)*(n-1)-1)*'попыток'+(n*(n-1)-1)*'попытки')
        if n <= 0:
            print('Такого ID не существует. Вы пытаетесь обмануть Департамент спорта г.Москвы.')
            sys.exit()
        ID = int(input())
    for key in tb:
        if tb[key] == ID:
            tb[key] = -1
        with open("guesty.json", "w") as write_file:
            json.dump(tb, write_file, ensure_ascii=False, indent='\t')
    print('Ваше бронирование отменено')
    
elif choice == 1:
    print('Выберите места. После завершения выбора, нажмите кнопку "Завершить". Серым отмечены места, занятые другими людьми')
    q = 0
    zanyato_person = set()
    
    #функция, регулирующая работу одного места
    def switch(event,button):
    #работаем с счетчиком
        global q, zanyato_person
        if button['state'] == 'normal' and button['bg']!='green':
            q+=1
            zanyato_person.add(button['text'])
            #видоизменяем стадион
            button['fg'] = 'dark blue'
            button['bg'] = 'green'
            
        elif button['bg']=='green':
            q-=1
            zanyato_person.remove(button['text'])
            button['fg'] = 'white'
            button['bg'] = '#409fff'
            
    #функция завершения работы графического интерфейса
    def delete(event,button):
        window.destroy()
        global q,zanyato_person
        print('Вы забронировали '+str(q)+correct(q))
        if q!= 0:
            zanyato_person1 = list(zanyato_person)
            zanyato_person1.sort()
            zanyato_person1_copy = zanyato_person1.copy()
            zanyato_person1[0] = correctirovka(q)+' '+zanyato_person1[0]
            print(*zanyato_person1,sep = ',')
            
            ID = random.choice(list(d_help))
            print('Ваш ID =',str(ID))
            for i in (zanyato_person1_copy):
                tb[i] = ID
            with open("guesty.json", "w") as write_file:
                json.dump(tb, write_file, ensure_ascii=False, indent='\t')

    window = tk.Tk()
    window.title('Арена Чертаново')

    font1 = font.Font(family= "Arial", size=11, weight="bold")

    #северная трибуна
    frame = tk.Frame(master=window,borderwidth=1)
    frame.grid(row=0,padx = (0,40), column=15)
    label = tk.Label(master = frame,text = 'Северная трибуна',height = 3,width = 15, fg = 'black', font = font1 )
    label.pack()

    for i in range(1,6):
        for j in range(0,30):
            if i == 1 and j!=0 and (j+1)%5!=0:
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i, column=morethan(j),padx = (0,1), pady = (30,5))
                button = tk.Button(master=frame, text=f"A{(6-i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                #не выдаем места, которые уже заняты
                if button['text'] in zanyato:
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack() 
            #делаем отступ вначале
            elif i!=1 and j == 0:
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i, column=morethan(j),padx = (40,1), pady = (5))
                button = tk.Button(master=frame, text=f"A{(6-i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                #не выдаем места, которые уже заняты
                if button['text'] in zanyato:
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()
            
            elif i == 1 and j==0:
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i, column=morethan(j),padx = (40,1), pady = (30,5))
                button = tk.Button(master=frame, text=f"A{(6-i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                #не выдаем места, которые уже заняты
                if button['text'] in zanyato:
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()

            elif i == 1 and ((j+1)%5==0):
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i, column=morethan(j),padx = (0,40), pady = (30,5))
                button = tk.Button(master=frame, text=f"A{(6-i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                #не выдаем места, которые уже заняты
                if button['text'] in zanyato:
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()
                
            #если у нас обычное место (не у прохода и не снизу)
            elif ((j+1)%5 != 0):
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i, column=morethan(j),padx = (0,1), pady = 5)
                button = tk.Button(master=frame, text=f"A{(6-i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                if button['text'] in zanyato:
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()
            
            #место у прохода
            else:
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i, column=morethan(j),padx = (0,40), pady = 5)
                button = tk.Button(master=frame, text=f"A{(6-i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                if button['text'] in zanyato:
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()



    frame = tk.Frame(master=window,borderwidth=1)
    frame.grid(row=6, column=15,padx = (0,40), pady = (90,45))
    button = tk.Button(master=frame, text=f"Завершить работу", height = 2, width = 15,bg = 'red', fg = 'white')
    button.pack()
    button.bind("<Button-1>", lambda event, button=button: delete(event, button))


    #южная трибуна

    frame = tk.Frame(master=window,borderwidth=1)
    frame.grid(row=12,padx = (0,40), pady= (25,0), column=15)
    label = tk.Label(master = frame,text = 'Южная трибуна',height = 3,width = 15,fg = 'black',font = font1 )
    label.pack()

    for i in range(1,6):
        for j in range(0,30):

            #cделаем отступ между трибунами
            if j == 0 and i!=1:
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i+6, column=j,padx = (40,1), pady = 5)
                button = tk.Button(master=frame, text=f"B{(i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                if button['text'] in zanyato:
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()

            elif i == 1 and j == 0:
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i+6, column=j,padx = (40,1), pady = (60,5))
                button = tk.Button(master=frame, text=f"B{(i)*100+j}", height = 1, width = 3 , bg = '#409fff', fg = 'white')
                if button['text'] in zanyato:
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                
                button.pack()

            elif i == 1 and j!= 0 and ((j+1)%5!=0):
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i+6, column=morethan(j),padx = (0,1), pady = (60,5))
                button = tk.Button(master=frame, text=f"B{(i)*100+j}", height = 1, width = 3, bg = '#409fff',  fg = 'white' )
                if button['text'] in zanyato:
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()

            elif i == 1 and ((j+1)%5==0):
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i+6, column=morethan(j),padx = (0,40), pady = (60,5))
                button = tk.Button(master=frame, text=f"B{(i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                if button['text'] in zanyato:
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()
            
            elif (j+1)%5 != 0:
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i+6, column=morethan(j),padx = (0,1), pady = 5)
                button = tk.Button(master=frame, text=f"B{(i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                if button['text'] in zanyato:
                    button['state'] ='disabled'
                    button['fg'] = 'grey'
                    button['bg'] = 'grey'
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()


            else:
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i+6, column=morethan(j),padx = (0,40), pady = 5)
                button = tk.Button(master=frame, text=f"B{(i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                if button['text'] in zanyato:
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()


    window.mainloop()

elif choice == 2:
    n = 3
    print('Напишите Ваш ID')
    ID = int(input())
    while (ID not in zanyato_guests):
        n -= 1
        print('Неверный ID, у вас осталось'+ ' '+ str(n)+ ' '+ (n-2)*n*(-1)*'попытка'+((n-2)*(n-1)-1)*'попыток'+(n*(n-1)-1)*'попытки')
        if n <= 0:
            print('Такого ID не существует. Вы пытаетесь обмануть Департамент спорта г.Москвы.')
            sys.exit()
        ID = int(input())

    person_booked = []
    
    for key in tb:
        if tb[key] == ID:
            person_booked.append(key)
    
    print('Выберите места. После завершения выбора, нажмите кнопку "Завершить". Зелёным отмечены ранее выбранные вами места, серым - занятыми другими людьми')
    
    q=0
    #функция, регулирующая работу одного места
    def switch(event,button):
    #работаем с счетчиком
        global tb,q
        if button['bg'] == 'green':
            button['fg'] = 'white'
            button['bg'] = '#409fff'
            tb[button['text']] = -1
            q-=1
        elif button['state'] == 'normal':
            button['fg'] = 'dark blue'
            button['bg'] = 'green'
            tb[button['text']] = ID
            q+=1

    #функция завершения работы графического интерфейса
    def delete(event,button):
        window.destroy()
        global q,tb
        print('Вы забронировали '+str(q)+correct(q))

        
        if q!= 0:
            person_places = []
            for key in tb:
                if tb[key] == ID:
                    person_places.append(key)
                    
            person_places.sort()
            person_places[0] = correctirovka(q)+' '+person_places[0]
            print(*person_places,sep = ',')

            with open("guesty.json", "w") as write_file:
                json.dump(tb, write_file, ensure_ascii=False, indent='\t')

    window = tk.Tk()
    window.title('Арена Чертаново')

    font1 = font.Font(family= "Arial", size=11, weight="bold")

    #северная трибуна
    frame = tk.Frame(master=window,borderwidth=1)
    frame.grid(row=0,padx = (0,40), column=15)
    label = tk.Label(master = frame,text = 'Северная трибуна',height = 3,width = 15, fg = 'black', font = font1 )
    label.pack()

    for i in range(1,6):
        for j in range(0,30):
            if i == 1 and j!=0 and (j+1)%5!=0:
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i, column=morethan(j),padx = (0,1), pady = (30,5))
                button = tk.Button(master=frame, text=f"A{(6-i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                #не выдаем места, которые уже заняты
                if (button['text'] in zanyato) and (button['text'] not in person_booked):
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                elif (button['text'] in person_booked):
                    button['fg'] ='dark blue'
                    button['bg'] ='green'
                    q+=1
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()
                
            #делаем отступ вначале
            elif i!=1 and j == 0:
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i, column=morethan(j),padx = (40,1), pady = (5))
                button = tk.Button(master=frame, text=f"A{(6-i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                #не выдаем места, которые уже заняты
                if (button['text'] in zanyato) and (button['text'] not in person_booked):
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                elif (button['text'] in person_booked):
                    button['fg'] ='dark blue'
                    button['bg'] ='green'
                    q+=1
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()
            
            elif i == 1 and j==0:
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i, column=morethan(j),padx = (40,1), pady = (30,5))
                button = tk.Button(master=frame, text=f"A{(6-i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                #не выдаем места, которые уже заняты
                if (button['text'] in zanyato) and (button['text'] not in person_booked):
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                elif (button['text'] in person_booked):
                    button['fg'] ='dark blue'
                    button['bg'] ='green'
                    q+=1
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()

            elif i == 1 and ((j+1)%5==0):
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i, column=morethan(j),padx = (0,40), pady = (30,5))
                button = tk.Button(master=frame, text=f"A{(6-i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                #не выдаем места, которые уже заняты
                if button['text'] in zanyato:
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                elif (button['text'] in person_booked):
                    button['fg'] ='dark blue'
                    button['bg'] ='green'
                    q+=1
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()
                
            #если у нас обычное место (не у прохода и не снизу)
            elif ((j+1)%5 != 0):
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i, column=morethan(j),padx = (0,1), pady = 5)
                button = tk.Button(master=frame, text=f"A{(6-i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                if (button['text'] in zanyato) and (button['text'] not in person_booked):
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                elif (button['text'] in person_booked):
                    button['fg'] ='dark blue'
                    button['bg'] ='green'
                    q+=1
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()
            
            #место у прохода
            else:
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i, column=morethan(j),padx = (0,40), pady = 5)
                button = tk.Button(master=frame, text=f"A{(6-i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                if (button['text'] in zanyato) and (button['text'] not in person_booked):
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                elif (button['text'] in person_booked):
                    button['fg'] ='dark blue'
                    button['bg'] ='green'
                    q+=1
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()



    frame = tk.Frame(master=window,borderwidth=1)
    frame.grid(row=6, column=15,padx = (0,40), pady = (90,45))
    button = tk.Button(master=frame, text=f"Завершить работу", height = 2, width = 15,bg = 'red', fg = 'white')
    button.pack()
    button.bind("<Button-1>", lambda event, button=button: delete(event, button))


    #южная трибуна

    frame = tk.Frame(master=window,borderwidth=1)
    frame.grid(row=12,padx = (0,40), pady= (25,0), column=15)
    label = tk.Label(master = frame,text = 'Южная трибуна',height = 3,width = 15,fg = 'black',font = font1 )
    label.pack()

    for i in range(1,6):
        for j in range(0,30):

            #cделаем отступ между трибунами
            if j == 0 and i!=1:
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i+6, column=j,padx = (40,1), pady = 5)
                button = tk.Button(master=frame, text=f"B{(i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                if (button['text'] in zanyato) and (button['text'] not in person_booked):
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                elif (button['text'] in person_booked):
                    button['fg'] ='dark blue'
                    button['bg'] ='green'
                    q+=1
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()

            elif i == 1 and j == 0:
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i+6, column=j,padx = (40,1), pady = (60,5))
                button = tk.Button(master=frame, text=f"B{(i)*100+j}", height = 1, width = 3 , bg = '#409fff', fg = 'white')
                if (button['text'] in zanyato) and (button['text'] not in person_booked):
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                elif (button['text'] in person_booked):
                    button['fg'] ='dark blue'
                    button['bg'] ='green'
                    q+=1
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                
                button.pack()

            elif i == 1 and j!= 0 and ((j+1)%5!=0):
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i+6, column=morethan(j),padx = (0,1), pady = (60,5))
                button = tk.Button(master=frame, text=f"B{(i)*100+j}", height = 1, width = 3, bg = '#409fff',  fg = 'white' )
                if (button['text'] in zanyato) and (button['text'] not in person_booked):
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                elif (button['text'] in person_booked):
                    button['fg'] ='dark blue'
                    button['bg'] ='green'
                    q+=1
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()

            elif i == 1 and ((j+1)%5==0):
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i+6, column=morethan(j),padx = (0,40), pady = (60,5))
                button = tk.Button(master=frame, text=f"B{(i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                if (button['text'] in zanyato) and (button['text'] not in person_booked):
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                elif (button['text'] in person_booked):
                    button['fg'] ='dark blue'
                    button['bg'] ='green'
                    q+=1
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()
            
            elif (j+1)%5 != 0:
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i+6, column=morethan(j),padx = (0,1), pady = 5)
                button = tk.Button(master=frame, text=f"B{(i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                if (button['text'] in zanyato) and (button['text'] not in person_booked):
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                elif (button['text'] in person_booked):
                    button['fg'] ='dark blue'
                    button['bg'] ='green'
                    q+=1
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()


            else:
                frame = tk.Frame(master=window,borderwidth=1)
                frame.grid(row=i+6, column=morethan(j),padx = (0,40), pady = 5)
                button = tk.Button(master=frame, text=f"B{(i)*100+j}", height = 1, width = 3, bg = '#409fff', fg = 'white')
                if (button['text'] in zanyato) and (button['text'] not in person_booked):
                    button['state'] ='disabled'
                    button['fg'] ='grey'
                    button['bg'] ='grey'
                elif (button['text'] in person_booked):
                    button['fg'] ='dark blue'
                    button['bg'] ='green'
                    q+=1
                button.bind("<Button-1>", lambda event, button=button: switch(event, button))
                button.pack()


    window.mainloop()

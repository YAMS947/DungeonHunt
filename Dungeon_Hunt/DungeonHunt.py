import random, json, os, sys
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def init_():
    global data, dungeons, objects, shopItems, forge

    jsonPath = resource_path("Data.json")
    with open(jsonPath, "r", encoding="utf-8") as f:
        data = json.load(f)

    dungeons = data["dungeons"]
    objects = data["objects"]
    shopItems = data["shop"]
    forge = data["forge"]

def choise_():
     while True:
        choise = input()
        try:
            choise = int(choise)
            return choise
        except ValueError:
            print("Ingrese un valor númerico\n")

def sing_In_Menu():
    print("""En cualquier parte del proceso escriba EXIT para regresar al paso anterior
1: Iniciar Sesión
2: Crear Nueva Cuenta
3: Salir
""")
    choise = choise_()
    if choise == 1:
        return sing_In()
    elif choise == 2:
        sign_Up()
    elif choise == 3:
        print("\nSaliendo de Juego...\n")
    else:
        print("\n¡ERROR! Ingrese una opción valida\n")
        return sing_In_Menu()    

def sing_In():
    global userName
    while True:
        print("\nIngrese su nombre de usuario: ")
        userName = str(input())
        if userName == "EXIT":
            return sing_In_Menu()
        if userName in data["users"]:
            while True:
                print("Ingrese su contraseña")
                userPassword = str(input())
                if userPassword == data["users"][userName]["password"]:
                    global equipment
                    global statistics
                    global inventory
                    equipment = data["users"][userName]["equipment"]
                    statistics = data["users"][userName]["statistics"]
                    inventory = data["users"][userName]["inventory"]
                    #Llamar un objeto desde el inventario: objects[inventory[Posicion en el indice][0]][inventory[Posición en el indice][1]]
                    break
                elif userPassword == "EXIT":
                    return sing_In()
                else:
                    print("\nContraseña incorrecta \n")
            break
        else:
            print("\nNombre de usuario no encontrado\n")
    return start_Menu()

def sign_Up():
    while True:
        print("\nIngrese un nombre de usuario: \n")
        userName = str(input())
        if userName == "EXIT":
            return sing_In_Menu()
        if userName not in data["users"]:
            while True:
                print("\nIngrese una contraseña entre 8 y 15 caracteres: \n")
                userPassword = str(input())
                if userPassword == "EXIT":
                    return sign_Up()
                if not userPassword.__len__() < 8 and not userPassword.__len__() > 15:
                    while True:
                        print("\nIngrese nuevamente la contraseña\n")
                        userPasswordConfirm = str(input())
                        if userPasswordConfirm == "EXIT":
                            break
                        if userPasswordConfirm == userPassword:
                            data["users"][userName] = {}
                            data["users"][userName].update({
                                "password": userPassword,
                                "equipment": {
                                    "weapon": "nothing",
                                    "head": "nothing",
                                    "chest": "nothing",
                                    "legs": "nothing",
                                    "boots": "nothing",
                                    "accesory": "nothing"
                                },
                                "statistics":{
                                    "money":0,
                                    "power": 6
                                },
                                "inventory":[]
                            })
                            save_Progress()
                            break
                        else:
                            print("\nLa contraseña no coincide\n")
                    if userPasswordConfirm != "EXIT":
                            break 
                else:
                    print("\nIngrese una contraseña valida\n")
            break
        else:
            print("\nNombre de usuario ya existente\n")
    return sing_In()

def save_Progress():
    jsonPath = resource_path("Data.json")
    data["users"][userName]["equipment"] = equipment
    data["users"][userName]["statistics"] = statistics
    data["users"][userName]["inventory"] = inventory
    with open (jsonPath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
def gather_(type, object):
    global inventory
    if [type,object] in inventory:
        price = objects[type][object]["value"]
        print(f"Se ha vendido {objects[type][object]["name"]} por {(objects[type][object]["value"])*.9}\n")
        modify_Money(objects[type][object]["value"])
    else:
        inventory.append([type,object])
        print(f"Haz obtenido {objects[type][object]["name"]}.\n")

def start_Menu():
    print("1: Enfrentar Mazmorra \n2: Entrar al inventario \n3: Entrar a la tienda\n4: Entrar a la forja \n5: Salir del juego")
    choise = choise_()
    if choise == 1:
        print("\nBuscando Mazmorras...\n")
        return show_Dungeons()
    elif choise == 2:
        print("\nEntrando al inventario...\n")
        return inventary_Menu()
    elif choise == 3:
        print("\n Entrando a la tienda...\n")
        return shop_()
    elif choise == 4:
        print("\nEntrando a la forja")
        return show_Forge()
    elif choise == 5:
        print("\nSaliendo del Juego...\n")
        save_Progress()
    else:
        print("\n¡ERROR! Ingrese una opción valida\n")
        return start_Menu()

def inventary_Menu():
    print("1: Mostrar inventario \n2: Mostrar equipamiento \n3: Salir")
    choise = choise_()
    if choise == 1:
        print("\nMostrando inventario...\n")
        return show_Invetary()
    elif choise == 2:
        print("\nMostrando Equipamiento...\n")
        return show_Equipment()
    elif choise == 3:
        print("\nRegresando al menú...\n")
        return start_Menu()
    else:
        print("\n¡ERROR! Ingrese una opción valida\n")
        return inventary_Menu()

def show_Invetary():
    print(f"Power: {statistics['power']}           Money: {statistics['money']}")
    for i in range (0,inventory.__len__(),3):
        try:
            print(f"{i+1}: {objects[inventory[i][0]][inventory[i][1]]["name"]}        {i+2}: {objects[inventory[i+1][0]][inventory[i+1][1]]["name"]}        {i+3}: {objects[inventory[i+2][0]][inventory[i+2][1]]["name"]}")
        except:
            try:
                print(f"{i+1}: {objects[inventory[i][0]][inventory[i][1]]["name"]}        {i+2}: {objects[inventory[i+1][0]][inventory[i+1][1]]["name"]}")
            except:
                print(f"{i+1}: {objects[inventory[i][0]][inventory[i][1]]["name"]}")
    print(f"\n0: Salir \n1-{inventory.__len__()}:Mostrar Objeto")
    choise = choise_()
    if choise == 0:
        print("\nRegresando al inicio...\n")
        return start_Menu()
    elif choise >= 1 and choise <= inventory.__len__():
        print("\nMostrando objeto...\n")
        return show_Object(choise-1)
    else:
        print("\n¡ERROR! Ingrese una opción valida\n")
        return show_Invetary()

def show_Object(index):
    print(f"""Nombre: {objects[inventory[index][0]][inventory[index][1]]["name"]}
Poder: {objects[inventory[index][0]][inventory[index][1]]["power"]}
Type: {objects[inventory[index][0]][inventory[index][1]]["type"][0].upper()}{objects[inventory[index][0]][inventory[index][1]]["type"][1:]}
Descripción: {objects[inventory[index][0]][inventory[index][1]]["description"]}

1: Equipar
2: Desequipar
3: Vender
4: Salir
""")
    choise = choise_()
    if choise == 1:
        return equip_Object(objects[inventory[index][0]][inventory[index][1]]["type"],objects[inventory[index][0]][inventory[index][1]]["key"])
    elif choise == 2:
        return unequip_Object(objects[inventory[index][0]][inventory[index][1]]["type"],objects[inventory[index][0]][inventory[index][1]]["key"])
    elif choise == 3: 
        return sell_Object(objects[inventory[index][0]][inventory[index][1]]["type"],objects[inventory[index][0]][inventory[index][1]]["key"])
    elif choise == 4:
        print("\nRegresando al inventario...\n")
        return show_Invetary()
    else:
        print("\n¡ERROR! Ingrese una opción valida\n")
        return show_Object(index)


def equip_Object(type, object):
    global equipment
    if [objects[type][object]["type"],objects[type][object]["key"]] in inventory:
        if objects[type][object]["key"] in equipment[type]:
            print("\nYa tienes equipado este objeto\n")
            set_Power()
            return show_Invetary()
        else:
            print(f"\nHaz equipado {objects[type][object]["name"]}\n")
            equipment[type] = objects[type][object]["key"]
            set_Power()
            return show_Invetary()
    else: 
        print("\nNo tienes el objeto\n")
        save_Progress()
        return show_Invetary()

def sell_Object(type, object):
    if [objects[type][object]["type"],objects[type][object]["key"]] in inventory:
        if objects[type][object]["key"] in equipment[type]:
            print("\nNo puedes vender un objeto equipado\n")
            return show_Invetary()
        else:
            print(f"\nHaz vendido {objects[type][object]["name"]}\n")
            inventory.remove([type,object])
            modify_Money(objects[type][object]["value"]-(objects[type][object]["value"]*.1))
            return show_Invetary()
    else:
        print("\nNo tienes el objeto\n")
        return show_Invetary()

def modify_Money(value):
    global statistics
    statistics["money"] += value
    save_Progress()


def show_Equipment():
    print(f"""1: Arma: {objects['weapon'][equipment['weapon']]["name"]}
2: Sombrero: {objects["head"][equipment["head"]]["name"]}
3: Pechera: {objects["chest"][equipment["chest"]]["name"]}
4: Piernas: {objects["legs"][equipment["legs"]]["name"]}
5: Botas: {objects["boots"][equipment["boots"]]["name"]}
6: Accesorio: {objects["accesory"][equipment["accesory"]]["name"]}

0: Salir
1-6: Desequipar""")
    choise = choise_()
    if choise == 0:
        print("\nRegresando al inventario\n")
        return inventary_Menu()
    elif choise == 1:
        return unequip_Object("weapon",equipment["weapon"])
    elif choise == 2:
        return unequip_Object("head",equipment["head"])
    elif choise == 3:
        return unequip_Object("chest",equipment["chest"])
    elif choise == 4:
        return unequip_Object("legs",equipment["legs"])
    elif choise == 5:
        return unequip_Object("boots",equipment["boots"])
    elif choise == 6:
        return unequip_Object("accesory",equipment["accesory"])
    else:
        print("\n¡ERROR! Ingrese una opción valida\n")
        return show_Equipment()

def unequip_Object(type, object):
    global equipment
    if objects[type][object]["key"] in equipment[type]:
        print(f"\nHaz desequipado {objects[type][object]["name"]}\n")
        equipment[type] = objects[type]["nothing"]["key"]
        set_Power()
    else:
        print("\nNo tienes el objeto equipado\n") 
    return show_Equipment()
     
def set_Power():
    statistics["power"] = objects["weapon"][equipment["weapon"]]["power"] * (objects["head"][equipment["head"]]["power"] + objects["chest"][equipment["chest"]]["power"] + objects["legs"][equipment["legs"]]["power"] + objects["boots"][equipment["boots"]]["power"] * objects["accesory"][equipment["accesory"]]["power"])
    save_Progress()

def show_Dungeons():
    print("\n0: Salir")
    for i in range(0,dungeons["idDungeons"].__len__(), 1):
        print(f"{i+1}: {dungeons[dungeons["idDungeons"][i]]["name"]}")
    choise = choise_()
    if choise == 0:
        print("\nRegresando al inicio\n")
        return start_Menu()
    elif choise > 0 and choise < dungeons["idDungeons"].__len__() +1:
        return figth_Dungeon(dungeons[dungeons["idDungeons"][choise-1]])
    else:    
        print(f"\nIngrese un valor entre 0 y {dungeons["idDungeons"].__len__()}\n")
        return show_Dungeons()

def figth_Dungeon(dungeon):
    progress = 100 / dungeon["difficult"] * statistics["power"]
    if progress > 100:
        progress = 100
        if not dungeon["key"] in statistics["dungeonCompleted"]: 
            statistics["dungeonCompleted"].append(dungeon["key"])
    print(f"""Entrando a la mazmorra {dungeon["name"]}
haz completado el {progress}% de la mazmorra
""")
    print(f"Haz ganado {progress*dungeon["moneyMultiplier"]*2}$\n")
    drops_(dungeon["drops"], progress)
    modify_Money(progress*dungeon["moneyMultiplier"]*2)
    save_Progress()
    return start_Menu()

    
def drops_(drops, progress):
    ndrops = int(((progress // 10) // 2) - .5)
    if ndrops <0:
        ndrops = 0
    for i in range(0,ndrops,1):
        dropped = random.randint(1,100)
        for i2 in range (0,drops.__len__(),1):
            if dropped >= drops[i2][2] and dropped <= drops[i2][3]:
                gather_(drops[i2][1],drops[i2][0]) 
    
def shop_():
    c = 1
    print(f"Tienes {statistics["money"]}$\n")
    print("0: Salir\n")
    for i in range (0,statistics["dungeonCompleted"].__len__(),1):
        for i2 in range(0,6,1):
            print(f"{i2+1}: {objects[shopItems[statistics["dungeonCompleted"][i]][i2][0]][shopItems[statistics["dungeonCompleted"][i]][i2][1]]["name"]} {objects[shopItems[statistics["dungeonCompleted"][i]][i2][0]][shopItems[statistics["dungeonCompleted"][i]][i2][1]]["value"]}$\n")
            c+=1
    choise = choise_()
    if choise == 0:
        return start_Menu()
    elif choise <= c:
        # Hay que comprobar que funcione cuando se agreguen mas objetos de otras mazmorras
        dungeon = statistics["dungeonCompleted"][choise // 6]
        purchase = shopItems[dungeon][(choise % 6)-1]
        if purchase in inventory:
            print("No hay stock de este objeto\n")
            return shop_()
        else:
            gather_(purchase[0], purchase[1])
            modify_Money(-objects[purchase[0]][purchase[1]]["value"])
            return shop_()
    else:
        print("\n¡ERROR! Ingrese una opción valida\n")
        return shop_()
    
def show_Forge():
    c = 1
    print(f"Tienes {statistics["money"]}$\n")
    print("0: Salir\n")
    for i in range (0,statistics["dungeonCompleted"].__len__(),1):
        for i2 in range(0,6,1):
            print(f"{i2+1}: {objects[forge[statistics["dungeonCompleted"][i]][i2][0]][forge[statistics["dungeonCompleted"][i]][i2][1]]["name"]} {objects[forge[statistics["dungeonCompleted"][i]][i2][0]][forge[statistics["dungeonCompleted"][i]][i2][1]]["value"]}$\n")
            c+=1
    choise = choise_()
    if choise == 0:
        return start_Menu()
    elif choise <= c:
        dungeon = statistics["dungeonCompleted"][choise // 6]  
        forged = forge[dungeon][(choise % 6)-1]
        if [forged[0], forged[1]] in inventory:
            print("No puedes tener dos de este objeto\n")
            return show_Forge()
        else:
            if [forged[0], forged[2]] in inventory and [forged[0], forged[3]] in inventory:
                gather_(forged[0], forged[1])
                modify_Money(-objects[forged[0]][forged[1]]["value"])
                return show_Forge()
            else:
                print(f"\nNecesitas tener {objects[forged[0]][forged[2]]["name"]} y {objects[forged[0]][forged[3]]["name"]}\n")
                return show_Forge()
    else:
        print("\n¡ERROR! Ingrese una opción valida\n")
        return show_Forge()
#Funciones Fin
init_()
sing_In_Menu()
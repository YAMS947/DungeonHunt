import random, json

with open("DungeonHunt\Dungeon_Hunt\Data.json ", "r", encoding="utf-8") as f:
    data = json.load(f)

dungeons = data["dungeons"]

objects = data["objects"]


#Diccionarios Fin

#Funciones Inicio
def sing_In_Menu():
    print("""1: Iniciar Sesión
2: Crear Nueva Cuenta
3: Salir
""")
    choise = int(input())
    if choise == 1:
        sing_In()
    elif choise == 2:
        sign_Up()
    elif choise == 3:
        print("\nSaliendo de Juego...\n")
    else:
        print("\n¡ERROR! Ingrese una opción valida\n")
        sing_In_Menu    

def sing_In():
    global userName
    while True:
        print("Ingrese su nombre de ususario: ")
        userName = str(input())
        if userName in data["users"]:
            while True:
                print("Ingrese su contraseña")
                userPassword = str(input())
                if userPassword in data["users"][userName]["password"]:
                    global equipment
                    global statistics
                    global inventory
                    equipment = data["users"][userName]["equipment"]
                    statistics = data["users"][userName]
                    inventory = data["users"][userName]["inventory"]
                    #Llamar un objeto desde el inventario: objects[inventory[Posicion en el indice][0]][inventory[Posición en el indice][1]]
                    break
                else:
                    print("Contraseña incorrecta ")
            break
        else:
            print("Nombre de usuario no encontrado")
    start_Menu()

def sign_Up():
    while True:
        print("Ingrese un nombre de usuario: ")
        userName = str(input())
        if userName not in data["users"]:
            while True:
                print("Ingrese una contraseña entre 8 y 15 caracteres: ")
                userPassword = str(input())
                if not userPassword.__len__() < 8 and not userPassword.__len__() > 15:
                    while True:
                        print("Ingrese nuevamente la contraseña o escriba EXIT para poner otra")
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
                            with open("DungeonHunt\Dungeon_Hunt\Data.json", "w", encoding="utf-8") as f:
                                json.dump(data, f, indent=4, ensure_ascii=False)
                                break
                        else:
                            print("La contraseña no coincide")
                    if userPasswordConfirm != "EXIT":
                            
                            break 
                else:
                    print("Ingrese una contraseña valida")
            break
        else:
            print("Nombre de usuario ya existente")
    sing_In()
        
def gather_(type, object):
    global inventory
    inventory.append((type,object))
    print(f"Haz obtenido {objects[type][object]["name"]}.\n")

def start_Menu():
    print("1: Enfrentar Mazmorra \n2: Entrar al inventario \n3: Salir del juego")
    choise = int(input())
    if choise == 1:
        print("\nBuscando Mazmorras...\n")
        ########################################
    elif choise == 2:
        print("\nEntrando al inventario...\n")
        inventary_Menu()
    elif choise == 3:
        print("\nSaliendo de Juego...\n")
        ########################################
    else:
        print("\n¡ERROR! Ingrese una opción valida\n")
        start_Menu()

def inventary_Menu():
    print("1: Mostrar inventario \n2: Mostrar equipamiento \n3: Salir")
    choise = int(input())
    if choise == 1:
        print("\nMostrando inventario...\n")
        show_Invetary()
    elif choise == 2:
        print("\nMostrando Equipamiento...\n")
        show_Equipment()
    elif choise == 3:
        print("\nRegresando al menú...\n")
        start_Menu()
    else:
        print("\n¡ERROR! Ingrese una opción valida\n")
        inventary_Menu()

def show_Invetary():
    print(f"Power: {statistics['power']}           Money: {statistics['money']}")
    for i in range (0,inventory.__len__(),3):
        try:
            print(f"{i+1}: {inventory[i]}        {i+2}: {inventory[i+1]}        {i+3}: {inventory[i+2]}")
        except:
            try:
                print(f"{i+1}: {inventory[i]}        {i+2}: {inventory[i+1]}")
            except:
                print(f"{i+1}: {inventory[i]}")
    print(f"\n0: Salir \n1-{inventory.__len__()}:Mostrar Objeto")
    choise = int(input())
    if choise == 0:
        print("\nRegresando al inicio...\n")
        start_Menu()
    elif choise >= 1 and choise <= inventory.__len__():
        print("\nMostrando objeto...\n")
        show_Object(choise-1)
    else:
        print("\n¡ERROR! Ingrese una opción valida\n")
        show_Invetary()

def show_Object(index):
    print(f"""Nombre: {objects[inventory[index][0]][inventory[index][1]]["name"]}
Poder: {objects[inventory[index][0]][inventory[index][1]]["power"]}
Type: {objects[inventory[index][0]][inventory[index][1]]["type"][0].upper()}{objects[inventory[index][0]][inventory[index][1]]["type"][1:]}
Descripción: {objects[inventory[index][0]][inventory[index][1]]["description"]}

1: Equipar
2: Desequipar
2: Vender
3: Salir
""")
    choise = int(input())
    if choise == 1:
        equip_Object(objects[inventory[index][0]][inventory[index][1]]["type"],objects[inventory[index][0]][inventory[index][1]]["key"])
    elif choise == 2:
        unequip_Object(objects[inventory[index][0]][inventory[index][1]]["type"],objects[inventory[index][0]][inventory[index][1]]["key"])
    elif choise == 3: 
        sell_Object(objects[inventory[index][0]][inventory[index][1]]["type"],objects[inventory[index][0]][inventory[index][1]]["key"])
    elif choise == 4:
        print("\nRegresando al inventario...\n")
        show_Invetary()
    else:
        print("\n¡ERROR! Ingrese una opción valida\n")
        show_Object(index)


def equip_Object(type, object):
    global equipment
    if (objects[type][object]["type"],objects[type][object]["key"]) in inventory:
        if objects[type][object]["key"] in equipment[type]:
            print("\nYa tienes equipado este objeto\n")
            set_Power()
            show_Invetary()
        else:
            print(f"\nHaz equipado {objects[type][object]["name"]}\n")
            equipment[type] = objects[type][object]["key"]
            set_Power()
            show_Invetary()
    else: 
        print("\nNo tienes el objeto\n")
        show_Invetary

def sell_Object(type, object):
    if (objects[type][object]["type"],objects[type][object]["key"]) in inventory:
        if objects[type][object]["key"] in equipment[type]:
            print("\nNo puedes vender un objeto equipado\n")
            show_Invetary()
        else:
            print(f"\nHaz vendido {objects[type][object]["name"]}\n")
            inventory.remove((type,object))
            modify_Money(objects[type][object]["value"])
            show_Invetary()
    else:
        print("\nNo tienes el objeto\n")
        show_Invetary()

def modify_Money(value):
    global statistics
    statistics["money"] += value

def show_Equipment():
    print(f"""1: Arma: {objects['weapon'][equipment['weapon']]["name"]}
2: Sombrero: {objects["head"][equipment["head"]]["name"]}
3: Pechera: {objects["chest"][equipment["chest"]]["name"]}
4: Piernas: {objects["legs"][equipment["legs"]]["name"]}
5: Botas: {objects["boots"][equipment["boots"]]["name"]}
6: Accesorio: {objects["accesory"][equipment["accesory"]]["name"]}

0: Salir
1-6: Desequipar""")
    choise = int(input())
    if choise == 0:
        print("\nRegresando al inventario\n")
        inventary_Menu()
    if choise == 1:
        unequip_Object("weapon",equipment["weapon"])
    elif choise == 2:
        unequip_Object("head",equipment["head"])
    elif choise == 3:
        unequip_Object("chest",equipment["chest"])
    elif choise == 4:
        unequip_Object("legs",equipment["legs"])
    elif choise == 5:
        unequip_Object("boots",equipment["boots"])
    elif choise == 6:
        unequip_Object("accesory",equipment["accesory"])
    else:
        print("\n¡ERROR! Ingrese una opción valida\n")
        show_Equipment()

def unequip_Object(type, object):
    global equipment
    if objects[type][object]["key"] in equipment[type]:
        print(f"\nHaz desequipado {objects[type][object]["name"]}\n")
        equipment[type] = objects[type]["nothing"]["key"]
    else:
        print("\nNo tienes el objeto equipado\n") 
    set_Power()
    show_Equipment()
     
def set_Power():
     statistics["power"] = objects["weapon"][equipment["weapon"]]["power"] * (objects["head"][equipment["head"]]["power"] + objects["chest"][equipment["chest"]]["power"] + objects["legs"][equipment["legs"]]["power"] + objects["boots"][equipment["boots"]]["power"] * objects["accesory"][equipment["accesory"]]["power"])
#Funciones Fin

sing_In_Menu()

show_Equipment()
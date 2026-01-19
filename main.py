from bot import bot,pycozmo,time

def save_image(v):
    image = v.get_image_camera()
    if image:
        filename = f"img/capture_{int(time.time())}.png"
        try:
            image.save(filename)
            print(f"Image enregistrée : {filename}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
    else:
        print("Aucune image disponible")

def main():
    v = bot()
    boucle = 1
    while boucle == 1:
        try:
            # Connexion au robot via le context manager
            with pycozmo.connect() as robot:
                v.setClient(robot)
                while robot.conn.is_alive():
                    try :
                        var = int(input("1.Capture\n0.Quitter\n# "))

                        match var :
                            case 1 :
                                save_image(v)
                            case 0 :
                                boucle = 0

                    except :
                        print("Valeur invalider")

        except Exception as e:
            print(f"Erreur ou perte de connexion : {e}")
        if hasattr(v, 'disconnect_flag'):
            v.disconnect_flag()
        else:
            v.connected = False
        time.sleep(5)

if __name__ == '__main__':
    main()
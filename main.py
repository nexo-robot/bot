from bot import bot,pycozmo,time
from xbox_controler import xbox_controller

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

def gestion_input_xbox(v, controller):
    axes = controller.get_axes_changes()
    buttons = controller.get_button_events()

    for event, button_id in buttons:
        print(f"Event: {event}, Button ID: {button_id}")
        if event == "pressed":
            match (button_id):
                case 6 :
                    save_image(v)
                    break

def main():
    v = bot()
    manette = 0
    controler = None
    while manette == 0:
        try :
            manette = int(input("Choisir votre type de manette\n1.XBOX\n2.PS4\n# "))
        except:
            print("Valeur invalide")

    print(manette)

    if manette == 1 :
        controler = xbox_controller(deadzone=0.15)

    if controler is not None:
        boucle = 1
        while boucle == 1:
            try:
                # Connexion au robot via le context manager
                with pycozmo.connect() as robot:
                    v.setClient(robot)
                    while robot.conn.is_alive():
                       controler.update()

                       if manette == 1 :
                           gestion_input_xbox(v,controler)

                       time.sleep(0.02)

            except Exception as e:
                print(f"Erreur ou perte de connexion : {e}")

            time.sleep(5)

if __name__ == '__main__':
    main()
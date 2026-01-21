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

    # Gestion des boutons
    for event, button_id in buttons:
        print(f"Event: {event}, Button ID: {button_id}")
        if event == "pressed":
            match (button_id):
                case 6 :
                    save_image(v)
                    break

    # Gestion du joystick gauche pour le déplacement
    # Axe 0 : Gauche/Droite (X)
    # Axe 1 : Haut/Bas (Y)
    
    # On récupère les valeurs actuelles des axes (pas seulement les changements)
    # pour avoir un mouvement continu
    left_x = controller.get_axis(0)
    left_y = controller.get_axis(1)
    
    # Seuil pour considérer qu'il y a mouvement (déjà géré par deadzone dans controller, mais on peut vérifier si non nul)
    if abs(left_x) > 0 or abs(left_y) > 0:
        speed_factor = 100.0
        forward_speed = -left_y * speed_factor # Inversion de Y car souvent -1 est haut
        turn_speed = left_x * speed_factor
        left_wheel = forward_speed + turn_speed
        right_wheel = forward_speed - turn_speed
        max_val = max(abs(left_wheel), abs(right_wheel))
        if max_val > 100.0:
            left_wheel = (left_wheel / max_val) * 100.0
            right_wheel = (right_wheel / max_val) * 100.0

        if abs(forward_speed) > abs(turn_speed):
            if forward_speed > 0:
                v.forward(abs(forward_speed), 0.1)
            else:
                v.backward(abs(forward_speed), 0.1)
        else:
            if turn_speed > 0:
                v.left(abs(turn_speed), 0.1)
            else:
                v.right(abs(turn_speed), 0.1)

    # Note: Ce système n'est pas parfait car bot.py lance des threads et attend la fin du mouvement.
    # Pour un vrai pilotage joystick, il faudrait une méthode set_wheel_speeds(l, r) dans bot.py qui appelle drive_wheels sans bloquer.

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
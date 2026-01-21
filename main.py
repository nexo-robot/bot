from bot import bot,pycozmo,time
from xbox_controler import xbox_controller
import sys

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
    
    should_quit = False

    # Gestion des boutons
    for event, button_id in buttons:
        # print(f"Event: {event}, Button ID: {button_id}")
        if event == "pressed":
            match (button_id):
                case 6 : # Bouton Back/Select souvent utilisé pour quitter ou options
                    save_image(v)
                case 7 : # Bouton Start souvent utilisé pour quitter
                    should_quit = True

    # Gestion du joystick gauche pour le déplacement
    left_x = controller.get_axis(0)
    left_y = controller.get_axis(1)
    
    if abs(left_x) > 0 or abs(left_y) > 0:
        speed_factor = 100.0 
        forward_speed = -left_y * speed_factor 
        turn_speed = left_x * speed_factor
        
        left_wheel = forward_speed + turn_speed
        right_wheel = forward_speed - turn_speed
        
        max_val = max(abs(left_wheel), abs(right_wheel))
        if max_val > 100.0:
            left_wheel = (left_wheel / max_val) * 100.0
            right_wheel = (right_wheel / max_val) * 100.0
            
        v.drive_wheels(left_wheel, right_wheel)
    else:
        v.drive_wheels(0.0, 0.0)
        
    return should_quit

def main():
    v = bot()
    manette = 0
    controler = None
    while manette == 0:
        try :
            manette = int(input("Choisir votre type de manette\n1.XBOX\n2.PS4\n# "))
        except KeyboardInterrupt:
            print("\nArrêt demandé.")
            return
        except:
            print("Valeur invalide")

    print(manette)

    if manette == 1 :
        try:
            controler = xbox_controller(deadzone=0.15)
        except Exception as e:
            print(f"Erreur initialisation manette: {e}")
            return

    if controler is not None:
        running = True
        while running:
            try:
                print("En attente de connexion au robot...")
                # Connexion au robot via le context manager
                with pycozmo.connect() as robot:
                    print("Robot connecté.")
                    v.setClient(robot)
                    
                    # Boucle principale de contrôle
                    while robot.conn.is_alive() and running:
                       controler.update()

                       if manette == 1 :
                           if gestion_input_xbox(v,controler):
                               print("Arrêt demandé via la manette.")
                               v.drive_wheels(0, 0) # Arrêt des moteurs avant de quitter
                               running = False
                               break

                       time.sleep(0.02)
                    
                # Sortie du context manager : la connexion est fermée physiquement
                # On met à jour l'état de l'objet bot
                v.disconnect_flag()
                print("Déconnexion du robot effectuée.")

            except KeyboardInterrupt:
                print("\nArrêt demandé par l'utilisateur (Ctrl+C).")
                running = False
            except Exception as e:
                print(f"Erreur ou perte de connexion : {e}")
                v.disconnect_flag() # On s'assure que le flag est reset en cas d'erreur
                # On attend un peu avant de retenter la connexion si on ne quitte pas
                if running:
                    time.sleep(2)

        # Nettoyage final
        if controler:
            controler.quit()
        print("Programme terminé.")

if __name__ == '__main__':
    main()
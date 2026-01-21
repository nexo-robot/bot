import pycozmo
from threading import Thread as th
import time

class bot:
    def __init__(self,cli:pycozmo.Client=None):
        self.__cozmo = None
        self.__cube_id = None
        self.__cubeConnected = False
        self.__move = False
        self.connected = False

        self.__fluxCamera = None

        if cli:
            self.setClient(cli)

    def setClient(self,cli:pycozmo.Client):
        self.__cozmo = cli
        self.connected = True
        try:
            self.__cozmo.set_volume(50000)
            self.__startCamera()
        except Exception as e:
            print("Erreur init client:", e)

    def disconnect_flag(self):
        """Appelé par le main quand la connexion saute"""
        self.connected = False
        self.__fluxCamera = None

    def is_connected(self) -> bool:
        return self.connected

    def __startCamera(self) -> bool:
        if not self.connected:
            return False
        else:
            try:
                self.__cozmo.enable_camera(enable=True, color=True)
                self.__cozmo.add_handler(pycozmo.event.EvtNewRawCameraImage, self.__set_image_camera)
                return True
            except Exception as e:
                print("Erreur :", e)
                return False

    def __set_image_camera(self,cli,image):
        self.__fluxCamera = image

    def get_image_camera(self):
        if not self.connected:
            return None

        if not self.__fluxCamera:
            return None

        return self.__fluxCamera

    def drive_wheels(self, lwheel_speed: float, rwheel_speed: float):
        """
        Commande directe des roues sans blocage ni thread.
        Idéal pour le contrôle joystick continu.
        """
        if not self.connected or not self.__cozmo:
            return False
        
        try:
            self.__cozmo.drive_wheels(lwheel_speed=lwheel_speed, rwheel_speed=rwheel_speed)
            return True
        except Exception as e:
            print(f"Erreur drive_wheels : {e}")
            return False

    def __moveEngine(self, lspeed: float, rspeed: float, duration: float):
        """
        Gère le mouvement en 3 étapes : Start -> Sleep -> Stop
        Cela évite de passer 'duration' à drive_wheels qui fait souvent planter pycozmo.
        La boucle de pause vérifie régulièrement l'état de la connexion pour éviter
        que le robot ne continue de bouger indéfiniment en cas de déconnexion.
        """
        if lspeed > 100 or rspeed > 100:
            return False
        if self.__move:
            return False

        self.__move = True

        try:
            if self.is_connected() and self.__cozmo:
                self.__cozmo.drive_wheels(lwheel_speed=lspeed, rwheel_speed=rspeed)
                end_time = time.time() + duration
                while time.time() < end_time:
                    if not self.is_connected():
                        return False
                    time.sleep(0.05)
                if self.is_connected() and self.__cozmo:
                    self.__cozmo.drive_wheels(lwheel_speed=0.0, rwheel_speed=0.0)
                return True
        except Exception as e:
            print(f"Erreur dans __moveEngine : {e}")
            return False
        finally:
            self.__move = False


    def forward(self,speed:float,duration:float) -> bool:
        if not self.connected:
            return False
        else :
            if speed <= 100:
                try :
                    self.__moveEngine(speed,speed,duration)
                    return True
                except Exception as e:
                    print("Erreur :", e)
                    return False
            else :
                return False

    def backward(self,speed:float,duration:float) -> bool:
        if not self.connected:
            return False
        else:
            if speed <= 100:
                try:
                    self.__moveEngine(-speed,-speed,duration)
                    return True
                except Exception as e:
                    print("Erreur :", e)
                    return False
            else:
                return False

    def right(self,speed:float,duration:float) -> bool:
        if not self.connected:
            return False
        else:
            if speed <= 100:
                try:
                    self.__moveEngine(-speed,speed,duration)
                    return True
                except Exception as e:
                    print("Erreur :", e)
                    return False
            else:
                return False

    def left(self,speed:float,duration:float) -> bool:
        if not self.connected:
            return False
        else:
            if speed <= 100:
                try:
                    self.__moveEngine(speed,-speed,duration)
                    return True
                except Exception as e:
                    print("Erreur :", e)
                    return False
            else:
                return False

    def move_head(self, possition:int) -> bool:
        """
        1 : -0.5 --> Down position
        2 : -0.4
        3 : -0.3
        4 : -0.2
        5 : -0.1
        6 : 0.0 --> Middle position
        7 : 0.1
        8 : 0.2
        9 : 0.3
        10 : 0.4
        11 : 0.5
        12 : 0.6
        13 : 0.7
        14 : 0.8
        15 : 0.9 --> Up position
        """
        if not self.connected:
            return False
        else:
            try:
                if possition == 1:
                    self.__cozmo.set_head_angle(angle=-0.5)
                elif possition == 2:
                    self.__cozmo.set_head_angle(angle=-0.4)
                elif possition == 3:
                    self.__cozmo.set_head_angle(angle=-0.3)
                elif possition == 4:
                    self.__cozmo.set_head_angle(angle=-0.2)
                elif possition == 5:
                    self.__cozmo.set_head_angle(angle=-0.1)
                elif possition == 6:
                    self.__cozmo.set_head_angle(angle=0.0)
                elif possition == 7:
                    self.__cozmo.set_head_angle(angle=0.1)
                elif possition == 8:
                    self.__cozmo.set_head_angle(angle=0.2)
                elif possition == 9:
                    self.__cozmo.set_head_angle(angle=0.3)
                elif possition == 10:
                    self.__cozmo.set_head_angle(angle=0.4)
                elif possition == 11:
                    self.__cozmo.set_head_angle(angle=0.5)
                elif possition == 12:
                    self.__cozmo.set_head_angle(angle=0.6)
                elif possition == 13:
                    self.__cozmo.set_head_angle(angle=0.7)
                elif possition == 14:
                    self.__cozmo.set_head_angle(angle=0.8)
                elif possition == 15:
                    self.__cozmo.set_head_angle(angle=0.9)
                else:
                    return False
                return True
            except Exception as e:
                print("Erreur :", e)
                return False

    def moveLift(self, height:float) -> bool:
        if not self.connected:
            return False
        else:
            if pycozmo.MIN_LIFT_HEIGHT.mm <= height <= pycozmo.MAX_LIFT_HEIGHT.mm :
                try:
                    self.__cozmo.set_lift_height(height=height)
                    return True
                except Exception as e:
                    print("Erreur :", e)
                    return False
            else:
                return False

    def sound(self,file:str):
        try :
            self.__cozmo.play_audio(file)
            self.__cozmo.wait_for(pycozmo.event.EvtAudioCompleted)
            return True
        except Exception as e:
            print("Erreur :", e)
            return False

    def disconnectCube(self):
        if not self.__cubeConnected or self.__cube_id is None:
            return False

        if not self.connected:
            return False

        self.__cubeConnected = False
        self.__cube_id = None

        pkt = pycozmo.protocol_encoder.ObjectConnect(
            factory_id=self.__cube_factory_id,
            connect=False
        )
        self.__cozmo.conn.send(pkt)

        self.__cube_factory_id = None

        return True



    def connectCubes(self, cube_number=1):
        """
        cube_number : 1, 2 ou 3
        1 -> LIGHTCUBE1
        2 -> LIGHTCUBE2
        3 -> LIGHTCUBE3
        """
        try:
            if self.__cubeConnected:
                self.disconnectCube()

            cube_map = {
                1: pycozmo.protocol_encoder.ObjectType.Block_LIGHTCUBE1,
                2: pycozmo.protocol_encoder.ObjectType.Block_LIGHTCUBE2,
                3: pycozmo.protocol_encoder.ObjectType.Block_LIGHTCUBE3,
            }

            if cube_number not in cube_map:
                raise ValueError("cube_number doit être 1, 2 ou 3")

            target_type = cube_map[cube_number]

            self.__cube_factory_id = None

            # Recherche du cube dans available_objects
            while not self.__cube_factory_id:
                available_objects = dict(self.__cozmo.available_objects)

                for factory_id, obj in available_objects.items():
                    if obj.object_type == target_type:
                        self.__cube_factory_id = factory_id
                        break

            pkt = pycozmo.protocol_encoder.ObjectConnect(
                factory_id=self.__cube_factory_id,
                connect=True
            )
            self.__cozmo.conn.send(pkt)

            # Attendre l’événement de connexion
            self.__cozmo.conn.wait_for(pycozmo.protocol_encoder.ObjectConnectionState)

            timeout = time.time() + 5
            while not self.__cozmo.connected_objects:
                if time.time() > timeout:
                    raise TimeoutError("Le cube n'est jamais apparu dans connected_objects.")
                time.sleep(0.05)

            self.__cube_id = next(iter(self.__cozmo.connected_objects.keys()))

            self.__cubeConnected = True
            return True
        except Exception as e:
            print("Erreur :", e)
            return False


    def setSound(self,sound:int):
        if 0 <= sound <= 65535:
            self.__cozmo.set_volume(sound)
            return True
        else :
            self.__cozmo.set_volume(50000)
            return False

    def setLightCube(self,light1,light2,light3,light4):
        if not self.__cubeConnected:
            return False

        if not self.connected:
            return False


        try :
            pkt = pycozmo.protocol_encoder.CubeId(object_id=self.__cube_id)
            self.__cozmo.conn.send(pkt)
            # Set lights
            pkt = pycozmo.protocol_encoder.CubeLights(states=(light1, light2, light3, light4))
            self.__cozmo.conn.send(pkt)
            return True
        except Exception as e :
            print("Erreur :", e)
            return False

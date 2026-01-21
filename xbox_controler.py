import pygame
import sys

class xbox_controller:
    def __init__(self, deadzone=0.1):
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            raise RuntimeError("Aucune manette détectée")

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        self.deadzone = deadzone

        self.num_axes = self.joystick.get_numaxes()
        self.num_buttons = self.joystick.get_numbuttons()

        # États précédents
        self.prev_axes = [0.0] * self.num_axes
        self.prev_buttons = [0] * self.num_buttons

    def _apply_deadzone(self, value):
        return 0 if abs(value) < self.deadzone else value

    def update(self):
        """
        À appeler dans la boucle principale
        """
        pygame.event.pump()

    def get_axes_changes(self):
        """
        Retourne les axes qui ont bougé
        """
        changes = []

        for i in range(self.num_axes):
            value = self._apply_deadzone(self.joystick.get_axis(i))

            if value != self.prev_axes[i]:
                changes.append((i, value))
                self.prev_axes[i] = value

        return changes

    def get_button_events(self):
        """
        Retourne les boutons pressés ou relâchés
        """
        events = []

        for i in range(self.num_buttons):
            state = self.joystick.get_button(i)

            if state != self.prev_buttons[i]:
                if state:
                    events.append(("pressed", i))
                else:
                    events.append(("released", i))

                self.prev_buttons[i] = state

        return events

from .djitellopy import Tello
import cv2
import pygame
import numpy as np
import time
from threading import Thread
from multiprocessing import Process

# Speed of the drone
S = 60
# Frames per second of the pygame window display
FPS = 25
# Rotation degrees
ROTATION_DEGREES = 30


class DroneApi(object):
    """ Maintains the Tello display and moves it through the keyboard keys.
        Press escape key to quit.
        The controls are:
            - T: Takeoff
            - L: Land
            - Arrow keys: Forward, backward, left and right.
            - A and D: Counter clockwise and clockwise rotations
            - W and S: Up and down.
    """

    def __init__(self, is_fake=False):

        self.is_fake = is_fake

        # Init Tello object that interacts with the Tello drone
        self.tello = Tello(enable_exceptions = False)

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10
        self.should_stop = False

        self.is_connected = False
        self.send_rc_control = False

    def runPygame(self):
        # Init pygame
        pygame.init()

        # Creat pygame window
        pygame.display.set_caption("Tello video stream")
        self.screen = pygame.display.set_mode([960, 720])

        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 50)

        while not self.should_stop:
            self.processPygame()
            time.sleep(1 / FPS)

        # Call it always before finishing. To deallocate resources.
        if not self.is_fake:
            self.frame_read.stop()
            self.tello.end()
        pygame.quit()

    def processPygame(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                self.update()
            elif event.type == pygame.QUIT:
                self.should_stop  =True
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.should_stop = True
                    return
                else:
                    self.keydown(event.key)
            elif event.type == pygame.KEYUP:
                self.keyup(event.key)

        if not self.is_fake and self.frame_read.stopped:
            self.frame_read.stop()
            self.should_stop = True
            return

        #cv2.imshow("frame", self.frame_read.frame)

        if not self.is_fake:
            self.screen.fill([0, 0, 0])
            frame = cv2.cvtColor(self.frame_read.frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = np.flipud(frame)
            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
            pygame.display.update()

    def keydown(self, key):
        """ Update velocities based on key pressed
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP:  # set forward velocity
            self.for_back_velocity = S
        elif key == pygame.K_DOWN:  # set backward velocity
            self.for_back_velocity = -S
        elif key == pygame.K_LEFT:  # set left velocity
            self.left_right_velocity = -S
        elif key == pygame.K_RIGHT:  # set right velocity
            self.left_right_velocity = S
        elif key == pygame.K_w:  # set up velocity
            self.up_down_velocity = S
        elif key == pygame.K_s:  # set down velocity
            self.up_down_velocity = -S
        elif key == pygame.K_a:  # set yaw counter clockwise velocity
            self.yaw_velocity = -S
        elif key == pygame.K_d:  # set yaw clockwise velocity
            self.yaw_velocity = S

    def keyup(self, key):
        """ Update velocities based on key released
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP or key == pygame.K_DOWN:  # set zero forward/backward velocity
            self.for_back_velocity = 0
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:  # set zero left/right velocity
            self.left_right_velocity = 0
        elif key == pygame.K_w or key == pygame.K_s:  # set zero up/down velocity
            self.up_down_velocity = 0
        elif key == pygame.K_a or key == pygame.K_d:  # set zero yaw velocity
            self.yaw_velocity = 0
        elif key == pygame.K_t:  # takeoff
            self.takeoff()
            print(self.send_rc_control)
        elif key == pygame.K_l:  # land
            self.land()

    def update(self):
        """ Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            if not self.is_fake:
                self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity, self.up_down_velocity,
                                           self.yaw_velocity)

    def connect(self):
        if not self.is_fake:
            if not self.tello.connect():
                print("Tello not connected")
                return

            if not self.tello.set_speed(self.speed):
                print("Not set speed to lowest possible")
                return

            # In case streaming is on. This happens when we quit this program without the escape key.
            if not self.tello.streamoff():
                print("Could not stop video stream")
                return

            if not self.tello.streamon():
                print("Could not start video stream")
                return

            self.frame_read = self.tello.get_frame_read()
        else:
            print("Starting Drone API in fake mode...")

        self.is_connected = True

    def takeoff(self):
        """ Take off """
        if self.is_connected:
            if not self.is_fake:
                self.tello.takeoff()
            else: 
                print("Fake take off")
        self.send_rc_control = True


    def land(self):
        """ Land """
        print(self.send_rc_control)
        if self.send_rc_control:
            if not self.is_fake:
                self.tello.land()
            else: 
                print("Fake land")
        self.send_rc_control = False

    def right(self):
        """ Turn X degrees right """
        print(self.send_rc_control)
        if self.send_rc_control:
            if not self.is_fake:
                self.tello.rotate_clockwise(ROTATION_DEGREES)
            else: 
                print("Fake turn right")

    def left(self):
        """ Turn X degrees right """
        if self.send_rc_control:
            if not self.is_fake:
                self.tello.rotate_counter_clockwise(ROTATION_DEGREES)
            else: 
                print("Fake turn left")
import pygame
import pygame_menu
import random, sys, math, time
from perlin_noise import PerlinNoise
from pygame_gui.ui_manager import UIManager
from pygame_gui.elements import UIPanel, UIButton, UILabel, UITextEntryLine, UIScrollingContainer, UIStatusBar

current_time = time.time()
random.seed(current_time)
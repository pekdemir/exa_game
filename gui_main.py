import pygame
import pygame_gui

import pygame_gui.data

from pygame.color import Color
from pygame.surface import Surface
from pygame_gui.elements import UIWindow

from pygame_gui.elements import UITextBox, UITextEntryBox

"""
A test bed to tinker with future text features.
"""


def test_app():
    pygame.init()

    display_surface = pygame.display.set_mode((800, 600))

    ui_manager = pygame_gui.UIManager((800, 600), 'console_theme.json')

    output_window = UIWindow(pygame.Rect(400, 20, 300, 400), window_display_title="Pygame GUI Formatted Text")
    output_window2 = UIWindow(pygame.Rect(400, 20, 300, 400), window_display_title="Pygame GUI Formatted Text")

    background = Surface((800, 600), depth=32)
    background.fill(Color("#606060"))

    text_box = UITextEntryBox(
        relative_rect=pygame.Rect((0, 0), output_window.get_container().get_size()),
        container=output_window,
        manager=ui_manager)
    
    text_box.should_html_unescape_input_text = True

    text_box.set_text(html_text="<body>"
                  "<p style=\"line-height:100px\">"
                  "<font color=#F0F0F0><b>MARK</b> start\n</font>"
                  "<font color=#F0F0F0 ><body bgcolor=#A0A050><b>ADDI</b> X 1 X\n</body></font>"
                  "<font color=#F0F0F0><b>TEST</b> X < 10\n</font>"
                  "<font color=#F0F0F0><b>FJMP</b> start\n</font>"
                  "<font color=#F0F0F0><b>HALT</b>\n</font>"
                  "</p></body>")

    text_box2 = UITextEntryBox(
    relative_rect=pygame.Rect((0, 0), output_window.get_container().get_size()),
    container=output_window2,
    manager=ui_manager)

    is_running = True
    clock = pygame.time.Clock()

    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            ui_manager.process_events(event)

        display_surface.blit(background, (0, 0))

        ui_manager.update(0.01)
        ui_manager.draw_ui(window_surface=display_surface)

        pygame.display.update()


if __name__ == "__main__":
    test_app()
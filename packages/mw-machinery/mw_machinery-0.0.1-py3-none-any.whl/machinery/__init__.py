#!/usr/bin/env python3

"""The machine engine"""

import asyncio
import time
from typing import Callable

import pygame
from pygame import QUIT

FPS = 100
width, height = 700, 400


class Ball:  # using a Sprite would be better
    """FIXME: class docstring"""

    def __init__(self):
        """FIXME: function docstring"""
        self.ball = pygame.image.load("intro_ball.gif")
        self.rect = self.ball.get_rect()
        self.speed = [2, 2]

    def move(self):
        """FIXME: function docstring"""
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speed[1] = -self.speed[1]

    def draw(self, screen):
        """FIXME: function docstring"""
        screen.blit(self.ball, self.rect)


def pygame_event_loop(loop, event_queue):
    """FIXME: function docstring"""
    while True:
        event = pygame.event.wait()
        asyncio.run_coroutine_threadsafe(event_queue.put(event), loop=loop)


async def animation(screen, ball):
    """FIXME: function docstring"""
    black = 0, 0, 0

    current_time = 0
    while True:
        last_time, current_time = current_time, time.time()
        await asyncio.sleep(1 / FPS - (current_time - last_time))  # tick
        ball.move()
        screen.fill(black)
        ball.draw(screen)
        pygame.display.flip()


async def handle_events(event_queue, ball):
    """FIXME: function docstring"""
    while True:
        event = await event_queue.get()
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if ball.speed == [0, 0]:
                    ball.speed = [2, 2]
                else:
                    ball.speed = [0, 0]
        else:
            print("event", event)

        pygame.display.update()
    asyncio.get_event_loop().stop()


def run(callback: Callable[[], None]) -> None:
    """The starting point"""
    print("run")

    dom = callback()

    loop = asyncio.get_event_loop()
    event_queue = asyncio.Queue()

    pygame.init()

    pygame.display.set_caption("pygame+asyncio")
    screen = pygame.display.set_mode((width, height), 0, 32)

    screen.fill((255, 255, 255))

    for elem in dom.get("draw"):
        if elem[0] == "rect":
            dimensions, color = elem[1], elem[2]
            pygame.draw.rect(screen, color, dimensions)

    ball = Ball()

    pygame_task = loop.run_in_executor(None, pygame_event_loop, loop, event_queue)
    animation_task = asyncio.ensure_future(animation(screen, ball))
    event_task = asyncio.ensure_future(handle_events(event_queue, ball))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        pygame_task.cancel()
        animation_task.cancel()
        event_task.cancel()

    pygame.quit()

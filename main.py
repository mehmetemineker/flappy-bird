import pygame, asyncio

import assets
import configs
from objects.background import Background
from objects.bird import Bird
from objects.column import Column
from objects.floor import Floor
from objects.gameover_message import GameOverMessage
from objects.gamestart_message import GameStartMessage
from objects.score import Score

pygame.init()
screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Game v1.0.2")
img = pygame.image.load('assets/icons/red_bird.png')
pygame.display.set_icon(img)

clock = pygame.time.Clock()


assets.load_sprites()
assets.load_audios()

sprites = pygame.sprite.LayeredUpdates()

def create_sprites():
    Background(0, sprites)
    Background(1, sprites)
    Floor(0, sprites)
    Floor(1, sprites)

    return Bird(sprites), GameStartMessage(sprites), Score(sprites)

async def main():
    game_over = False
    game_started = False
    bird, game_start_message, score = create_sprites()
    column_create_event = pygame.USEREVENT

    while True:
        for event in pygame.event.get():           
            if event.type == column_create_event and game_started:
                Column(sprites)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_started and not game_over:
                    game_started = True
                    game_start_message.kill()
                    pygame.time.set_timer(column_create_event, 1500)
                if event.key == pygame.K_ESCAPE and game_over:
                    game_over = False
                    game_started = False
                    sprites.empty()
                    bird, game_start_message, score = create_sprites()

            if not game_over:
                bird.handle_event(event)

        screen.fill(0)

        sprites.draw(screen)

        if game_started and not game_over:
            sprites.update()

        if bird.check_collision(sprites) and not game_over:
            game_over = True
            game_started = False
            GameOverMessage(sprites)
            pygame.time.set_timer(column_create_event, 0)
            assets.play_audio("hit")
            column_create_event += 1

        for sprite in sprites:
            if type(sprite) is Column and sprite.is_passed():
                score.value += 1
                assets.play_audio("point")
        
        pygame.display.update()
        clock.tick(configs.FPS)
        await asyncio.sleep(0)

asyncio.run(main())
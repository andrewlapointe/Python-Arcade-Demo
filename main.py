import arcade
import random
import time

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = "temp_name"

CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

PROJECTILE_SPEED = 3.5
PROJECTILE_SPRITE_LIST = [":resources:images/space_shooter/meteorGrey_big1.png", ":resources:images/space_shooter/meteorGrey_big2.png", ":resources:images/space_shooter/meteorGrey_big3.png", ":resources:images/space_shooter/meteorGrey_big4.png"]

PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

# LEFT_VEIWPORT_MARGIN = 250
# RIGHT_VEIWPORT_MARGIN = 250
# BOTTOM_VEIWPORT_MARGIN = 50
# TOP_VEIWPORT_MARGIN = 100

class gameWindow(arcade.Window):
    def __init__(self) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        self.background1 = arcade.load_texture(":resources:images/cybercity_background/far-buildings.png")
        self.background2 = arcade.load_texture(":resources:images/cybercity_background/back-buildings.png")
  
        
        self.coin_list = None
        self.wall_list = None
        self.player_list = None

        self.player_sprite = None
        self.current_texture = 0

        self.view_bottom = 0
        self.view_left = 0

        self.audio_playing = False

        self.speed_mod = 1

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash = True)
        self.coin_list = arcade.SpriteList(use_spatial_hash = True)
        self.projectile_list = arcade.SpriteList()

        image_source = ":resources:images/animated_characters/robot/robot_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 200
        self.player_list.append(self.player_sprite)

        for i in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/stone.png", TILE_SCALING)
            wall.center_x = i
            wall.center_y = 48
            self.wall_list.append(wall)

        coordinate_list = [[random.randint(30, SCREEN_WIDTH - 30), 1000],[random.randint(30, SCREEN_WIDTH - 30), 700],[random.randint(30, SCREEN_WIDTH - 30), 800], [random.randint(30, SCREEN_WIDTH - 30), 700],[random.randint(30, SCREEN_WIDTH - 30), 1600]]

        # for coordinate in coordinate_list:
        #     projectile = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
        #     projectile.position = coordinate
        #     self.projectile_list.append(projectile)

        self.physics_engine = arcade.PhysicsEnginePlatformer(player_sprite = self.player_sprite, walls = self.wall_list, gravity_constant = GRAVITY)


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED * -1

    def on_key_release(self, key, modifiers):
        
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
    
    def on_update(self, delta_time: float):
        self.physics_engine.update()

        if not self.audio_playing:
            audio = arcade.load_sound("earthworm-jim-music-snes-buttville-the-queens-lair.mp3", False)
            arcade.play_sound(audio)
            self.audio_playing = True


        for projectile in self.projectile_list:
            projectile.center_y -= PROJECTILE_SPEED * self.speed_mod

            if projectile.center_y < -6:
                self.projectile_list.remove(projectile)
        
        if len(self.projectile_list) < 14:
            new_projectile = arcade.Sprite(PROJECTILE_SPRITE_LIST[random.randint(0, len(PROJECTILE_SPRITE_LIST) - 1)], TILE_SCALING)
            new_projectile.position = [random.randint(30, SCREEN_WIDTH - 30), random.randint(800, 1400)]
            new_projectile.angle = random.randint(0, 180)
            self.projectile_list.append(new_projectile)

        colliding = False
        for projectile in self.projectile_list:
            colliding = arcade.check_for_collision(self.player_sprite, projectile)
            if colliding: break
        
        if colliding: self.close()

    def player_animation(self):
        self.current_texture += 1
        if self.current_texture > 7:
            self.current_texture = 0
        self.texture = self.walk_textures[self.current_texture][
            self.character_face_direction
        ]



    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(500, 400, 1000,
                                      800, self.background1)
        arcade.draw_texture_rectangle(500, 400, 1000,
                                      800, self.background2)

        self.wall_list.draw()
        self.player_list.draw()
        self.coin_list.draw()
        self.projectile_list.draw()


def main():
    window = gameWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
import pygame
import os
import math

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Circle:
    def __init__(self, center, radius):
        self.center = center   # tower的中心點
        self.radius = radius   # tower的攻擊範圍

    def collide(self, enemy):
        """
        Q2.2)check whether the enemy is in the circle (attack range), if the enemy is in range return True
        :param enemy: Enemy() object
        :return: Bool
        """
        # 記下 enemy 和 tower 的位置
        enemy_x, enemy_y = enemy.get_pos()
        tower_x, tower_y = self.center
        # 計算 enemy 和 tower 之間的距離
        distance_enemy_to_tower = math.sqrt((enemy_x - tower_x)**2 + (enemy_y - tower_y)**2)
           
        # 若 enemy 和 tower 之間的距離"小於等於"攻擊範圍則回傳"True" 
        if(distance_enemy_to_tower <= self.radius):
            return True
        else:
            return False
        """
        Hint:
        x1, y1 = enemy.get_pos()
        ...
        """

    def draw_transparent(self, win):
        """
        Q1) draw the tower effect range, which is a transparent circle.
        :param win: window surface
        :return: None
        """
         # 創造一個透明的 surface
        transparent_surface = pygame.Surface((1024, 600), pygame.SRCALPHA)
        transparency = 50  # define transparency: 0~255, 0 is fully transparent
        
        # 在透明的 surface上畫一個半透明的圓
        pygame.draw.circle(transparent_surface, (255, 255, 255, transparency), self.center, self.radius, 0)
        # 在 window surface上畫上創造出來的透明的 surface
        win.blit(transparent_surface, (0, 0))


class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected = True  # the state of whether the tower is selected
        self.type = "tower"

    def is_cool_down(self):
        """
        Q2.1) Return whether the tower is cooling down
        (1) Use a counter to computer whether the tower is cooling down (( self.cd_count
        :return: Bool
        """
        # 當冷卻經過時間 小於 冷卻完成時間時，冷卻經過時間增加，並回傳 False 表示還"未完成冷卻"
        if self.cd_count < self.cd_max_count:
            self.cd_count += 1
            return False
        # 若冷卻經過時間 等於 冷卻完成時間時，重置冷卻時間，並回傳 True 表示"完成冷卻"
        else:
            self.cd_count = 0
            return True
        """
        Hint:
        let counter be 0
        if the counter < max counter then
            set counter to counter + 1
        else 
            counter return to zero
        end if
        """

    def attack(self, enemy_group):
        """
        Q2.3) Attack the enemy.
        (1) check the the tower is cool down ((self.is_cool_down()
        (2) if the enemy is in attack range, then enemy get hurt. ((Circle.collide(), enemy.get_hurt()
        :param enemy_group: EnemyGroup()
        :return: None
        """
        enemy = enemy_group.get()    # 利用".get()" 獲得 enemy list
        
        # 當"冷卻完成"時，開始分析 enemy 是否位於攻擊範圍內，若"是"則對該 enemy 進行攻擊
        if(self.is_cool_down() == True):
            for i in range(len(enemy)):
                if(self.range_circle.collide(enemy[i])== True):
                    enemy[i].get_hurt(self.damage)
                    return 
            
    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        """
        # 記下 滑鼠點下左鍵的位置 和 tower的位置
        mouse_x, mouse_y = (x, y)
        tower_x, tower_y = self.rect.center
        # 計算 滑鼠點下左鍵的位置 和 tower的位置 之間的距離
        distance_mouse_to_tower = math.sqrt((mouse_x - tower_x)**2 + (mouse_y - tower_y)**2)
        
        # 若兩者之間的距離小於50時，則 return True 表滑鼠有點擊到 tower了
        if(distance_mouse_to_tower <= 50):
            return True
        else:
            return False

    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        self.is_selected = is_selected

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower


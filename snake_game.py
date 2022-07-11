from turtle import Turtle, Screen
import random
import time


class Snake:
    def __init__(self, distance=20, delay_time=0.05, scree_size=(600, 600), initial_len=3):
        self.game_pause_banner = None
        self.box = None
        self.score_banner = None
        self.shift = 0.8
        self.food = None
        self.distance = distance
        self.default_distance = distance
        self.delay_time = delay_time
        self.screen_size = scree_size
        self.snakes = []
        self.screen = Screen()
        self.screen.setup(width=scree_size[0], height=scree_size[1])
        self.screen.bgcolor("black")
        self.screen.title("Snake Game v1.0")
        self.draw_bounds()
        self.screen.tracer(0)
        self.game_on = True
        self.initial_len = initial_len
        self.food_threshold = 15
        self.game_pause = None
        self.score = 0
        self.high_score = 0
        pos = 0
        for i in range(initial_len):
            self.snake = Turtle()
            self.snake.penup()
            self.snake.shape("square")
            self.snake.color("white")
            self.snake.setposition(x=0 - pos, y=0)
            self.snakes.append(self.snake)
            pos += self.distance
        self.snake_head = self.snakes[0]
        self.snake_food()
        self.screen_update(self.delay_time)
        self.score_board()
        print("Initialization done successfully! Starting the game..")
        self.game_loop(self.snakes)
        self.screen.exitonclick()

    def draw_bounds(self):
        self.box = Turtle()
        self.box.penup()
        self.box.color("white", "black")
        self.box.shape("square")
        self.box.turtlesize(stretch_wid=int((self.screen_size[0] / 20) * 0.85),
                            stretch_len=int((self.screen_size[1] / 20) * 0.85))

    def score_board(self):
        self.score_banner = Turtle()
        self.score_banner.penup()
        self.score_banner.color("white")
        self.score_banner.hideturtle()
        self.score_banner.goto(x=0, y=int(0.90 * (self.screen_size[1] / 2)))
        self.score_banner.write(f"Score : {self.score}\tHigh score: {self.high_score}", True, align="center",
                                font=('Arial', 15, 'normal'))

    def screen_update(self, delay_time):
        time.sleep(delay_time)
        self.screen.update()

    def snake_move(self, snakes, distance):
        self.screen_update(self.delay_time)
        for i in range(len(self.snakes) - 1, 0, -1):
            y_pos = self.snakes[i - 1].ycor()
            x_pos = self.snakes[i - 1].xcor()
            self.snakes[i].goto(x_pos, y_pos)
        self.snake_head.forward(self.distance)
        self.screen_update(self.delay_time)

    def snake_direction_up(self):
        if self.snake_head.heading() != 270:
            self.snake_head.setheading(90)

    def snake_direction_down(self):
        if self.snake_head.heading() != 90:
            self.snake_head.setheading(270)

    def snake_direction_left(self):
        if self.snake_head.heading() != 0:
            self.snake_head.setheading(180)

    def snake_direction_right(self):
        if self.snake_head.heading() != 180:
            self.snake_head.setheading(0)

    def snake_pause(self):
        if not self.game_pause and self.game_on:
            # self.distance = 0
            print("Game is paused!")
            self.game_pause_banner = Turtle()
            self.game_pause_banner.penup()
            self.game_pause_banner.color("white")
            self.game_pause_banner.hideturtle()
            self.box.hideturtle()
            self.game_pause_banner.write(f"Game is paused!", True, align="center", font=('Arial', 15, 'normal'))
            self.game_on = False
            self.game_pause = True
            time.sleep(0.1)
        if self.game_pause and not self.game_on:
            self.game_pause_banner.clear()
            print("Game is un-paused!")
            self.game_pause_banner.write(f"Game is un-paused!", True, align="center", font=('Arial', 15, 'normal'))
            self.game_pause = False
            time.sleep(1)
            self.game_pause_banner.clear()
            self.distance = self.default_distance
            self.game_on = True

    def game_loop(self, snakes):
        while True:
            time.sleep(0.1)
            while self.game_on:
                self.check_bounds()
                self.check_self_bounds()
                self.snake_move(self.snakes, self.distance)
                self.screen.listen()
                self.screen.onkey(key="Up", fun=self.snake_direction_up)
                self.screen.onkey(key="Down", fun=self.snake_direction_down)
                self.screen.onkey(key="Left", fun=self.snake_direction_left)
                self.screen.onkey(key="Right", fun=self.snake_direction_right)
                self.screen.onkey(key="space", fun=self.snake_pause)
                if self.snake_head.distance(self.food) < self.food_threshold:
                    print("You ate food!")
                    self.score_banner.clear()
                    self.score += 1
                    if self.score > self.high_score:
                        self.high_score = self.score
                    self.score_board()
                    self.move_food()
                    self.snake_extend()

    def snake_food(self):
        self.food = Turtle()
        self.food.shape("circle")
        self.food.penup()
        self.food.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.food.color("white")
        self.food.speed("fastest")
        self.food.goto(x=random.randint(-1 * int(self.screen_size[0] / 2 * self.shift)
                                        , int(self.screen_size[0] / 2 * self.shift))
                       , y=random.randint(-1 * int(self.screen_size[1] / 2 * self.shift),
                                          int(self.screen_size[1] / 2 * self.shift)))
        self.screen_update(self.delay_time)

    def move_food(self):
        self.food.goto(
            x=random.randint(-1 * int(self.screen_size[0] / 2 * self.shift), int(self.screen_size[0] / 2 * self.shift))
            , y=random.randint(-1 * int(self.screen_size[1] / 2 * self.shift),
                               int(self.screen_size[1] / 2 * self.shift)))
        self.screen_update(self.delay_time)

    def check_bounds(self):
        if self.snake_head.xcor() >= int((self.screen_size[0] / 2) * 0.85) or self.snake_head.xcor() <= \
                -1 * int((self.screen_size[0] / 2) * 0.85) or self.snake_head.ycor() >= \
                int((self.screen_size[1] / 2) * 0.85) or self.snake_head.ycor() <= \
                -1 * int((self.screen_size[1] / 2) * 0.85):
            print("Game over!")
            self.game_on = False
            self.score_banner.goto(x=0, y=0)
            self.box.hideturtle()
            self.score_banner.write(f"Game Over! Press space to play again..", True, align="center",
                                    font=('Arial', 15, 'normal'))

    def check_self_bounds(self):
        for i in self.snakes:
            if i == self.snake_head:
                continue
            else:
                if i.distance(self.snake_head) < 10:
                    print("Game over!")
                    self.game_on = False
                    self.score_banner.goto(x=0, y=0)
                    self.box.hideturtle()
                    self.score_banner.write(f"Game Over! Press space to play again..", True, align="center",
                                            font=('Arial', 15, 'normal'))

    def snake_extend(self):
        self.snake = Turtle()
        self.snake.penup()
        self.snake.shape("square")
        self.snake.color("white")
        self.snake.goto(self.snakes[-1].position())
        self.snakes.append(self.snake)


snake = Snake(distance=20, delay_time=0.05, scree_size=(600, 600), initial_len=3)

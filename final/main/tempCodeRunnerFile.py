    global player_lives, enemies_killed
        for laser in laser_group:
            if is_collision(self.rect.right, laser.rect.left, self.rect.left, laser.rect.right, laser, self.rect, laser.rect, scroll, self.jump) and laser.is_player != True:
                laser.kill()
                player_lives -= 1
                enemies_killed += 1  # Increment the killed enemies counter
                print("C:/Users/ADMIN/Downloads/main(2)/main/Got hit!")
                if player_lives <= 0:
                    # Handle game over logic here if necessary
                    pass
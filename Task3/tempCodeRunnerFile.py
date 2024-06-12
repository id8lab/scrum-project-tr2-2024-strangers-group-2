# Scale images to fit the screen if necessary (optional)
sky_cloud = pygame.transform.scale(sky_cloud, (screen_width, screen_height))
mountain = pygame.transform.scale(mountain, (screen_width, screen_height))

# Reduce the height of the pine images
pine_height = screen_height // 2  # Adjust this value as needed
pine1 = pygame.transform.scale(pine1, (screen_width, pine_height))
pine2 = pygame.transform.scale(pine2, (screen_width, pine_height))
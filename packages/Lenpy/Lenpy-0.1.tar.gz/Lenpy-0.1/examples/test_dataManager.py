
import pygame
import lenpy, sys

# Crea una variable, importando el Data Manager, coloca un nombre y un formato para el archivo
save_load = lenpy.data.Manager("Test",".dat")

# Define la variable que será la encargada de recibir los datos
entities = save_load.Load_game_data(["entities"], [[]])

while True:

    lenpy.config.screen.fill(pygame.Color("#000000"))

    for event in pygame.event.get():

        if event.type == pygame.QUIT: 

            # Guarda los datos del juego, usa los datos de la variable 'entities' y los guarda en el archivo 'entities', el nombre del
            # archivo no tiene que ser el mismo de la variable.

            save_load.Save_game_data([entities], ["entities"])
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            # Agrega la posición del mouse a la variable
            entities.append(mouse_pos)

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_0:

                # Toca 0 y se borrara la data

                save_load.delete_game_data([entities], ["entities"])

    for entity in entities:

        # Dibuja los circulos en base a las posiciones guardadas en 'entities'

        pygame.draw.circle(lenpy.config.screen, (255, 0, 0), (entity[0], entity[1]), 10)

    pygame.display.update()
    
    lenpy.config.clock.tick(60)
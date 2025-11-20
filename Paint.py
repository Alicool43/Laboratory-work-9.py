import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    radius = 15
    mode = 'blue'
    points = []
    
    draw_mode = 'line'
    start_pos = None

    while True:
        pressed = pygame.key.get_pressed()
        
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held: return
                if event.key == pygame.K_F4 and alt_held: return
                if event.key == pygame.K_ESCAPE: return

                if event.key == pygame.K_r: mode = 'red'
                elif event.key == pygame.K_g: mode = 'green'
                elif event.key == pygame.K_b: mode = 'blue'
                elif event.key == pygame.K_y: mode = 'yellow'
                elif event.key == pygame.K_p: mode = 'purple'

                elif event.key == pygame.K_1: draw_mode = 'rect'
                elif event.key == pygame.K_2: draw_mode = 'circle'
                elif event.key == pygame.K_l: draw_mode = 'line'
                elif event.key == pygame.K_e: draw_mode = 'eraser'
                elif event.key == pygame.K_c: screen.fill((0, 0, 0))

                elif event.key == pygame.K_3: draw_mode = 'square'
                elif event.key == pygame.K_4: draw_mode = 'right_triangle'
                elif event.key == pygame.K_5: draw_mode = 'equilateral_triangle'
                elif event.key == pygame.K_6: draw_mode = 'rhombus'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    radius = min(200, radius + 1)
                    start_pos = event.pos
                elif event.button == 3:
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and start_pos:
                    end_pos = event.pos
                    draw_shape(screen, start_pos, end_pos, radius, mode, draw_mode)
                    start_pos = None
            
            if event.type == pygame.MOUSEMOTION:
                position = event.pos
                if draw_mode == 'line':
                    points.append(position)
                    points = points[-256:]
                elif draw_mode == 'eraser' and pressed[0]:
                    pygame.draw.circle(screen, (0, 0, 0), position, radius)

        if draw_mode == 'line':
            screen.fill((0, 0, 0))
            for i in range(len(points) - 1):
                drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)

        pygame.display.flip()
        clock.tick(60)

def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))

    if color_mode == 'blue': color = (c1, c1, c2)
    elif color_mode == 'red': color = (c2, c1, c1)
    elif color_mode == 'green': color = (c1, c2, c1)
    elif color_mode == 'purple': color = (c2, c1, c2)
    elif color_mode == 'yellow': color = (c2, c2, c1)

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    for i in range(iterations):
        progress = i / iterations
        x = int(start[0] * (1 - progress) + end[0] * progress)
        y = int(start[1] * (1 - progress) + end[1] * progress)
        pygame.draw.circle(screen, color, (x, y), width)

def draw_shape(screen, start, end, width, color_mode, mode):
    color = {
        'blue': (0, 0, 255),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'yellow': (255, 255, 0),
        'purple': (255, 0, 255)
    }.get(color_mode, (255, 255, 255))

    x1, y1 = start
    x2, y2 = end

    draw_width = 0

    if mode == 'rect':
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2-x1), abs(y2-y1))
        pygame.draw.rect(screen, color, rect, draw_width)

    elif mode == 'circle':
        radius = int(((x2-x1)**2 + (y2-y1)**2) ** 0.5)
        pygame.draw.circle(screen, color, start, radius, draw_width)


    elif mode == 'square':
        side = max(abs(x2 - x1), abs(y2 - y1))
        rect = pygame.Rect(x1, y1, side, side)
        pygame.draw.rect(screen, color, rect, draw_width)

    elif mode == 'right_triangle':
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(screen, color, points, draw_width)

    elif mode == 'equilateral_triangle':
        side = abs(x2 - x1)
        height = int(side * (3 ** 0.5) / 2)
        points = [
            (x1, y1),
            (x1 + side, y1),
            (x1 + side / 2, y1 - height)
        ]
        pygame.draw.polygon(screen, color, points, draw_width)

    elif mode == 'rhombus':
        w = abs(x2 - x1)
        h = abs(y2 - y1)
        points = [
            (x1 + w // 2, y1),
            (x1 + w, y1 + h // 2),
            (x1 + w // 2, y1 + h),
            (x1, y1 + h // 2)
        ]
        pygame.draw.polygon(screen, color, points, draw_width)

main()
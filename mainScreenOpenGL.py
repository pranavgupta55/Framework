import pygame
import moderngl
import struct
import math
import time
import sys
import array

# Import Framework Utilities (Assumes these files exist in the directory)
from text import drawText
from fontDict import fonts

# --- SHADER LOADING UTILITY ---
def load_shader(ctx, vert_path, frag_path):
    with open(vert_path, 'r') as f:
        vert_src = f.read()
    with open(frag_path, 'r') as f:
        frag_src = f.read()
    return ctx.program(vertex_shader=vert_src, fragment_shader=frag_src)

# --- COLORS (From Framework) ---
class Endesga:
    maroon_red = [87, 28, 39]
    lighter_maroon_red = [127, 36, 51]
    dark_green = [9, 26, 23]
    light_brown = [191, 111, 74]
    black = [19, 19, 19]
    grey_blue = [66, 76, 110]
    cream = [237, 171, 80]
    white = [255, 255, 255]
    greyL = [200, 200, 200]
    grey = [150, 150, 150]
    greyD = [100, 100, 100]
    greyVD = [50, 50, 50]
    very_light_blue = [199, 207, 221]
    my_blue = [32, 36, 46]
    debug_red = [255, 96, 141]

# --- INIT ---
pygame.init()

# 1. Setup Pygame with OpenGL flags
screen = pygame.display.set_mode((0, 0), pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN)
info = pygame.display.Info()
WINDOW_WIDTH, WINDOW_HEIGHT = info.current_w, info.current_h

# 2. Create ModernGL Context
ctx = moderngl.create_context()
ctx.enable(moderngl.BLEND) # Enable transparency blending

# 3. Game Logic Variables (From Framework/main_screen.py)
clock = pygame.time.Clock()
fps = 60
scaleDownFactor = 3 # The pixel art scaling factor

# Virtual Resolution (Low Res)
VIRTUAL_W = int(WINDOW_WIDTH / scaleDownFactor)
VIRTUAL_H = int(WINDOW_HEIGHT / scaleDownFactor)

# Pygame Surfaces (CPU side)
# We draw to these, then upload to GPU
screen2 = pygame.Surface((VIRTUAL_W, VIRTUAL_H)).convert_alpha() # Main game layer
screenUI = pygame.Surface((VIRTUAL_W, VIRTUAL_H)).convert_alpha() # UI layer

# 4. OpenGL Textures
# We create a texture to hold our Pygame surface data
game_texture = ctx.texture((VIRTUAL_W, VIRTUAL_H), 4) # 4 components (RGBA)
# NEAREST filter ensures crisp pixel art when upscaled
game_texture.filter = (moderngl.NEAREST, moderngl.NEAREST) 
game_texture.swizzle = 'BGRA' # Pygame uses BGRA usually, ModernGL needs to know

# 5. Geometry (Full Screen Quad)
# Format: x, y, u, v
quad_buffer = ctx.buffer(data=array.array('f', [
    # Position (x,y)   # UV Coords (u,v)
    -1.0, 1.0,         0.0, 0.0,  # Top Left
    -1.0, -1.0,        0.0, 1.0,  # Bottom Left
    1.0, 1.0,          1.0, 0.0,  # Top Right
    1.0, -1.0,         1.0, 1.0,  # Bottom Right
]))

# 6. Load Shaders
# Ensure you create the 'shaders' folder and files provided below
prog = load_shader(ctx, 'shaders/basic.vert', 'shaders/basic.frag')

# Vertex Array Object
# We map the buffer data to the 'in_vert' and 'in_text' attributes in the vertex shader
vao = ctx.vertex_array(prog, [
    (quad_buffer, '2f 2f', 'in_vert', 'in_text')
])

# Font Setup (Adaptive to scale)
# Note: fonts dict must be present in fontDict.py
try:
    montserratRegularAdaptive = fonts[f"regular{int(25 / (scaleDownFactor ** (1 / 1.5)))}"]
except KeyError:
    # Fallback if specific size missing
    montserratRegularAdaptive = pygame.font.SysFont("Arial", 20)

# Loop Variables
timer = 0
shake = [0, 0]
oscillating_random_thing = 0
toggle = True
click = False
last_time = time.time()
running = True

# --- MAIN LOOP ---
while running:
    # A. Time Management
    dt = time.time() - last_time
    dt *= fps
    last_time = time.time()
    
    # B. Input Handling
    mx, my = pygame.mouse.get_pos()
    # Scale mouse pos to virtual screen for logic checks
    vmx, vmy = mx / scaleDownFactor, my / scaleDownFactor
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        if event.type == pygame.MOUSEBUTTONUP:
            click = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                toggle = not toggle

    # C. Logic
    timer -= 1 * dt
    oscillating_random_thing += math.pi / fps * dt
    
    # D. Rendering to Pygame Surfaces
    # 1. Fill Background (Regular Blue)
    screen2.fill(Endesga.my_blue)
    screenUI.fill((0, 0, 0, 0)) # Clear UI (Transparent)

    # 2. Draw UI Elements (From Framework logic)
    if toggle:
        items = {round(clock.get_fps()): None}
        for i, label in enumerate(items.keys()):
            string_val = str(label)
            if items[label] is not None:
                string_val = f"{items[label]}: " + string_val
            
            # Use Framework drawText
            drawText(screenUI, Endesga.debug_red, montserratRegularAdaptive, 
                     5, VIRTUAL_H - (30 + 25 * i) / (scaleDownFactor ** (1 / 1.8)), 
                     string_val, Endesga.black, 
                     int(3 / scaleDownFactor) + int(3 / scaleDownFactor) < 1, 
                     antiAliasing=False)
        
        # Custom Cursor
        pygame.mouse.set_visible(False)
        pygame.draw.circle(screenUI, Endesga.black, (vmx + 1, vmy + 1), 2, 1)
        pygame.draw.circle(screenUI, Endesga.white, (vmx, vmy), 2, 1)

    # 3. Composite Pygame Surfaces
    # Blit UI onto the Game Screen
    screen2.blit(screenUI, (0, 0))

    # E. OpenGL Rendering
    # 1. Convert Pygame Surface to Byte Data
    # Note: ModernGL expects bytes. We use RGBA.
    texture_data = pygame.image.tobytes(screen2, 'RGBA')
    
    # 2. Write to GPU Texture
    game_texture.write(texture_data)
    
    # 3. Bind Texture to Unit 0
    game_texture.use(location=0)
    
    # 4. Clear Screen & Render Quad
    ctx.clear(0.0, 0.0, 0.0) # Clear physical screen
    vao.render(mode=moderngl.TRIANGLE_STRIP)
    
    # 5. Swap Buffers
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()

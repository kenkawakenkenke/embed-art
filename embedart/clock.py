from PIL import Image,ImageDraw
import math

def draw_clockborder(draw, center, length, line_thickness, color):
    draw.ellipse(
        (
            center[0] - length,
            center[1] - length,
            center[0] + length,
            center[1] + length,
        ),
        outline=color,
        width=line_thickness
    )

def draw_hand(draw, center, angle, length, line_thickness, color):
    toPoint = (
        int(center[0] + length * math.sin(angle)),
        int(center[1] - length * math.cos(angle)),
    )
    draw.line([center,toPoint],
        fill=color,
        width=line_thickness
    )

def draw_clock(time,
                width=512,
                height=512,
                clock_size_prop=0.9,
                base_circle_thickness = 0, 
                base_hour_hand_thickness = 15,
                base_minute_hand_thickness = 10, 
                colorFill="white", 
                colorStroke="black"):
    (hours, mins) = divmod(time, 60)

    # width, height = 512, 512
    clock_img = Image.new("RGB", (width, height), colorFill)
    draw = ImageDraw.Draw(clock_img)
    shorter = min(width, height)
    circle_radius = int(shorter//2 * clock_size_prop)
    circle_thickness = int(base_circle_thickness * circle_radius / 512)
    hour_hand_thickness = int(base_hour_hand_thickness * circle_radius / 512)
    minute_hand_thickness = int(base_minute_hand_thickness * circle_radius / 512)
    circle_center = (width//2, height//2)
    
    if circle_thickness > 0:
        draw_clockborder(draw, circle_center, circle_radius, circle_thickness, colorStroke)
    draw_hand(draw, circle_center, (hours+mins/60)/12*math.pi*2, int(circle_radius*0.75), hour_hand_thickness, colorStroke)
    draw_hand(draw, circle_center, mins/60*math.pi*2, int(circle_radius*0.9), minute_hand_thickness, colorStroke)

    return clock_img

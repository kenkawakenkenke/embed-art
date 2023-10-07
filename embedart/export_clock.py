from generate import generate
from image import display_image, export_image, export_movie, read_image
from clock import draw_clock
from prompt import DEFAULT_OIL_PAINTING, DEFAULT_PHOTO

def compute_clock(project, prompt, seed, time,
                width,
                height,
                circle_thickness, 
                hour_hand_thickness,
                minute_hand_thickness, 
                colorFill,
                colorStroke,
                show=False,
                forceRecompute=True):
    file_name = 'output/{}_{}/out{}.jpg'.format(project, width, time)
    output_image = None
    if not forceRecompute:
        output_image = read_image(file_name)
    if output_image == None:
        input_image = draw_clock(
            time,
            width,
            height,
            circle_thickness,
            hour_hand_thickness,
            minute_hand_thickness,
            colorFill,
            colorStroke)    
        if show:
            input_image.show()
        output_image = generate(prompt, seed, input_image, width, height)

    if show:
        output_image.show()
    display_image(output_image)
    export_image(output_image, file_name)
    return output_image

if __name__ == '__main__':
    # Testing size
    width = 512
    height = width

    # Prod size
    width = 768
    height = width * 768 // 1024

    # Force export even if a file already exists.
    recomputeAll = True
    # recomputeAll = False # Uncomment to only compute incrementally.

    fps = 4

    colorFill="white"
    colorStroke = "black"
    circle_thickness = 0
    hour_hand_thickness = 15
    minute_hand_thickness = 10
    seed = 135

    # basePrompt = ['beautiful forest','trees','flowing stream','rocks']+DEFAULT_PHOTO
    # # basePrompt = ['beautiful forest','trees','flowing stream,rocks','waterfall']+DEFAULT_OIL_PAINTING
    # project="forest"
    # colorFill="lightgray"
    # colorStroke = "black"
    # hour_hand_thickness = 15
    # minute_hand_thickness = 10
    # seed = -1

    # basePrompt = ['beautiful factory nightscape', 'desolate', 'industrial', 'pipes']+DEFAULT_PHOTO
    # project="factory"
    # colorFill="black"
    # colorStroke = "white"
    # hour_hand_thickness = 15
    # minute_hand_thickness = 10
    # seed = -1

    # basePrompt = ['beautiful aerial photography','from a helicopter','masterpiece','sharp focus','best quality','ultra detailed','wide-angle lens']
    # colorFill="white"
    # colorStroke = "darkgray"
    # project="aerial"
    # hour_hand_thickness = 15
    # minute_hand_thickness = 10
    # seed = -1

    # basePrompt = ['lightning bolt striking a cityscape']+DEFAULT_PHOTO
    # project="lightning"
    # colorFill="black"
    # colorStroke = "white"
    # hour_hand_thickness = 5
    # minute_hand_thickness = 5
    # seed = -1

    # basePrompt = ['2D game background art of a magical forest','trees','flowing stream,rocks','waterfall'] + DEFAULT_OIL_PAINTING
    # project="magic"
    # colorFill="black"
    # colorStroke = "gray"
    # hour_hand_thickness = 10
    # minute_hand_thickness = 10
    # seed = -1

    # basePrompt = ['petite european town', 'beautiful']+DEFAULT_PHOTO
    # project="europe"
    # colorFill="white"
    # colorStroke = "black"
    # hour_hand_thickness = 15
    # minute_hand_thickness = 10
    # seed = -1

    # basePrompt = ['breathtaking landscape', 'must-see', 'beautiful']+DEFAULT_PHOTO
    # project="landscape"
    # colorFill="lightgray"
    # colorStroke = "black"
    # hour_hand_thickness = 15
    # minute_hand_thickness = 10
    # seed = -1

    # basePrompt = ['worlds most scenic roadtrip', 'amazing']+DEFAULT_PHOTO
    # project="highway"
    # colorFill="black"
    # colorStroke = "white"
    # hour_hand_thickness = 15
    # minute_hand_thickness = 10
    # seed = -1

    # basePrompt = ['backstreet', 'night', 'beautiful']+DEFAULT_PHOTO
    # project="backstreet"
    # colorFill="black"
    # colorStroke = "lightgray"
    # hour_hand_thickness = 15
    # minute_hand_thickness = 10
    # seed = -1

    # basePrompt = ['window with cracked class']+DEFAULT_PHOTO
    # project="crackedglass"
    # colorFill="white"
    # colorStroke = "gray"
    # hour_hand_thickness = 5
    # minute_hand_thickness = 5
    # seed = -1

    basePrompt = ['beautiful island beach']+DEFAULT_PHOTO
    project="beach"
    colorFill="white"
    colorStroke = "gray"
    hour_hand_thickness = 8
    minute_hand_thickness = 8
    seed = -1

    # time = 4*60+44
    # compute_clock("clock", create_prompt(time), time, show=True)
    # exit()

    hour_hand_thickness *= height//512
    minute_hand_thickness *= height//512

    images = []
    for time in range(1440//2):
        prompt = basePrompt
        # prompt = prompt + prompt_time(time)
        print(time, prompt)

        image = compute_clock(
            project,
            prompt,
            seed,
            time,
            width,
            height, 
            circle_thickness, 
            hour_hand_thickness,
            minute_hand_thickness, 
            colorFill,
            colorStroke,
            forceRecompute = recomputeAll)
        images.append(image)
        if len(images)<20 or len(images) % 100 == 0:
            print("Exporting movie...")
            export_movie(images, fps, 'output/out_{}_{}.mp4'.format(project, width))
    
    export_movie(images, fps, 'output/out_{}_{}.mp4'.format(project, width))



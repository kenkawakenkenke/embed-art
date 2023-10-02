from embedart.generate import generate
from embedart.image import display_image, export_image, export_movie
from embedart.clock import draw_clock
from embedart.prompt import DEFAULT_OIL_PAINTING, DEFAULT_PHOTO

def compute_clock(project, prompt, seed, time,
                width,
                height,
                circle_thickness, 
                hour_hand_thickness,
                minute_hand_thickness, 
                colorFill,
                colorStroke,
                show=False):
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
    export_image(output_image, 'output/{}_{}/out{}.jpg'.format(project, width, time))
    return output_image

if __name__ == '__main__':
    width = 512
    height = width
    # width = 1024
    # height = 768
    fps = 4

    colorFill="white"
    colorStroke = "black"
    circle_thickness = 0
    hour_hand_thickness = 15
    minute_hand_thickness = 10
    seed = 135

    # basePrompt = ['beautiful forest','trees','flowing stream,rocks','waterfall']+DEFAULT_PHOTO
    # # basePrompt = ['beautiful forest','trees','flowing stream,rocks','waterfall']+DEFAULT_OIL_PAINTING
    # project="forest"
    # colorFill="white"
    # colorStroke = "gray"
    # hour_hand_thickness = 15
    # minute_hand_thickness = 10
    # seed = -1

    # basePrompt = ['beautiful aerial photography','from a helicopter','highly detailed','sharp focus']
    # colorFill="white"
    # colorStroke = "darkgray"
    # project="aerial"
    # hour_hand_thickness = 15
    # minute_hand_thickness = 10
    # seed = -1

    basePrompt = ['lightning bolt striking a cityscape']+DEFAULT_PHOTO
    project="lightning"
    colorFill="black"
    colorStroke = "white"
    hour_hand_thickness = 5
    minute_hand_thickness = 5
    seed = -1

    # basePrompt = ['2D game background art of a magical forest','trees','flowing stream,rocks','waterfall'] + DEFAULT_OIL_PAINTING
    # project="magic"
    # colorFill="black"
    # colorStroke = "gray"
    # hour_hand_thickness = 10
    # minute_hand_thickness = 10
    # seed = -1

    # basePrompt = ['beautiful European town']+DEFAULT_PHOTO
    # project="london"
    # colorFill="black"
    # colorStroke = "gray"
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

    # basePrompt = ['Photo of a beach','palm trees']
    # project="beach"
    # colorFill="white"
    # colorStroke = "darkgray"
    # hour_hand_thickness = 15
    # minute_hand_thickness = 10
    # seed = -1

    # time = 4*60+44
    # compute_clock("clock", create_prompt(time), time, show=True)
    # exit()

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
            colorStroke)
        images.append(image)
        if len(images)<30 or len(images) % 30 == 0:
            print("Exporting movie...")
            export_movie(images, fps, 'output/out_{}_{}.mp4'.format(project, width))
    
    export_movie(images, fps, 'output/out_{}_{}.mp4'.format(project, width))



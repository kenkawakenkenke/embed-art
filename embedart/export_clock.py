from generate import generate
from image import display_image, export_image, export_movie, read_image
from clock import draw_clock
from prompt import DEFAULT_OIL_PAINTING, DEFAULT_PHOTO
import argparse

parser = argparse.ArgumentParser(description="Export clocks")
parser.add_argument('--width', type=int, default=512, help="Width of the output")
parser.add_argument('--height', type=int, default=512, help="Height of the output")
parser.add_argument('--aspectRatio', type=str, default="", help="Optional:(square|smartphone|laptop) Sets the height to the to the given aspect ratio given the width")
parser.add_argument('--forceRecomputeAll', type=bool, default=True, help="Force recompute all")
parser.add_argument('--fps', type=int, default=4, help="fps for the exported movie")
parser.add_argument('--project', type=str, default="", help="Optional: the project to compute. If not set, computes all projects")

class Scenario:
    def __init__(self,
                 project,
                 prompt,
                 base_circle_thickness = 0, 
                 base_hour_hand_thickness = 15,
                 base_minute_hand_thickness = 10,
                 colorFill = "white",
                 colorStroke = "black",
                 seed = -1):
        self.project = project
        self.prompt = prompt
        self.seed = seed
        self.width = width
        self.height = height
        self.base_circle_thickness = base_circle_thickness
        self.base_hour_hand_thickness = base_hour_hand_thickness
        self.base_minute_hand_thickness = base_minute_hand_thickness
        self.colorFill = colorFill
        self.colorStroke = colorStroke

    def compute_clock(self,
                       time, 
                       width, 
                       height,
                       show=False,
                       forceRecompute=True):
        file_name = 'output/{}_{}_{}/out{}.jpg'.format(self.project, width, height, time)
        output_image = None
        if not forceRecompute:
            output_image = read_image(self.file_name)
        if output_image == None:
            input_image = draw_clock(
                time,
                width,
                height,
                self.base_circle_thickness,
                self.base_hour_hand_thickness,
                self.base_minute_hand_thickness,
                self.colorFill,
                self.colorStroke)
            if show:
                input_image.show()
            output_image = generate(self.prompt, self.seed, input_image, width, height)

        if show:
            output_image.show()
        display_image(output_image)
        export_image(output_image, file_name)
        return output_image
    
    def export_movie(self, images, fps, width):
        export_movie(images, fps, 'output/out_{}_{}_{}.mp4'.format(self.project, width, height))


if __name__ == '__main__':
    args = parser.parse_args()

    width = args.width
    height = args.height
    recomputeAll = args.forceRecomputeAll
    fps = args.fps
    if args.aspectRatio=="square":
        height = width
    elif args.aspectRatio=="smartphone":
        height = width * 960 // 640
    elif args.aspectRatio=="laptop":
        height = width * 1024 // 768

    print(f"Args {width}x{height} Recompute all:{recomputeAll} FPS:{fps}")

    scenarios = [
        Scenario(project = "forest",
                 prompt = ['beautiful forest','trees','flowing stream','rocks']+DEFAULT_PHOTO,
                 base_hour_hand_thickness = 15,
                 base_minute_hand_thickness = 10, 
                 colorFill = "white",
                 colorStroke = "gray"),

        Scenario(project = "nightforest",
                 prompt = ['beautiful forest at night','trees','flowing stream','rocks']+DEFAULT_PHOTO,
                 base_hour_hand_thickness = 15,
                 base_minute_hand_thickness = 10, 
                 colorFill = "black",
                 colorStroke = "gray"),

        Scenario(project = "factory",
                 prompt = ['beautiful factory nightscape', 'desolate', 'industrial', 'pipes']+DEFAULT_PHOTO,
                 base_hour_hand_thickness = 15,
                 base_minute_hand_thickness = 10, 
                 colorFill = "black",
                 colorStroke = "white"),

        Scenario(project = "aerial",
                 prompt = ['beautiful aerial photography','from a helicopter','masterpiece','sharp focus','best quality','ultra detailed','wide-angle lens'],
                 base_hour_hand_thickness = 15,
                 base_minute_hand_thickness = 10, 
                 colorFill = "white",
                 colorStroke = "darkgray"),

        Scenario(project = "lightning",
                 prompt = ['lightning bolt striking a cityscape']+DEFAULT_PHOTO,
                 base_hour_hand_thickness = 5,
                 base_minute_hand_thickness = 5, 
                 colorFill = "black",
                 colorStroke = "white"),

        Scenario(project = "magic",
                 prompt = ['2D game background art of a magical forest','trees','flowing stream,rocks','waterfall'] + DEFAULT_OIL_PAINTING,
                 base_hour_hand_thickness = 10,
                 base_minute_hand_thickness = 10, 
                 colorFill = "black",
                 colorStroke = "gray"),

        Scenario(project = "europe",
                 prompt = ['petite european town', 'beautiful']+DEFAULT_PHOTO,
                 base_hour_hand_thickness = 15,
                 base_minute_hand_thickness = 10, 
                 colorFill = "black",
                 colorStroke = "black"),

        Scenario(project = "landscape",
                 prompt = ['breathtaking landscape', 'must-see', 'beautiful']+DEFAULT_PHOTO,
                 base_hour_hand_thickness = 15,
                 base_minute_hand_thickness = 10, 
                 colorFill = "lightgray",
                 colorStroke = "black"),

        Scenario(project = "highway",
                 prompt = ['worlds most scenic roadtrip', 'amazing']+DEFAULT_PHOTO,
                 base_hour_hand_thickness = 15,
                 base_minute_hand_thickness = 10, 
                 colorFill = "black",
                 colorStroke = "white"),

        Scenario(project = "backstreet",
                 prompt = ['backstreet', 'night', 'beautiful']+DEFAULT_PHOTO,
                 base_hour_hand_thickness = 15,
                 base_minute_hand_thickness = 10, 
                 colorFill = "black",
                 colorStroke = "lightgray"),

        # Scenario(project = "crackedglass",
        #          prompt = ['window with cracked glass', 'beautiful', 'transparency', 'clean']+DEFAULT_PHOTO,
        #          base_hour_hand_thickness = 5,
        #          base_minute_hand_thickness = 5, 
        #          colorFill = "white",
        #          colorStroke = "gray"),

        Scenario(project = "beach",
                 prompt = ['beautiful beach with palm trees', 'summer', 'island', 'cinematic']+DEFAULT_PHOTO,
                #  base_hour_hand_thickness = 8,
                #  base_minute_hand_thickness = 8, 
                 base_hour_hand_thickness = 15,
                 base_minute_hand_thickness = 10, 
                 colorFill = "white",
                 colorStroke = "gray"),
    ]

    for scenario in scenarios:
        if args.project != "" and args.project != scenario.project:
            continue

        images = []
        for time in range(1440//2):
            (hours, mins) = divmod(time, 60)
            print(f"{hours:02d}:{mins:02d} {scenario.prompt}")
            images.append(scenario.compute_clock(time, width, height, forceRecompute = recomputeAll))
            if len(images)<20 or len(images) % 100 == 0:
                print("Exporting movie...")
                scenario.export_movie(images, fps, width)
        
        scenario.export_movie(images, fps, width)
        print(f"Done {scenario.project}")


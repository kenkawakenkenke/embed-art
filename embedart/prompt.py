DEFAULT_NEGATIVE_PROMPTS = ['ugly','tiling','poorly drawn hands','poorly drawn feet','poorly drawn face','out of frame','extra limbs','disfigured','deformed','body out of frame','bad anatomy','watermark','signature','cut off','low contrast','underexposed','overexposed','bad art','beginner','amateur','distorted face','blurry','draft','grainy',
                            'worst quality','normal quality','low quality','low res','blurry','text','watermark','logo','banner','extra digits','cropped','jpeg artifacts','signature','username','error','duplicate','ugly','disgusting']

DEFAULT_OIL_PAINTING = ['oil painting','hyperrealistic','artstation','highly detailed',' sharp focus','cinematic lighting']

DEFAULT_PHOTO = ['professional photograph', 'masterpiece','best quality','ultra detailed','wide-angle lens']

def prompt_time(time):
    (hour, min) = divmod(time, 60)
    if hour < 3:
        description = "midnight, moonlight"
    elif hour < 6:
        description = "in the early morning, misty"
    elif 6 <= hour < 12:
        description = "in the morning, sunlight"
    elif hour == 12:
        description = "noon, sunlight"
    elif hour < 18:
        description = "in the afternoon"
    else:  # hour < 24
        description = "in the evening"
    timeDescription="{:02}:{:02} {}".format(hour, min, description)
    return [timeDescription]
    # promptList.append(timeDescription)
    # return basePrompt.format(timeDescription)
    # timeDescription="night time"

def promptsToString(promptList):
    return ",".join(promptList)


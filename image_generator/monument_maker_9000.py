 # Program by OK_Diamond
from PIL import Image as pil # pip install pillow
from os import listdir

def merge(monument: pil.Image, frame: pil.Image) -> pil.Image:
    merged_image = pil.new("RGBA", (300, 150))
    merged_image.paste(monument, (5, 5))
    merged_image.paste(frame, mask=frame)
    return merged_image

def main(input_location: str, output_location: str, output_file_type = "dds") -> None:
    template = pil.open(f"{input_location}template.dds")
    for i in listdir(f"{input_location}input"):
        #print("i", i)
        monument = pil.open(f"{input_location}input\\{i}")
        #print("size", monument.size)
        if monument.width < monument.height*2:
            offset = int((monument.height*2-monument.width)/4)
            monument = monument.crop((0, offset, monument.width, monument.height-offset))
            #print("Too tall", offset)
        elif monument.width > monument.height*2:
            offset = int((monument.width-monument.height*2)/2)
            monument = monument.crop((offset, 0, monument.width-offset, monument.height))
            #print("Too wide", offset)

        monument = monument.resize((300, 150))
        monument = monument.crop((5, 5, 295, 145))

        final_image = merge(monument, template)
        file_name = i[0:i.find(".")]
        final_image.save(f"{output_location}{file_name}.{output_file_type}")
        monument.close()
    template.close()

if __name__ == "__main__":
    main("", "output\\", "dds")

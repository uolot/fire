from PIL import Image
import glob
import datetime

images = [
    Image.open(image)
    for image in glob.glob('export/*.png')
]

today = datetime.date.today().strftime('%Y-%m-%d')
gif = images[0]
gif.save(
    fp=f'fire-{today}.gif',
    format='gif',
    save_all=True,
    append_images=images[1:]
)

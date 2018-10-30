import datetime
import glob
import imageio

filenames = sorted(glob.glob('export/*.png'))

images = [imageio.imread(fn) for fn in filenames]

now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
fname = f'gifs/fire-{now}.gif'
imageio.mimsave(fname, images, fps=15, subrectangles=True)

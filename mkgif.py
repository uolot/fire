import datetime
import glob
import imageio

filenames = sorted(glob.glob('export/*.png'))

images = [imageio.imread(fn) for fn in filenames]

today = datetime.date.today().strftime('%Y-%m-%d')
fname = f'export/fire-{today}.gif'
imageio.mimsave(fname, images)

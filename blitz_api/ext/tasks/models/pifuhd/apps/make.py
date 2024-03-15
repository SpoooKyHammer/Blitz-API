
from .recon import reconWrapper


def make_obj(image_path: str, resolution: int=512):
    """
    Creates a 3d object from image and it's rect.
    

    Parameters
    ----------
        image_path: str
            location of the image directory
        resolution: int
            resolution of the image (default is 512)
    """
    resolution = str(resolution)
    start_id = "-1"
    end_id = "-1"
    cmd = ['--dataroot', image_path, '--results_path', image_path,\
            '--loadSize', '1024', '--resolution', resolution, '--load_netMR_checkpoint_path', \
            './blitz_api/ext/tasks/models/pifuhd/checkpoints/pifuhd.pt', '--start_id', start_id, '--end_id', end_id]
    
    reconWrapper(args=cmd, use_rect=True)

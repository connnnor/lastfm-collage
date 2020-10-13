from math import sqrt
import json
import uuid
import sys
import os
import tempfile
from PIL import Image
import pylast
import wget


def do_sizes_match(imgs):
    """Returns if sizes match for all images in list."""
    return len([*filter(lambda x: x.size != x.size[0], imgs)]) > 0


def gen_collage(imgs):
    """Returns grid collage of Images in imgs

    Parameters:
    imgs (list): list of Images of equal size

    Returns:
    Image: Collage
    """
    if not do_sizes_match(imgs):
        raise ValueError("imgs must be the same size")
    n = int(sqrt(len(imgs)))
    size = imgs[0].size[0]
    if n ** 2 != len(imgs):
        # if number of imgs is not a perfect square add a dummy row
        # e.g. if len(imgs) is 6, the last row will be empty
        n += 1

    # paste the imgs onto a grid
    back_im = Image.new("RGB", (size * n, size * n))
    for i, img in enumerate(imgs):
        row = i // n
        col = i % n
        back_im.paste(img, (col * size, row * size))

    return back_im


def download_links(urls, out=None):
    """Download list of URLs and returns list of their filenames."""
    return [wget.download(url, out=out, bar=None) for url in urls if url]


def load_secrets():
    secrets_file = "lastfm-creds.json"
    if os.path.exists(secrets_file):
        with open(secrets_file) as f:
            creds = json.load(f)
    else:
        creds = {}
        try:
            creds["api_key"] = os.environ["LASTFM_API_KEY"].strip()
            creds["api_secret"] = os.environ["LASTFM_API_SECRET"].strip()
        except KeyError:
            print("Missing env vars: LASTFM_API_KEY or LASTFM_API_SECRET.")
    return creds


def gen_album_collage(username, period=pylast.PERIOD_7DAYS, limit=9, dst_dir=None):
    """Create lastfm album collage and return path to image"""
    # api setup
    secrets = load_secrets()
    network = pylast.LastFMNetwork(
        api_key=secrets["api_key"],
        api_secret=secrets["api_secret"],
    )
    # query lastfm for users top albums
    user = network.get_user(username)
    top_albums = user.get_top_albums(period=period, limit=limit)
    cover_art_urls = [x.item.get_cover_image() for x in top_albums]
    # download urls locally to temp directory

    temp_d = tempfile.TemporaryDirectory()
    art_files = download_links(cover_art_urls,temp_d.name)
    art_imgs = [Image.open(f) for f in art_files]
    # create collage
    im = gen_collage(art_imgs)
    dst = (dst_dir or "") + uuid.uuid4().hex + ".png"
    im.save(dst)
    # close temp dir
    temp_d.cleanup()
    return dst


if __name__ == "__main__":
    try:
        gen_album_collage(sys.argv[1])
    except IndexError:
        print("Usage: ./lastfm_collage <lastfm_username>")

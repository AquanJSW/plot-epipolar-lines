#!/usr/bin/python3
r"""Plot horizontal lines through a single image or 2 concatenated images."""

from PIL import Image
from PIL import ImageDraw
import argparse


def argparser():
    parser = argparse.ArgumentParser(
        description="Plot horizontal lines through a single image or 2 "
                    "concatenated images."
    )
    parser.add_argument('-f', '--file', nargs='+', type=str,
                        help='Specifying one or two images.')
    parser.add_argument('-s', '--show', default=False, action='store_true',
                        help='Enable showing output image.')
    parser.add_argument('--disable_write', default=False, action='store_true',
                        help='By default, output image would be saved.')
    parser.add_argument('-o', '--output', default="concatenated.jpg",
                        help="Output file path. This option implies enabling"
                             " write.")
    parser.add_argument('-n', '--number', default=10, type=int,
                        help="The number of plotted lines along y-axis.")
    parser.add_argument('-i', '--interval', default=0, type=int,
                        help='Only valid when input 2 images: the interval '
                             'pixels between images.')
    parser.add_argument('--interval_rgb', nargs=3, type=int, default=[0, 0, 0],
                        help="The padding color of interval.")
    parser.add_argument('--line_rgb', nargs=3, type=int, default=[0, 0, 0],
                        help="The horizontal lines' color.")
    parser.add_argument('--line_width', default=3, type=int,
                        help="Width of horizontal lines.")
    return parser.parse_args()


def main(left_path, right_path, lines, interval):
    imgs = [Image.open(left_path), Image.open(right_path)]
    widths, heights = zip(*(img.size for img in imgs))

    total_width = sum(widths) + interval * (len(imgs) - 1)
    max_height = max(heights)

    img_concat = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for img in imgs:
        img_concat.paste(img, (x_offset, 0))
        x_offset += img.size[0] + interval

    draw = ImageDraw.Draw(img_concat)
    y_offset = 0
    y_interval = int(max_height / (lines + 1))
    for _ in range(lines):
        y_offset += y_interval
        draw.line((0, y_offset, total_width, y_offset), fill=(200, 0, 0),
                  width=2)

    img_concat.save('/home/tjh/nas/tmp/out3_rgb.jpg')


if __name__ == '__main__':
    main('/home/tjh/nas/rdr/NLB_637365613RAS_F0790654NCAM0.JPG',
         '/home/tjh/nas/rdr/NRB_637365613RAS_F0790654NCAM0.JPG',
         10, 10)

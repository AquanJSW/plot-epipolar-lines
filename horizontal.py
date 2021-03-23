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
    parser.add_argument('-f', '--file', nargs='+', type=str, required=True,
                        help='Specifying one or two images.')
    parser.add_argument('-s', '--show', default=False, action='store_true',
                        help='Enable showing output image.')
    parser.add_argument('--disable_output', default=False, action='store_true',
                        help='By default, output image would be saved.')
    parser.add_argument('-o', '--output', default="concatenated.jpg",
                        help="Output file path. This option implies enabling"
                             " write.")
    parser.add_argument('-c', '--line_count', default=10, type=int,
                        help="The number of plotted lines along y-axis.")
    parser.add_argument('-i', '--interval', default=0, type=int,
                        help='Only valid when input 2 images: the interval '
                             'pixels between images.')
    parser.add_argument('--interval_rgb', nargs=3, type=int, default=[0, 0, 0],
                        help="The padding color of interval.")
    parser.add_argument('--line_rgb', nargs=3, type=int, default=[0, 0, 0],
                        help="The horizontal lines' color.")
    parser.add_argument('-w', '--line_width', default=3, type=int,
                        help="Width of horizontal lines.")
    return parser.parse_args()


def main(file: list, line_count: int, interval: int,
         interval_rgb: list, line_rgb: list, line_width: int) -> Image.Image:
    images = [Image.open(image) for image in file]
    widths, heights = zip(*(images.size for images in images))

    total_width = sum(widths) + interval * (len(images) - 1)
    max_height = max(heights)

    concatenated = Image.new('RGB', (total_width, max_height))

    offset = 0
    if interval:
        image_interval = Image.new('RGB', (interval, max_height),
                                   tuple(interval_rgb))
    for image in images:
        concatenated.paste(image, (offset, 0))
        if interval:
            concatenated.paste(image_interval, (offset + image.size[0], 0))
        offset += image.size[0] + interval

    draw = ImageDraw.Draw(concatenated)
    offset = 0
    line_interval = int(max_height / (line_count + 1))
    if line_width >= line_interval:
        raise Warning("Too wide line.")
    for _ in range(line_count):
        offset += line_interval
        draw.line((0, offset, total_width, offset), fill=tuple(line_rgb),
                  width=line_width)
    return concatenated


if __name__ == '__main__':
    args = argparser()
    output_image = main(file=args.file,
                        line_count=args.line_count,
                        interval=args.interval,
                        interval_rgb=args.interval_rgb,
                        line_width=args.line_width,
                        line_rgb=args.line_rgb,
                        )
    if args.show:
        output_image.show("Concatenated")
    if not args.disable_output:
        output_image.save(args.output)

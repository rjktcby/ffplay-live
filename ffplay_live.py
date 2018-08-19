import sys
import ffmpeg
from argparse import ArgumentParser
from chunked_reader import ChunkedReader

parser = ArgumentParser()
parser.add_argument('-video_size', nargs=1, type=str, required=True)
parser.add_argument('-pixel_format', nargs=1, type=str, required=True)
parser.add_argument('-r', type=float, default=25.0)
parser.add_argument('input', nargs=1)

args = parser.parse_args()
print('got args: {}'.format(args))

frame_size = tuple([int(v) for v in args.video_size[0].split('x')])

pix_fmt_sizes = {
    'yuv420p': lambda width, height: int(width * height * 3 / 2)
}


frame_byte_size = pix_fmt_sizes[args.pixel_format[0]](*frame_size)
all_frames = []


def process_frame(frame):
    all_frames.append(frame)
    print('received frame #{}'.format(len(all_frames)))


reader = ChunkedReader(
    src=sys.stdin.buffer if args.input[0] == '-' else open(args.input[0]),
    chunk_size=frame_byte_size,
    consumer=process_frame)

reader.read()

print('EOF, received {} frames'.format(len(all_frames)))

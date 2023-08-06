import argparse

from pyunitx.resistance import from_color


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--tolerance",
        action="store_true",
        help="Indicate the absolute tolerance in the output."
    )
    parser.add_argument(
        "-s",
        "--sensitivity",
        action="store_true",
        help="Indicate both temperature sensitivity and absolute tolerance in the output."
    )
    parser.add_argument(
        "spec",
        help="""The color code to read. Each color is represented by one letter, capitalized 
        here in the word:
        blacK, Brown, Red, Orange, Yellow, grEen, blUe, Violet, Gray, White, goLd, Silver.
        """
    )
    return parser.parse_args()


def main():
    args = parse_args()
    values = from_color(args.spec, args.tolerance, args.sensitivity)
    if args.sensitivity:
        print(
            f"{values[0].to_natural_si()} + {values[2].value} Ω/K ± {values[1].to_natural_si()}"
        )
    elif args.tolerance:
        print(f"{values[0].to_natural_si()} ± {values[1].to_natural_si()}")
    else:
        print(values.to_natural_si())


if __name__ == '__main__':
    main()

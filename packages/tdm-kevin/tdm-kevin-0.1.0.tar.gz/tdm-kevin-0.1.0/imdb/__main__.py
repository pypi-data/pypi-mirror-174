import argparse
import sys
import uvicorn

def start_api(port: int):
    uvicorn.run("imdb.api:app", port=port, log_level="info")

def main():
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(help="possible commands", dest="command")
	some_parser = subparsers.add_parser("imdb", help="")
	some_parser.add_argument("-p", "--port", help="port to run on", type=int)

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)

	args = parser.parse_args()

	if args.command == "imdb":
		start_api(port = args.port)

if __name__ == "__main__":
	main()
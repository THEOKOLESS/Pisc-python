import sys

def	init_dic(arg):
	states = {
	"Oregon" : "OR",
	"Alabama" : "AL",
	"New Jersey": "NJ",
	"Colorado" : "CO"
	}

	capital_cities = {
	"OR": "Salem",
	"AL": "Montgomery",
	"NJ": "Trenton",
	"CO": "Denver"
	}
	if arg in states:
		value = states[arg]
		print(capital_cities[value])
	else:
		print("Unknown state")

def main():
	if (len(sys.argv) == 2):
		init_dic(sys.argv[1])

if __name__ == '__main__':
	main()
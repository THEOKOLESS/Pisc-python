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
	cap = ""
	for k, v in capital_cities.items():
		if v == arg:
			cap = k
			for k, v in states.items():
				if cap == v:
					print(k)
	if cap == "":
		print("Unknown state")
		


def main():
	if (len(sys.argv) == 2):
		init_dic(sys.argv[1])

if __name__ == '__main__':
	main()
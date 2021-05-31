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

	l = arg.split(',')
	non_e_l = [line for line in l if line.strip() != ""] #rmv empty l 

	for elem in non_e_l:
		tmp = " ".join(elem.split()) #rmv whitespace
		if not check_cap(capital_cities, tmp.title(), states) and not check_states(tmp.title(), states, capital_cities):
			print(tmp, " is neither a capital city nor a state")

def	check_cap(capital_cities, arg, states):
	for k, v in capital_cities.items():
		if v == arg:
			cap = k
			for k, v in states.items():
				if cap == v:
					print(arg, "is the capital of", k)
					return True
	return	False
	
def	check_states(arg, states, capital_cities):
	if arg in states:
		value = states[arg]
		print(capital_cities[value], "is the capital of", arg)
		return True
	return False
	
	


def main():
	if (len(sys.argv) == 2):
		init_dic(sys.argv[1])

if __name__ == '__main__':
	main()
import sys
import antigravity

def main():
    if len(sys.argv) != 4:
        print("Usage: python geohashing.py <latitude> <longitude> <datedow>")
        sys.exit(1)

    latitude = sys.argv[1]
    try:
        latitude = int(latitude)
    except ValueError:
        print(f"Error: {latitude} must be an integer.")
        sys.exit(1)
    longitude = sys.argv[2]
    
    try: 
        longitude = int(longitude)
    except ValueError:
        print(f"Error: {longitude} must be an integer.")
        sys.exit(1)
  
    try:
        datedow = sys.argv[3].encode("utf-8")
    except ValueError:
        print(f"Error: {datedow} must be a string.")
        sys.exit(1)

    antigravity.geohash(int(latitude), int(longitude), datedow)



if __name__ == "__main__":
    main()
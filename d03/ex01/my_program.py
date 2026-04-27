from local_lib.path import Path

def main():
    path = Path("my_folder")
    path.mkdir_p()

    file = path / "test.txt"
    file.write_text("Hello, World!")
    with file.open() as f:
        content = f.read()
        print(content)



if __name__ == "__main__":
    main()
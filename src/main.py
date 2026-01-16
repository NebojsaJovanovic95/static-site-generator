from textnode import TextNode, TextType

def main():
    node = TextNode(
        "This is some text node i am trying",
        TextType.LINK,
        "http://www.boot.dev"
    )
    print(f"{node}")

if __name__ == "__main__":
    main()

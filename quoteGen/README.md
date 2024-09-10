This script provides a simple quote generator UI in Maya.
It displays random quotes from a text file.
I created it when I was learning Python as a fun project.

1. Place the 'quoteGen' folder in your Maya scripts directory(e.g., C:/Users/your_username/Documents/maya/scripts/).
2. In Maya's script editor, python tab run the following commands:
    quoteGen import quoteGen
    quoteGen.QuoteWindow(quoteGen.QuoteGenerator()).create_ui()


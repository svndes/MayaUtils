This script provides a simple quote generator UI in Maya.<br/>
It displays random quotes from a text file.<br/>
I created it when I was learning Python as a fun project.<br/>

1. Place the 'quoteGen' folder in your Maya scripts directory<br/>(e.g., C:/Users/your_username/Documents/maya/scripts/).<br/>
2. In Maya's script editor, python tab run the following commands:<br/>

        quoteGen import quoteGen
        quoteGen.QuoteWindow(quoteGen.QuoteGenerator()).create_ui()


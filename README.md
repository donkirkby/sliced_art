# Sliced Art
A drawing puzzle

This puzzle takes a picture and slices it up into smaller pieces. You get the
pieces, but they're all shuffled up with clues to which piece goes where. To
solve the puzzle, you have to solve an anagram for each piece. One of the
letters in each solution is highlighted, and that letter tells you which spot
to copy the piece into (A, then B, then C, and so on).

Here's an example puzzle, based on a public-domain image from [svgsilh.com].

![example PNG]

To try the puzzle, either print out the image, or download the [PDF].

[svgsilh.com]: https://svgsilh.com
[example PNG]: example.png
[PDF]: example.pdf

To make your own puzzles, download the source code, and install the dependencies
using `pipenv`. Find a picture that you like, and download it. Black and white
works best. Avoid cross hatching, because it's hard to copy. If you want to
publish the puzzles, you should probably search for images that are licensed for
[reuse].

Run the program, and open the image file. Download the word file from
[vograbulary], and open that. Type a word for each letter on the words tab. It
will show you other words that are anagrams of the word you typed, and it will
capitalize the position that is highlighted in the clue. If your word has more
than one of the target letters, you can capitalize the one you want to highlight.
Go back to the art tab, and drag the squares around until you like the position.
Then, shuffle the squares until you like the arrangement. Save the puzzle as
a PDF, and then print out the PDF. Challenge your friends to solve the puzzle!

Each square gets a clue. Add one letter and unscramble the word. The added
letter tells you which position to draw the square in.

[vograbulary]: https://github.com/donkirkby/vograbulary/blob/master/core/assets/wordlist.txt
[reuse]: https://www.google.com/search?q=animal%20line%20art&tbm=isch&tbs=sur%3Afc

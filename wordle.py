from matplotlib.path import Path
import matplotlib.pyplot as plt

def custom_box_style(x0, y0, width, height, n):
    """
    Given the location and size of the box, return the path of the box around
    it.

    Rotation is automatically taken care of.

    Parameters
    ----------
    x0, y0, width, height : float
        Box location and size.
    mutation_size : float
        Mutation reference scale, typically the text font size.
    """
    
    # width and height with padding added.
    width = 38
    height = 40
    # boundary of the padded box
    x0, y0 = x0-7, y0+3
    # x0, y0 = x0, y0
    x1, y1 = x0 + width, y0 + height

    
    return Path([(x0, y0),
                 (x1, y0), (x1, y1), (x0, y1),
                #  (x0-pad, (y0+y1)/2), (x0, y0),
                 (x0, y0)],
                closed=True)

def wordle_run(words, correct):
    fig, ax = plt.subplots(figsize=(4, 4))

    #box color matrix
    boxColor = [
        ['gray','gray','gray','gray','gray'],
        ['gray','gray','gray','gray','gray'],
        ['gray','gray','gray','gray','gray'],
        ['gray','gray','gray','gray','gray'],
        ['gray','gray','gray','gray','gray'],
        ['gray','gray','gray','gray','gray']
    ]

    for i, word in enumerate(words):
                    
        for j, letter in enumerate(word):
            if letter in correct:
                boxColor[i][j] = 'yellow'
            if letter == correct[j]:
                boxColor[i][j] = 'green'

            ax.text(
                0.05+0.2*j, 0.7-0.3*i,
                letter, 
                size=30, 
                fontname = 'Consolas',
                bbox=dict(
                    boxstyle=custom_box_style, alpha=0.5, 
                    color = boxColor[i][j],
                    ec = 'black'
                    # color = 'gray'
                )
            )

    ax.set_ylim(-1,1)
    fig.suptitle('bot Wordle', fontweight = 'bold')

    plt.axis('off')
    plt.savefig('result.PNG')
    # plt.show()

    if correct in words:
        return True
    if len(words) >= 6:
        return False

# words = [ 
#     "HELLO", 
#     "     ", 
#     "     ", 
#     "     ", 
#     "     ", 
#     "     ", 
# ]

# win = wordle(words, 'CHEEK')
# print(win)
# print(words[0])
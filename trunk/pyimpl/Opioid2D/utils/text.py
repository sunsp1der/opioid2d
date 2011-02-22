"""Text rendering utilities and effects
"""

import pygame
from pygame.locals import *

__all__ = (
    "textbox",
    "split",
    "multiline",
    "bordered_text",
    )

def bordered_text(font, text, color, bordercolor, antialias=False):
    """bordered_text(font, text, color, bordercolor, antialias=False) -> Surface
    
    Render a piece of text just like pygame Font.render, but add a 1px
    wide border around the text.
    """
    ts = font.render(text, antialias, color)
    ts2 = font.render(text, antialias, bordercolor)
    x,y = ts.get_size()
    x += 2
    y += 2
    s = pygame.Surface((x,y), SRCALPHA, 32)
    for dx in range(-1,2):
        for dy in range(-1,2):
            s.blit(ts2, (1+dx,1+dy))
    s.blit(ts, (1,1))
    return s

def textbox(font, text, maxwidth, color=(255,255,255), antialias=True, border=False):
    """textbox(font, text, maxwidth, color=(255,255,255), antialias=True) -> Surface

    Renders a string using the given font so that each line is no
    wider than the specified maximum width (except, if a word does
    not fit a single line). This is essentially the same as calling
    text.split and text.multiline manually.
    """
    lines = split(font, text, maxwidth)
    s = multiline(font, lines, color, antialias, border)
    return s

def split(font, text, maxwidth):
    """split(font, text, maxwidth) -> lines

    Splits a string of text into multiple lines, so that
    when the text is rendered using the given font, no
    line exceeds the specified maximum width.
    """    
    words = text.split(' ')
    words.reverse()
    line = []
    lines = []
    nextword = words.pop()
    while 1:
        linetext = ' '.join(line+[nextword])
        width,height = font.size(linetext)
        if line and width > maxwidth:
            lines.append(' '.join(line))
            line = []
        else:
            line.append(nextword)
            if not words:
                if line:
                    lines.append(' '.join(line))
                    width,height = font.size(linetext)
                break
            nextword = words.pop()
    return lines

def multiline(font, lines, color=(255,255,255), antialias=True, border=False):
    """multiline(font, lines) -> Surface

    Renders multiple lines of text. 'lines' can be a string
    that contains linefeed characters or a list of strings.
    """
    if isinstance(lines, str):
        lines = lines.split("\n")
    maxwidth = 0
    height = 0
    ## calculate surface size
    for line in lines:
        w,h = font.size(line)
        maxwidth = max(maxwidth, w)
        height += h+1
    s = pygame.Surface((maxwidth+2,height+2), SRCALPHA, 32)
    s.fill((0,0,0,0))
    y = 0
    for line in lines:
        if line:
            if border:
                s2 = bordered_text(font, line, color, (0,0,0), antialias)
            else:
                s2 = font.render(line, antialias, color)
            s.blit(s2, (0,y))
            y += s2.get_size()[1]
        else:
            w,h = font.size(line)
            y += h
    return s

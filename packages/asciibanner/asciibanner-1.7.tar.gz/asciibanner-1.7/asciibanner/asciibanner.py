#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Python Version    : 3.X
# Author            : Dicahsin
# File name         : asciibanner.py

import warnings, os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
    
# Disable warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

# Create art with #
def art_sharp(text): 
    size = (20, 11)
    img = Image.new("1",size,"black")
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, "white")
    pixels = np.array(img, dtype=np.uint8)
    chars = np.array([' ','#'], dtype="U1")[pixels]
    strings = chars.view('U' + str(chars.shape[1])).flatten()
    return( "\n".join(strings))

# Create art with /
def art_slash(text):
    size = (20, 11)
    img = Image.new("1",size,"black")
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, "white")
    pixels = np.array(img, dtype=np.uint8)
    chars = np.array([' ','/'], dtype="U1")[pixels]
    strings = chars.view('U' + str(chars.shape[1])).flatten()
    return( "\n".join(strings))

# Create art with $
def art_dollar(text):
    size = (20, 11)
    img = Image.new("1",size,"black")
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, "white")
    pixels = np.array(img, dtype=np.uint8)
    chars = np.array([' ','$'], dtype="U1")[pixels]
    strings = chars.view('U' + str(chars.shape[1])).flatten()
    return( "\n".join(strings))

# Create art with !
def art_exclamation(text):
    size = (20, 11)
    img = Image.new("1",size,"black")
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, "white")
    pixels = np.array(img, dtype=np.uint8)
    chars = np.array([' ','!'], dtype="U1")[pixels]
    strings = chars.view('U' + str(chars.shape[1])).flatten()
    return( "\n".join(strings))

# Create art with custom sign
def art_custom(text, sign):
    size = (20, 11)
    img = Image.new("1",size,"black")
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, "white")
    pixels = np.array(img, dtype=np.uint8)
    chars = np.array([' ',f'{sign}'], dtype="U1")[pixels]
    strings = chars.view('U' + str(chars.shape[1])).flatten()
    return( "\n".join(strings))

# Create art with ?
def art_interogation(text):
    size = (20, 11)
    img = Image.new("1",size,"black")
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, "white")
    pixels = np.array(img, dtype=np.uint8)
    chars = np.array([' ','?'], dtype="U1")[pixels]
    strings = chars.view('U' + str(chars.shape[1])).flatten()
    return( "\n".join(strings))
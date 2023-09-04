#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import sys
import os
import codecs
import re

language = sys.argv[1]
morph_output_folder = sys.argv[2]

#encodings: cp1252, utf-8, utf-16BE ...

#get path of input folder
containing_path = morph_output_folder.rsplit('\\', 1)[0].replace('\\', '/')
# language = 'GA'
with_underscores = 'no'
without_underscores = 'yes'
#folder_name = path.rsplit('\\', 1)[1]

#filename = os.path.join(containing_path, str(x)+'_report.txt')

#create output file
#fo = codecs.open(filename, 'a', 'utf-8')

#read filepaths
#list_filepaths = glob.glob(os.path.join(path, '*.conll'))
list_filepaths = glob.glob(os.path.join(morph_output_folder, '*_out.txt'))

def uppercase(match):
  return(match.group(1).upper())

def uppercaseDot(match):
  return('. '+match.group(1).upper())

def clean_outputs (text, count, underscores):
  # Irish things
  if language == 'GA':
    # Reestablish punctuations removed for morph processing
    text = re.subn("_APSTR_", "'", text)[0]
    text = re.subn("_OBRKT_", "(", text)[0]
    text = re.subn("_CBRKT_", ")", text)[0]
    text = re.subn("_AMPRS_", "&", text)[0]
    text = re.subn("_SEMICOL_", ";", text)[0]
    text = re.subn("_DOLLSIGN_", "$", text)[0]
    # The next line was not activated for the WebNLG submission
    # text = re.subn("_PLUSSIGN_", "+", text)[0]
    text = re.subn("_DBLQUOT_", '\"', text)[0]
    # Process prefixes (either after a space or at the beginning of a line)
    text = re.subn(" d- ", " d'", text)[0]
    text = re.subn("^d- ", "d'", text)[0]
    text = re.subn(' h- ', ' h', text)[0]
    text = re.subn('^h- ', 'h', text)[0]
    text = re.subn(' t- ', ' t-', text)[0]
    text = re.subn('^t- ', 't-', text)[0]
    # The hyphens left should all be from prefixed adjectives
    text = re.subn('- - ', '', text)[0]
    text = re.subn(' - ', '', text)[0]
    text = re.subn('- ', '', text)[0]
    # Bring together a + tá in relative clauses
    text = re.subn(' a tá ', ' atá ', text)[0]
    # contract "de" in front of "fh" and vowels, i, etc.
    text = re.subn(' de [aA]n ', ' den ', text)[0]
    text = re.subn(' de [aA]n_', ' den ', text)[0]
    text = re.subn(' do [aA]n ', ' don ', text)[0]
    text = re.subn(' do [aA]n_', ' don ', text)[0]
    text = re.subn(' faoi [aA]n ', ' faoin ', text)[0]
    text = re.subn(' faoi [aA]n_', ' faoin ', text)[0]
    text = re.subn(' ó [aA]n ', ' ón ', text)[0]
    text = re.subn(' ó [aA]n_', ' ón ', text)[0]
    text = re.subn(" d[eo] ([fF])h", " d'\g<1>h", text)[0]
    text = re.subn(" de ([aeiouAEIOUáéíóúÁÉÍÓÚ])", " d'\g<1>", text)[0]
    text = re.subn(' i Éire ', ' in Éirinn ', text)[0]
    text = re.subn(' i An ', ' ins An ', text)[0]
    text = re.subn(' i An_', ' ins An ', text)[0]
    text = re.subn(' i ([aeiouáéíóúAEIOUÁÉÍÓÚ])', ' in \g<1>', text)[0]
    # Lenition f (+ contraction)
    text = re.subn(' d[eo] ([fF])([^h])', " d'\g<1>h\g<2>", text)[0]
    text = re.subn(" (ar|de|do|faoi|mar|ó|roimh|trí|um|céad) ([bcdfgmptBCDFGMPT])([^hH])", " \g<1> \g<2>h\g<3>", text)[0]
    text = re.subn(" (ar|de|do|faoi|mar|ó|roimh|trí|um|céad) ([sS])([^hcfmptvHCFMPTV])", " \g<1> \g<2>h\g<3>", text)[0]
    # Eclipsis
    text = re.subn(' i ([bB][^pP])', ' i m\g<1>', text)[0]
    text = re.subn(' i ([cC])', ' i g\g<1>', text)[0]
    text = re.subn(' i ([dD][^tT])', ' i n\g<1>', text)[0]
    text = re.subn(' i ([fF])', ' i bh\g<1>', text)[0]
    text = re.subn(' i ([gG][^cC])', ' i n\g<1>', text)[0]
    text = re.subn(' i ([pP])', ' i b\g<1>', text)[0]
    text = re.subn(' i ([tT])', ' i d\g<1>', text)[0]
    # text = re.subn(' i ([aeiouáéíóú])', ' i n-\g<1>', text)[0]
    # text = re.subn(' i ([AEIOUÁÉÍÓÚ])', ' i n\g<1>', text)[0]
    # Ugly patches
    text = re.subn(' ar bhí ', ' a bhí ', text)[0]
    text = re.subn(' an ann ', ' air ', text)[0]
    text = re.subn(' an sé ', ' an é ', text)[0]
  # Erroneous "type = parenthetical" fix
  if re.search('\) \(', text):
    print('!!! Failed parenthesis generation in input '+str(count)+' (fixed)')
    text = re.subn('\) \(', ' ', text)[0]
  # clean quotes that MATE can’t take care of
  text = re.subn('\\\\"([^\\\\]+)\\\\', '"\g<1>"', text)[0]
  # uppercase words when at the beginning of a sentence or after a final dot (dots preceded by a space)
  text = re.subn(' \. ([a-z])', uppercaseDot, text)[0]
  text = re.subn('^([a-z])', uppercase, text)[0]
  # replace "a" by "an" before vowels (should restrict to English)
  if language == 'EN':
    text = re.subn(' a ([aeio])', ' an \g<1>', text)[0]
  # find generation fails (we introduce [..] or [...] or [......] when a sentence cannot be generated
  if re.search('\[\.\.', text):
    print('!!! Failed sentence generation in input '+str(count))
  # remove space before commas and dots
  text = re.subn(' ,', ',', text)[0]
  text = re.subn(' \.', '.', text)[0]
  # replace double dots by single ones
  while re.search('\.\.', text):
    text = re.subn('\.\.', '.', text)[0]
  text = re.subn('% %', '%', text)[0]
  # Clean remnants of non-generated sentences
  text = re.subn('Sentence \[\.\]\.', '', text)[0]
  # Remove initial spaces
  while re.search('^ ', text):
    text = re.subn('^ ', '', text)[0]
  # replace underscores by spaces
  if underscores == 'yes':
    pass
  else:
    text = re.subn('_', ' ', text)[0]
  # New 2023: replace double spaces by single ones
  while re.search('  ', text):
    text = re.subn('  ', ' ', text)[0]
  # reformat date/time
  text = re.subn('([0-9]+)-([0-9]+)-([0-9]+)T([0-9]+:[0-9]+:[0-9]+)Z', '\g<1>/\g<2>/\g<3> at \g<4>', text)[0]
  return(text)

count_strs_all_postproc = []
for filepath in sorted(list_filepaths):
  count_strs_all = 0
  # filename = filepath.split('\\')[-1].split('.')[0]
  head, tail = os.path.split(filepath)
  filename = tail.rsplit('.')[0]
  fd = codecs.open(filepath, 'r', 'utf-8')
  print('Processing '+filename)
  filename_out_noUnderscores = filename+'_postproc''.txt'
  filename_out_Underscores = filename+'_postproc_underscores''.txt'
  if without_underscores == 'yes':
    fo1 = codecs.open(os.path.join(morph_output_folder, filename_out_noUnderscores), 'w', 'utf-8')
  if with_underscores == 'yes':
    fo2 = codecs.open(os.path.join(morph_output_folder, filename_out_Underscores), 'w', 'utf-8')
  lines = fd.readlines()
  x = 0
  for line in lines:
    # To filter out final linebreak in each file
    if not line == '\n':
      if without_underscores == 'yes':
        new_line = clean_outputs(line, x, 'no')
        fo1.write(new_line)
      if with_underscores == 'yes':
        new_line = clean_outputs(line, x, 'yes')
        fo2.write(new_line)
      count_strs_all += 1
    x += 1
  if without_underscores == 'yes':
    fo1.close()
  if with_underscores == 'yes':
    fo2.close()
  count_strs_all_postproc.append(count_strs_all)
import argparse
from itertools import chain, repeat, islice


arg_parser = argparse.ArgumentParser(description='Combine CoNLL-2005 and CoNLL-2009 files.')
arg_parser.add_argument('--input_file_ptb', type=str, help='CoNLL-2005 file to process')
arg_parser.add_argument('--input_file_conll', type=str, help='CoNLL-2009 file to process')
arg_parser.add_argument('--output_file', type=str, help='File to write')
args = arg_parser.parse_args()


def pad_infinite(iterable, padding=None):
   return chain(iterable, repeat(padding))


def pad(iterable, size, padding=None):
   return islice(pad_infinite(iterable, padding), size)


def approx_equal(sent1, sent2):
  return ''.join(sent1) == ''.join(sent2)


def get_fields_ptb(split_line):
  # return first 8 fields, except first
  return split_line[1:8]


def get_fields_conll(split_line):
  # return 12th field and everything after
  fields = split_line[12:]

  # if no predicates, stick an empty column in anyway
  if len(fields) == 2:
    fields = fields + ["_"]
  return fields

sentences_ptb = []
sentences_conll = []
fields_ptb = []
fields_conll = []
# load words / fields
with open(args.input_file_ptb) as ptb_file, open(args.input_file_conll) as conll_file:
  buf = []
  fields_buf = []
  for line in ptb_file:
    line = line.strip()
    if line:
      split_line = line.split()
      word = split_line[1]
      buf.append(word)
      fields_buf.append(get_fields_ptb(split_line))
    elif buf:
      sentences_ptb.append(buf)
      fields_ptb.append(fields_buf)
      buf = []
      fields_buf = []
  if buf:
    sentences_ptb.append(buf)

  buf = []
  fields_buf = []
  for line in conll_file:
    line = line.strip()
    if line:
      split_line = line.split()
      word = split_line[1]

      # unescape
      word = word.replace("\\", "")

      buf.append(word)
      fields_buf.append(get_fields_conll(split_line))
    elif buf:
      sentences_conll.append(buf)
      fields_conll.append(fields_buf)
      buf = []
      fields_buf = []
  if buf:
    sentences_conll.append(buf)

print("Loaded %d sentences from ptb file" % len(sentences_ptb))
print("Loaded %d sentences from conll file" % len(sentences_conll))

ptb_idx = 0
aligned = 0
approx_aligned = 0
approx_difficult = 0
align_collisions = 0
# align sentences
with open(args.output_file, 'w') as out_file:
  for conll_idx, (sent_conll, field_conll) in enumerate(zip(sentences_conll, fields_conll)):
    sent_ptb = sentences_ptb[ptb_idx]
    field_ptb = fields_ptb[ptb_idx]
    if sent_ptb == sent_conll:
      for idx, (f_ptb, f_conll) in enumerate(zip(field_ptb, field_conll)):
        print("%d\t%s\t%s" % (idx, "\t".join(f_ptb), "\t".join(f_conll)), file=out_file)
      print("", file=out_file)
      aligned += 1
      ptb_idx += 1
    elif approx_equal(sent_ptb, sent_conll):
      i = 0
      offset = 0
      align = []
      new_fields_conll = []
      for i, tok in enumerate(sent_ptb):
        if tok == sent_conll[i + offset]:
          align.append(tok)
          new_fields_conll.append(field_conll[i + offset])
        else:
          b = []
          new_fields = []
          k = i + offset
          while k < len(sent_conll) and ''.join(b) != sent_ptb[i]:
            b.append(sent_conll[k])
            new_fields.append(field_conll[k])
            k += 1
          new_tok = ''.join(b)
          new_field = new_fields[0]
          nonempty_fields = filter(lambda nf: any([f != '_' for f in nf]), new_fields)
          nonempty = [list(filter(lambda f: f != '_', fields)) for fields in zip(*new_fields)]
          maxlen = max(map(lambda f: len(f), nonempty))
          nonempty_padded = list(zip(*map(lambda f: list(pad(f, maxlen, '_')), nonempty)))
          if nonempty_padded:
            new_field = nonempty_padded[0]
            if len(nonempty_padded) > 1:
              align_collisions += 1
              print(b)
              print(nonempty_padded)
          new_fields_conll.append(new_field)
          offset += k - (i + offset) - 1
          if new_tok == tok:
            align.append(tok)
      if align == sent_ptb:
        for idx, (f_ptb, f_conll) in enumerate(zip(field_ptb, new_fields_conll)):
          print("%d\t%s\t%s" % (idx, "\t".join(f_ptb), "\t".join(f_conll)), file=out_file)
        print("", file=out_file)
        approx_aligned += 1
      ptb_idx += 1

    else:
      # skip over sentences until we find this one
      while not approx_equal(sent_ptb, sent_conll):
        ptb_idx += 1
        sent_ptb = sentences_ptb[ptb_idx]
      field_ptb = fields_ptb[ptb_idx]
      if sent_ptb == sent_conll:
        for idx, (f_ptb, f_conll) in enumerate(zip(field_ptb, field_conll)):
          print("%d\t%s\t%s" % (idx, "\t".join(f_ptb), "\t".join(f_conll)), file=out_file)
        print("", file=out_file)
        aligned += 1
      else:
        i = 0
        offset = 0
        align = []
        new_fields_conll = []
        for i, tok in enumerate(sent_ptb):
          if tok == sent_conll[i + offset]:
            align.append(tok)
            new_fields_conll.append(field_conll[i + offset])
          else:
            b = []
            new_fields = []
            k = i + offset
            while k < len(sent_conll) and ''.join(b) != sent_ptb[i]:
              b.append(sent_conll[k])
              new_fields.append(field_conll[k])
              k += 1
            new_tok = ''.join(b)
            new_field = new_fields[0]
            nonempty = [list(filter(lambda f: f != '_', fields)) for fields in zip(*new_fields)]
            maxlen = max(map(lambda f: len(f), nonempty))
            nonempty_padded = list(zip(*map(lambda f: list(pad(f, maxlen, '_')), nonempty)))
            if nonempty_padded:
              new_field = nonempty_padded[0]
              if len(nonempty_padded) > 1:
                align_collisions += 1
                print(b)
                print(nonempty_padded)

            new_fields_conll.append(new_field)
            offset += k - (i + offset) - 1
            if new_tok == tok:
              align.append(tok)
        if align == sent_ptb:
          for idx, (f_ptb, f_conll) in enumerate(zip(field_ptb, new_fields_conll)):
            print("%d\t%s\t%s" % (idx, "\t".join(f_ptb), "\t".join(f_conll)), file=out_file)
          print("", file=out_file)
          approx_aligned += 1
      ptb_idx += 1

print("Aligned %d sents" % aligned)
print("Approximately aligned %d sents" % approx_aligned)
print("Align collisions: %d" % align_collisions)

print("Total: %d sents" % (aligned+approx_aligned+approx_difficult))


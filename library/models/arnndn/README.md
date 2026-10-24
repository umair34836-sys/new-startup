# arnndn models (ffmpeg neural speech de-noise)

Downloaded 2026-10-24 from https://github.com/richardpl/arnndn-models (raw.githubusercontent.com). Use with
`ffmpeg -i in.wav -af "arnndn=m=library/models/arnndn/std.rnnn" out.wav`; tested here 2026-10-24: pauses -42.9 -> -65.6 dB,
output 10 ms late (see library/research/editing/skills2/05-audio-dialogue.md #1538-#1541).

- `std.rnnn`: the model originally bundled with Xiph RNNoise (repo README). RNNoise licence: BSD-style (redistribution permitted with
  copyright notice; Copyright (c) 2017 Mozilla, 2007-2017 Jean-Marc Valin, 2005-2017 Xiph.Org Foundation, 2003-2004 Mark Borgerding),
  https://github.com/xiph/rnnoise/blob/master/COPYING.
- `bd, cb, lq, mp, sh .rnnn`: by Gregor Richards (rnnoise-models). His README: apart from tools/ and the README, "none of this work is
  creative and thus none of it is subject to copyright". Which to pick by signal/noise type: skill #1539.

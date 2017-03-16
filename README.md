Sheng Tan, Andrew Zhou
EE126 UC Berkeley
Mar.15th 2017

##Project Report

#Abstract

We convert the .txt file into hexadecimal numbers using their ASCII code. Then for each hexadecimal
number, we correspond one frequency to it (hex * 400 + 1000 Hz for hex< 10, (hex+2)*400 + 1000 Hz
for hex>10), so the range of frequency is 1000Hz to 7800Hz. The frequency 10.5*400+1000 = 5200Hz
is added between every hex number as a barrier to prevent missing two same consecutive hex numbers.
The frequency 9000Hz is added at the beginning and the end as a sign of starting and finishing. Once
the frequency is recorded, we start decoding once we see a 9000Hz. When ever we see a frequency(fi),
we check if fi+1,fi+2 is within 200Hz from fi. If so, we assume that we are receiving a stable reading of a
frequency. We look from fi – 100 to fi + 100 to see if fi is a decodable frequency. Once fi is read and
interpreted, we skip all the following frequencies until we see a barrier (5200Hz ± 50), and check if two
behind is also a barrier(to make sure it’s not an abrupt noise). Then we skip all of the following
frequencies until we see a frequency outside of the barrier range. If nothing is decoded between two
barrier, we assume that frequency is interrupted and try to calculate the average and fill the location
with a hex number to prevent misalignment, which destroy the entire decoded txt file.

#Difficulties
The biggest difficulty we encountered is definitely making sure that there is no misalignment in our
decoded file, as misalignment destroy all subsequent decoding. Our first design is that if nothing is
decodable between every two barriers, we calculate the average of the not decodable frequencies to try
to guess the actual frequency there. However, this design sometimes add random frequencies int 
between and does not prevent frequencies from missing very well. Later we found out in a piazza post
that the characters are only from standard 128 ASCii characters, which gives us a much better method
to detect misalignment: if the character(two h ex number, h1h2) being decoded is greater than 128, we
know that we are encountering misalignment and we ignore h1, and tries to decode h2h3, until we find
a meaningful decoding. Thus although it does not prevent the missing frequencies with 100%
guarantee, it prevent extreme conditions where the entire file is not readable. Also, tunning the
sampling speed of the receiver took us some time, because a low sampling speed does not meet the
requirement of 100 bits per second, whereas the reading is inaccurate when sampling speed is too high.

#Learning
In the implementation of our original design, we encountered numerous problems that deviates from
our theory. For instance, the microphone of the computer does not detect the frequency well when it is
above 10000 Hz, so we have to abort some of the range. Assign a unique frequency to every character
was our initial design, but then it creates difficulty to adding the barriers and makes decoding much
harder and thus we chose to convert the characters into hexadecimal numbers. We were trying to
simplify this problem into a erasing channel, yet because we do not know the location of each package,
the problem of erasing and adding still exists. All these challenges remind us that the reality deviates a
lot from the theory and it takes practicing and experiment to turn theory into useful applications.
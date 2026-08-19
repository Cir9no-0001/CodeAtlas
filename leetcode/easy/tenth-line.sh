# Tenth Line
# https://leetcode.com/problems/tenth-line
# difficulty: easy
# first_seen: 2026-08-19 00:12:10 EDT
# runtime: 29ms

# Notes:
# Hint: Read line by line using awk, NR stores current line number. When NR is 10, awk will
# print it, else nothing is printed. [TC: O(N)]
# End Notes

# Read from the file file.txt and output the tenth line to stdout.
awk 'NR==10' file.txt
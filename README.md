# Bunny Kingdom Board Generator

This project is made to randomly generate boards for Bunny Kingdom, in a way that is faithful to the original.

## Generation Rules

* 10x10 board
* 15 fish tiles
  * Four groups: 2, 2, 4, 7
  * Each tile is adjacent to the edge or another fish tile of the same group
* 15 wood tiles
  * 1x1, 1x2, or 1x3 groups
  * Wood groups have a 75% chance to generate touching the border
  * Groups may not touch
* 16 mountain tiles
  * 1x2 groups
  * Only 4 squares mountains may be adjacent
* 10 carrot tiles
  * 1x1 or 1x2 groups
  * 1/8 chance of a group being adjacent to an edge
* 16 city tiles
  * Not adjacent
* 28 blank tiles
  * No rules
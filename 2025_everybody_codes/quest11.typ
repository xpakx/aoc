#set page(
  paper: "a4",
  margin: (x: 2cm, y: 2cm),
  numbering: "1",
)
#set text(font: "EB Garamond", size: 11pt, lang: "en")
#set heading(numbering: "1.1.")

// ------------------------------------------------------------------
// UTILITIES
// ------------------------------------------------------------------

#let array-viz(items, active: (), pointers: (:), highlight-indices: (), label: none) = {
  let cell-size = 28pt
  
  // Define colors
  let color-inactive-bg = white
  let color-inactive-stroke = black
  let color-active-bg = blue.lighten(80%)
  let color-active-stroke = blue
  let color-highlight-bg = green.lighten(80%)
  
  let content = grid(
    columns: (cell-size,) * items.len(),
    rows: (cell-size, auto),
    column-gutter: 3pt,
    row-gutter: 4pt,
    
    // Row 1: The Boxes
    ..items.enumerate().map(((i, value)) => {
      let bg = if i in active { color-active-bg } 
               else if i in highlight-indices { color-highlight-bg }
               else { color-inactive-bg }
               
      let stroke-color = if i in active { color-active-stroke } else { color-inactive-stroke }
      
      rect(
        width: 100%, height: 100%, 
        fill: bg, 
        stroke: stroke-color + 0.5pt,
        radius: 3pt,
        align(center + horizon, text(weight: "medium", str(value)))
      )
    }),

    // Row 2: The Pointers
    ..range(items.len()).map(i => {
      let p = pointers.at(str(i), default: none)
      if p != none {
        align(center, text(size: 0.8em, fill: blue.darken(30%))[
          #sym.arrow.t \ #p
        ])
      } else {
        none
      }
    })
  )
  
  if label != none {
    figure(content, caption: label)
  } else {
    content
  }
}

// ------------------------------------------------------------------
// DOCUMENT CONTENT
// ------------------------------------------------------------------

#align(center)[
  #text(size: 18pt, weight: "bold")[Everybody Codes 2025] \
  #v(0.5em)
  #text(style: "italic")[Quest 11]
]

= Introduction

The problem asks us to simulate a process of
redistributing values in an array until stability is reached.
The process consists of two distinct phases:

1.  *Phase 1 (Sorting):* Iterates left-to-right. If a left value is larger than the right value ($x_i > x_(i+1)$), a duck is moved from left to right ($x_i arrow.l x_i - 1$, $x_(i+1) arrow.l x_(i+1) + 1$).
2.  *Phase 2 (Balancing):* Iterates left-to-right. If a left value is smaller than the right value ($x_i < x_(i+1)$), a duck is moved from right to left ($x_i arrow.l x_i + 1$, $x_(i+1) arrow.l x_(i+1) - 1$).

We are looking for an analytical solution for Part 2,
avoiding a costly brute-force simulation.

= Phase 1: Sorting

The first phase behaves similarly to a bubble sort,
but instead of swapping elements, it transfers magnitude.
This effectively pushes "mass" to the right,
smoothing out "heaps" and resulting in a monotonically
non-decreasing array.

Let's visualize a single step where $x_i > x_(i+1)$:

#array-viz(
  (5, 2, 2), 
  active: (0, 1), 
  pointers: ("0": "i", "1": "i+1"),
  label: [Condition $5 > 2$ is met. Mass flows right.]
)

#align(center, $arrow.b$)

#array-viz(
  (4, 3, 2), 
  active: (0, 1), 
  label: [Result after one operation.]
)

At the end of Phase 1, the array is guaranteed to be sorted:
$ x_0 <= x_1 <= dots <= x_n $ 

As a corollary, if an array
is aready monotonically non-decreasing, we can skip phase 1,
as it will take 0 steps.

= Phase 2: Balancing
Let $mu$ be the integer mean of the array: $mu = floor.l sum x / n floor.r$.

Because the array is sorted, we can divide
it into two segments at index $k$, such that:
1.  *Deficit Segment* ($0 dots k$): All $x_i < mu$.
2.  *Surplus Segment* ($k+1 dots n$): All $x_i >= mu$.

The task is equivalent to moving "mass" from
the Surplus Segment to the Deficit Segment until
all deficits are resolved (i.e., every element is at least $mu$).

// TODO: Add visualizations


// TODO: tidy up reasoning
// split into lemmas:
// 1. k>0 -> exactly one move from surpluses to deficits
// 2. k==0 -> program stops
// 3. k cannot move right
// 4. there is always k:
// 4.1. no holes to the right
// 4.2. no heaps to the left
// assumptions:
// 1. array is initially sorted
// 2. array is perfectly balanceable, i.e. mean = floor(mean)
let's consider a cycle (equivalent to `step_second_phase()`)
method

let's suppose we're at the beggining of a step, and $x$
is a state of an array before the step, and $x'$ after 
the step;
suppose there is a $k$ that fullfills such conditions,
then at $i==k$, $x'_k <= x_k$
(beacause one duck could have been moved "back"),
and $i+1$ wasn't moved yet;
and bc $k$ was boundary between deficits and surpluses,
it is guaranteed that there is exactly one swap
from surpluses to deficits, because:
$x'_k< x_(k+1)$

then either
$x'_(k+1)== mu - 1$,
or $x'_(k+1) >= mu$. otherwise,
in the former case, deficit we got would be
filled from $x(k+1)$, which is $>= mu$, and so on.
because there is still surplus on the right side,
then there is an element at $j>k$, that $x_j>=mu+1$
so even when it will move one duck left, it would be
at least $== mu$
so $k$ cannot move right

what's more:
and for each $i<k$, $x'_i < mu$,
and $x_i$ could grow only if $x_(i+1) > x'_[i]$,
because of that $x_i$ could at most grow to
$mu-1$ if $x'_i == mu-2$ and $x_(i+1) == mu-1$

so the only place when $x_i$ can grow to mean is $k$
so (1) there are no "heaps" before $k-1$, and (2) $k$ either
moves 1 place left or stays at the same place

so we know that in each cycle there is one duck
moved from $[k+1, n-1]$ to $[0, k]$ and
that the balancing ends when $k == 0$
(because all $[0, n-1]$ are $>= mu$, so
if at least one is $> mu$ by $c$, then sum is
$n*mu + c$, which is a contradiction,
bc intial input is balanceable, and by
properties of mean), and that at the beginning
of each cycle there is a k with such properties

because of that the total amount of cycles
is equal to total surplus


Since each cycle reduces the total deficit by exactly 1,
the total number of cycles required is simply the sum of all deficits.

Let $D$ be the set of indices where $x_i < mu$. The total steps $S$ is:

$ S = sum_(i in D) (mu - x_i) $

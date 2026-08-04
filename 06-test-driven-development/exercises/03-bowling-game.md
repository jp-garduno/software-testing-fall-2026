# Exercise 3: Bowling Game Kata

**Module**: 6 - Test Driven Development  
**Difficulty**: Advanced  
**Time**: 90 minutes

---

## 🎯 Objectives

Master complex TDD with stateful objects and intricate business logic.

By completing this exercise, you will:

- Design object-oriented solutions through tests
- Handle complex state and sequence logic
- Manage interdependent test cases
- Refactor toward elegant design
- Build confidence with challenging requirements

---

## Problem Description

Create a bowling game scoring system. The game consists of 10 frames. In each frame, the player has two opportunities to knock down 10 pins. The score for the frame is the total number of pins knocked down, plus bonuses for strikes and spares.

### Bowling Rules

**Spare**: Knocking down all 10 pins in two rolls

- Bonus: The next roll is added to the score

**Strike**: Knocking down all 10 pins on the first roll

- Bonus: The next TWO rolls are added to the score

**10th Frame**: Special case

- If you get a spare in the 10th frame, you get one more roll
- If you get a strike in the 10th frame, you get two more rolls
- These bonus rolls count for calculating 10th frame score only

### Examples

**All Gutter Balls** (0 pins each roll):

```
Score: 0
```

**All Ones** (1 pin each roll):

```
Score: 20 (10 frames × 2 rolls × 1 pin)
```

**One Spare** (spare in first frame, then 3 pins, then all gutter):

```
Frame 1: 5 + 5 (spare) = 10 + 3 (next roll) = 13
Frame 2: 3 + 0 = 3
Total: 16
```

**One Strike** (strike in first frame, then 3, 4, then all gutter):

```
Frame 1: 10 (strike) + 3 + 4 (next two rolls) = 17
Frame 2: 3 + 4 = 7
Total: 24
```

**Perfect Game** (12 strikes):

```
Score: 300
```

---

## Why Bowling Game?

This is Uncle Bob's (Robert C. Martin) most famous kata because:

- **Complex business logic**: Scoring rules are intricate
- **State management**: Must track rolls and frames
- **Look-ahead scoring**: Strikes and spares need future rolls
- **Edge cases**: 10th frame is special
- **Elegant solution**: Simple implementation for complex rules
- **Design lesson**: Tests guide you to clean design

This kata demonstrates the power of TDD for complex problems.

---

## API Design

The `BowlingGame` class needs:

```python
class BowlingGame:
    def roll(self, pins: int) -> None:
        """Record a single roll"""
        pass

    def score(self) -> int:
        """Calculate total score"""
        pass
```

```javascript
class BowlingGame {
  roll(pins) {
    // Record a single roll
  }

  score() {
    // Calculate total score
  }
}
```

**That's it!** Just two methods. The simplicity is beautiful.

---

## Step-by-Step TDD Guide

### Step 1: Gutter Game (All Zeros)

**Test First**:

```python
def test_gutter_game():
    """20 rolls, all 0 pins"""
    game = BowlingGame()
    for _ in range(20):
        game.roll(0)
    assert game.score() == 0
```

```javascript
test("gutter game - all zeros", () => {
  const game = new BowlingGame();
  for (let i = 0; i < 20; i++) {
    game.roll(0);
  }
  expect(game.score()).toBe(0);
});
```

**Simplest Implementation**:

```python
class BowlingGame:
    def __init__(self):
        self.rolls = []

    def roll(self, pins):
        self.rolls.append(pins)

    def score(self):
        return 0
```

```javascript
class BowlingGame {
  constructor() {
    this.rolls = [];
  }

  roll(pins) {
    this.rolls.push(pins);
  }

  score() {
    return 0;
  }
}
```

**Run test**: Should PASS (GREEN).

---

### Step 2: All Ones

**Test First**:

```python
def test_all_ones():
    """20 rolls, all 1 pin"""
    game = BowlingGame()
    for _ in range(20):
        game.roll(1)
    assert game.score() == 20
```

```javascript
test("all ones", () => {
  const game = new BowlingGame();
  for (let i = 0; i < 20; i++) {
    game.roll(1);
  }
  expect(game.score()).toBe(20);
});
```

**Implementation**:

```python
def score(self):
    return sum(self.rolls)
```

```javascript
score() {
  return this.rolls.reduce((sum, pins) => sum + pins, 0);
}
```

**Run tests**: Both should PASS.

---

### Step 3: One Spare

**Test First**:

```python
def test_one_spare():
    """Spare in first frame, then 3, then all gutters"""
    game = BowlingGame()
    game.roll(5)
    game.roll(5)  # Spare
    game.roll(3)  # Counts twice
    for _ in range(17):
        game.roll(0)
    assert game.score() == 16  # 10 + 3 + 3
```

```javascript
test("one spare", () => {
  const game = new BowlingGame();
  game.roll(5);
  game.roll(5); // Spare
  game.roll(3); // Counts twice
  for (let i = 0; i < 17; i++) {
    game.roll(0);
  }
  expect(game.score()).toBe(16); // 10 + 3 + 3
});
```

**Implementation** (Refactor to frame-based scoring):

```python
def score(self):
    total = 0
    roll_index = 0

    for frame in range(10):
        if self.rolls[roll_index] + self.rolls[roll_index + 1] == 10:  # Spare
            total += 10 + self.rolls[roll_index + 2]
            roll_index += 2
        else:
            total += self.rolls[roll_index] + self.rolls[roll_index + 1]
            roll_index += 2

    return total
```

```javascript
score() {
  let total = 0;
  let rollIndex = 0;

  for (let frame = 0; frame < 10; frame++) {
    if (this.rolls[rollIndex] + this.rolls[rollIndex + 1] === 10) { // Spare
      total += 10 + this.rolls[rollIndex + 2];
      rollIndex += 2;
    } else {
      total += this.rolls[rollIndex] + this.rolls[rollIndex + 1];
      rollIndex += 2;
    }
  }

  return total;
}
```

**Run tests**: All should PASS.

**Refactor**: Extract helper method:

```python
def is_spare(self, roll_index):
    return self.rolls[roll_index] + self.rolls[roll_index + 1] == 10
```

---

### Step 4: One Strike

**Test First**:

```python
def test_one_strike():
    """Strike in first frame, then 3 and 4, then all gutters"""
    game = BowlingGame()
    game.roll(10)  # Strike
    game.roll(3)
    game.roll(4)
    for _ in range(16):
        game.roll(0)
    assert game.score() == 24  # 10 + 3 + 4 + 3 + 4
```

```javascript
test("one strike", () => {
  const game = new BowlingGame();
  game.roll(10); // Strike
  game.roll(3);
  game.roll(4);
  for (let i = 0; i < 16; i++) {
    game.roll(0);
  }
  expect(game.score()).toBe(24); // 10 + 3 + 4 + 3 + 4
});
```

**Implementation**:

```python
def score(self):
    total = 0
    roll_index = 0

    for frame in range(10):
        if self.is_strike(roll_index):  # Strike
            total += 10 + self.rolls[roll_index + 1] + self.rolls[roll_index + 2]
            roll_index += 1
        elif self.is_spare(roll_index):  # Spare
            total += 10 + self.rolls[roll_index + 2]
            roll_index += 2
        else:
            total += self.rolls[roll_index] + self.rolls[roll_index + 1]
            roll_index += 2

    return total

def is_strike(self, roll_index):
    return self.rolls[roll_index] == 10

def is_spare(self, roll_index):
    return self.rolls[roll_index] + self.rolls[roll_index + 1] == 10
```

```javascript
score() {
  let total = 0;
  let rollIndex = 0;

  for (let frame = 0; frame < 10; frame++) {
    if (this.isStrike(rollIndex)) { // Strike
      total += 10 + this.rolls[rollIndex + 1] + this.rolls[rollIndex + 2];
      rollIndex += 1;
    } else if (this.isSpare(rollIndex)) { // Spare
      total += 10 + this.rolls[rollIndex + 2];
      rollIndex += 2;
    } else {
      total += this.rolls[rollIndex] + this.rolls[rollIndex + 1];
      rollIndex += 2;
    }
  }

  return total;
}

isStrike(rollIndex) {
  return this.rolls[rollIndex] === 10;
}

isSpare(rollIndex) {
  return this.rolls[rollIndex] + this.rolls[rollIndex + 1] === 10;
}
```

**Run tests**: All should PASS.

---

### Step 5: Perfect Game

**Test First**:

```python
def test_perfect_game():
    """12 strikes = 300"""
    game = BowlingGame()
    for _ in range(12):
        game.roll(10)
    assert game.score() == 300
```

```javascript
test("perfect game", () => {
  const game = new BowlingGame();
  for (let i = 0; i < 12; i++) {
    game.roll(10);
  }
  expect(game.score()).toBe(300);
});
```

**Run test**: Should PASS with existing implementation!

The beauty of TDD: You already handled this case correctly.

---

### Step 6: More Test Cases

Add these tests to cover edge cases:

```python
def test_all_spares():
    """All spares with 5 pins each roll"""
    game = BowlingGame()
    for _ in range(21):  # 10 frames + bonus roll
        game.roll(5)
    assert game.score() == 150


def test_alternating_strikes_and_gutters():
    """Strike, gutter, gutter, repeat"""
    game = BowlingGame()
    for _ in range(5):
        game.roll(10)  # Strike
        game.roll(0)
        game.roll(0)
    assert game.score() == 50


def test_tenth_frame_spare():
    """Spare in 10th frame gets bonus roll"""
    game = BowlingGame()
    for _ in range(18):
        game.roll(0)
    game.roll(5)
    game.roll(5)  # Spare in 10th
    game.roll(5)  # Bonus roll
    assert game.score() == 15


def test_tenth_frame_strike():
    """Strike in 10th frame gets two bonus rolls"""
    game = BowlingGame()
    for _ in range(18):
        game.roll(0)
    game.roll(10)  # Strike in 10th
    game.roll(3)   # Bonus roll 1
    game.roll(4)   # Bonus roll 2
    assert game.score() == 17
```

---

## Complete Solution

### Python (pytest)

```python
class BowlingGame:
    """
    Bowling game scorer.

    Usage:
        game = BowlingGame()
        game.roll(10)  # Strike
        game.roll(5)
        game.roll(4)
        # ... continue rolling
        total = game.score()
    """

    def __init__(self):
        self.rolls = []

    def roll(self, pins: int) -> None:
        """
        Record a single roll.

        Args:
            pins: Number of pins knocked down (0-10)
        """
        self.rolls.append(pins)

    def score(self) -> int:
        """
        Calculate total score.

        Returns:
            Total score for the game
        """
        total = 0
        roll_index = 0

        for frame in range(10):
            if self.is_strike(roll_index):
                total += self.strike_score(roll_index)
                roll_index += 1
            elif self.is_spare(roll_index):
                total += self.spare_score(roll_index)
                roll_index += 2
            else:
                total += self.frame_score(roll_index)
                roll_index += 2

        return total

    def is_strike(self, roll_index: int) -> bool:
        """Check if roll is a strike."""
        return self.rolls[roll_index] == 10

    def is_spare(self, roll_index: int) -> bool:
        """Check if frame is a spare."""
        return self.rolls[roll_index] + self.rolls[roll_index + 1] == 10

    def strike_score(self, roll_index: int) -> int:
        """Calculate score for strike frame."""
        return 10 + self.rolls[roll_index + 1] + self.rolls[roll_index + 2]

    def spare_score(self, roll_index: int) -> int:
        """Calculate score for spare frame."""
        return 10 + self.rolls[roll_index + 2]

    def frame_score(self, roll_index: int) -> int:
        """Calculate score for normal frame."""
        return self.rolls[roll_index] + self.rolls[roll_index + 1]


# Tests
class TestBowlingGame:
    def test_gutter_game(self):
        """All gutter balls"""
        game = BowlingGame()
        self.roll_many(game, 20, 0)
        assert game.score() == 0

    def test_all_ones(self):
        """All rolls knock down 1 pin"""
        game = BowlingGame()
        self.roll_many(game, 20, 1)
        assert game.score() == 20

    def test_one_spare(self):
        """One spare, then 3, then all gutters"""
        game = BowlingGame()
        game.roll(5)
        game.roll(5)  # Spare
        game.roll(3)
        self.roll_many(game, 17, 0)
        assert game.score() == 16

    def test_one_strike(self):
        """One strike, then 3 and 4, then all gutters"""
        game = BowlingGame()
        game.roll(10)  # Strike
        game.roll(3)
        game.roll(4)
        self.roll_many(game, 16, 0)
        assert game.score() == 24

    def test_perfect_game(self):
        """12 strikes"""
        game = BowlingGame()
        self.roll_many(game, 12, 10)
        assert game.score() == 300

    def test_all_spares(self):
        """All spares with 5 pins each"""
        game = BowlingGame()
        self.roll_many(game, 21, 5)
        assert game.score() == 150

    def test_tenth_frame_spare(self):
        """Spare in 10th frame"""
        game = BowlingGame()
        self.roll_many(game, 18, 0)
        game.roll(5)
        game.roll(5)  # Spare
        game.roll(5)  # Bonus
        assert game.score() == 15

    def test_tenth_frame_strike(self):
        """Strike in 10th frame"""
        game = BowlingGame()
        self.roll_many(game, 18, 0)
        game.roll(10)  # Strike
        game.roll(3)
        game.roll(4)
        assert game.score() == 17

    def test_complex_game(self):
        """Mix of strikes, spares, and regular frames"""
        game = BowlingGame()
        game.roll(10)  # Strike
        game.roll(7)
        game.roll(3)   # Spare
        game.roll(9)
        game.roll(0)
        game.roll(10)  # Strike
        game.roll(0)
        game.roll(8)
        game.roll(8)
        game.roll(2)   # Spare
        game.roll(0)
        game.roll(6)
        game.roll(10)  # Strike
        game.roll(10)  # Strike
        game.roll(10)  # Strike in 10th
        game.roll(8)
        game.roll(1)   # Bonus rolls
        assert game.score() == 167

    def roll_many(self, game, rolls, pins):
        """Helper: roll same pins multiple times"""
        for _ in range(rolls):
            game.roll(pins)
```

### JavaScript (Jest)

```javascript
class BowlingGame {
  constructor() {
    this.rolls = [];
  }

  roll(pins) {
    this.rolls.push(pins);
  }

  score() {
    let total = 0;
    let rollIndex = 0;

    for (let frame = 0; frame < 10; frame++) {
      if (this.isStrike(rollIndex)) {
        total += this.strikeScore(rollIndex);
        rollIndex += 1;
      } else if (this.isSpare(rollIndex)) {
        total += this.spareScore(rollIndex);
        rollIndex += 2;
      } else {
        total += this.frameScore(rollIndex);
        rollIndex += 2;
      }
    }

    return total;
  }

  isStrike(rollIndex) {
    return this.rolls[rollIndex] === 10;
  }

  isSpare(rollIndex) {
    return this.rolls[rollIndex] + this.rolls[rollIndex + 1] === 10;
  }

  strikeScore(rollIndex) {
    return 10 + this.rolls[rollIndex + 1] + this.rolls[rollIndex + 2];
  }

  spareScore(rollIndex) {
    return 10 + this.rolls[rollIndex + 2];
  }

  frameScore(rollIndex) {
    return this.rolls[rollIndex] + this.rolls[rollIndex + 1];
  }
}

describe("BowlingGame", () => {
  let game;

  beforeEach(() => {
    game = new BowlingGame();
  });

  function rollMany(n, pins) {
    for (let i = 0; i < n; i++) {
      game.roll(pins);
    }
  }

  test("gutter game", () => {
    rollMany(20, 0);
    expect(game.score()).toBe(0);
  });

  test("all ones", () => {
    rollMany(20, 1);
    expect(game.score()).toBe(20);
  });

  test("one spare", () => {
    game.roll(5);
    game.roll(5);
    game.roll(3);
    rollMany(17, 0);
    expect(game.score()).toBe(16);
  });

  test("one strike", () => {
    game.roll(10);
    game.roll(3);
    game.roll(4);
    rollMany(16, 0);
    expect(game.score()).toBe(24);
  });

  test("perfect game", () => {
    rollMany(12, 10);
    expect(game.score()).toBe(300);
  });

  test("all spares", () => {
    rollMany(21, 5);
    expect(game.score()).toBe(150);
  });

  test("tenth frame spare", () => {
    rollMany(18, 0);
    game.roll(5);
    game.roll(5);
    game.roll(5);
    expect(game.score()).toBe(15);
  });

  test("tenth frame strike", () => {
    rollMany(18, 0);
    game.roll(10);
    game.roll(3);
    game.roll(4);
    expect(game.score()).toBe(17);
  });

  test("complex game", () => {
    game.roll(10);
    game.roll(7);
    game.roll(3);
    game.roll(9);
    game.roll(0);
    game.roll(10);
    game.roll(0);
    game.roll(8);
    game.roll(8);
    game.roll(2);
    game.roll(0);
    game.roll(6);
    game.roll(10);
    game.roll(10);
    game.roll(10);
    game.roll(8);
    game.roll(1);
    expect(game.score()).toBe(167);
  });
});

module.exports = BowlingGame;
```

---

## Evaluation Criteria

| Criteria            | Points | Description                                  |
| ------------------- | ------ | -------------------------------------------- |
| **TDD Process**     | 20     | Tests written first, incremental development |
| **Correct Scoring** | 30     | All bowling rules implemented correctly      |
| **Edge Cases**      | 20     | 10th frame, perfect game, all spares handled |
| **Code Quality**    | 20     | Clean design, helper methods, readable       |
| **Test Coverage**   | 10     | Comprehensive test suite                     |

**Total**: 100 points

---

## Common Mistakes

❌ **Tracking frames instead of rolls**  
✅ Store rolls in array, calculate frames during scoring

❌ **Special-casing 10th frame**  
✅ Frame-based iteration handles it naturally

❌ **Complex conditional logic**  
✅ Extract helper methods (isStrike, isSpare, etc.)

❌ **Not testing edge cases**  
✅ Test perfect game, all spares, 10th frame variations

❌ **Over-engineering early**  
✅ Let tests guide you to simple solution

---

## Tips for Success

1. **Follow Uncle Bob's Steps**: Don't try to solve it all at once
2. **Test Names as Documentation**: Clear test names explain rules
3. **Helper Methods**: Extract rollMany for cleaner tests
4. **Refactor Aggressively**: The final solution is surprisingly simple
5. **Trust the Process**: Tests will guide you to elegant design
6. **10th Frame**: Your solution should handle it without special cases
7. **Frame-based Thinking**: Iterate over 10 frames, not 20 rolls

---

## Design Lessons

This kata teaches:

- **Simple data structures**: Just an array of rolls
- **Calculated properties**: Score is computed, not stored
- **Look-ahead logic**: Strikes and spares peek at future rolls
- **Helper methods**: Extract complexity into named methods
- **Test-driven design**: Tests reveal the simplest approach

**The Surprise**: The final solution is only about 30 lines of code, yet handles all the complexity!

---

## Bonus Challenges

### Challenge 1: Add Validation

Validate:

- Pins must be 0-10
- Two rolls per frame can't exceed 10
- Game must have exactly 10 frames

```python
def test_invalid_pins_raises_error():
    game = BowlingGame()
    with pytest.raises(ValueError):
        game.roll(11)
```

### Challenge 2: Game State

Track game state:

```python
def is_game_complete(self) -> bool:
    """Check if game is finished"""
    pass

def current_frame(self) -> int:
    """Return current frame number (1-10)"""
    pass
```

### Challenge 3: Display Score Card

Generate scorecard:

```
Frame:   1   2   3   4   5   6   7   8   9   10
Rolls:  X   7/  9-  X   -8  8/  -6  X   X   X 8 1
Score:  20  39  48  66  74  90  96  126 154 167
```

---

## Deliverables

1. **Complete BowlingGame class** with all tests passing
2. **Test suite** covering all scenarios
3. **Git history** showing TDD progression
4. **Design explanation** (1 page) of your approach
5. **Scorecard sample** (optional) from complex game

---

## Resources

- [Uncle Bob's Bowling Game Kata](http://butunclebob.com/ArticleS.UncleBob.TheBowlingGameKata)
- [Bowling Game Kata Video](https://www.youtube.com/watch?v=OPGTD47wY78) - Robert C. Martin
- [Bowling Scoring Rules](https://en.wikipedia.org/wiki/Ten-pin_bowling#Scoring)

---

## Next Steps

1. Complete [Exercise 4: Roman Numerals Kata](./04-roman-numerals.md)
2. Review [Theory: Outside-In vs Inside-Out TDD](../theory/04-tdd-approaches.md)
3. Watch Uncle Bob's video of this kata
4. Try implementing with different data structures

---

**The Bowling Game Kata proves that TDD leads to elegant solutions for complex problems!**

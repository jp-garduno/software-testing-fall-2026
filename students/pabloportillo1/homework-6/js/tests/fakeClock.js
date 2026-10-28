const DAY_MS = 24 * 60 * 60 * 1000;

class FakeClock {
  constructor(start = new Date("2026-10-01T00:00:00Z")) {
    this.today = start;
    this.now = () => this.today;
  }

  advance(days) {
    this.today = new Date(this.today.getTime() + days * DAY_MS);
  }
}

module.exports = { FakeClock };

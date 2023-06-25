import java.lang.Math;

class PtL {
  private long x;
  private long y;

  public PtL(long x, long y) {
    this.x = x;
    this.y = y;
  }

  public PtL(int x, int y) {
    this.x = (long)x;
    this.y = (long)y;
  }

  @Override
  public boolean equals(Object other) {
    PtL otherPtL = (PtL)other;
    return this.x == otherPtL.x && this.y == otherPtL.y;
  }

  @Override
  public int hashCode() {
    return (int)(Long.hashCode(this.x) + Long.hashCode(this.y));
  }

  public PtL add(PtL other) {
    return new PtL(this.x + other.x, this.y + other.y); 
  }

  public long manhattanDistance(PtL other) {
    return Math.abs(this.x - other.x) + Math.abs(this.y - other.y);
  }

  public long x() { return this.x; }
  public long y() { return this.y; }

  public String toString() {
    return "PtL(" + x() + ", " + y() + ")";
  }
}
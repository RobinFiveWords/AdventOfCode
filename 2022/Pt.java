import java.lang.Math;

class Pt {
  private int x;
  private int y;

  public Pt(int x, int y) {
    this.x = x;
    this.y = y;
  }

  @Override
  public boolean equals(Object other) {
    Pt otherPt = (Pt)other;
    return this.x == otherPt.x && this.y == otherPt.y;
  }

  @Override
  public int hashCode() {
    return this.x ^ (this.y << 16);
  }

  public Pt add(Pt other) {
    return new Pt(this.x + other.x, this.y + other.y); 
  }

  public int manhattanDistance(Pt other) {
    return Math.abs(this.x - other.x) + Math.abs(this.y - other.y);
  }

  public int x() { return this.x; }
  public int y() { return this.y; }

  public String toString() {
    return "Pt(" + x() + ", " + y() + ")";
  }
}
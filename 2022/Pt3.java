import java.lang.Math;

class Pt3 {
  private int x;
  private int y;
  private int z;

  public Pt3(int x, int y, int z) {
    this.x = x;
    this.y = y;
    this.z = z;
  }

  @Override
  public boolean equals(Object other) {
    Pt3 otherPt3 = (Pt3)other;
    return (this.x == otherPt3.x
            && this.y == otherPt3.y
            && this.z == otherPt3.z);
  }

  @Override
  public int hashCode() {
    return this.x ^ (this.y << 10) ^ (this.z << 20);
  }

  public Pt3 add(Pt3 other) {
    return new Pt3(this.x + other.x,
                   this.y + other.y,
                   this.z + other.z); 
  }

  public int manhattanDistance(Pt3 other) {
    return (Math.abs(this.x - other.x)
            + Math.abs(this.y - other.y)
            + Math.abs(this.z - other.z));
  }

  public int x() { return this.x; }
  public int y() { return this.y; }
  public int z() { return this.z; }

  public String toString() {
    return "Pt3(" + x() + ", " + y() + ", " + z() + ")";
  }
}
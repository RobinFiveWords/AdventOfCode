import java.util.HashSet;
import java.util.Set;

public class Day06 {

    public static void main(String[] args) throws Exception {
        String[] data = aocUtils.bufferLinesFromFile("2022day06input.txt");
        assert data.length == 1;
        assert findMarker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4) == 10;
        assert findMarker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29;
        int part1 = findMarker(data[0], 4);
        System.out.println("Day 6 part 1: " + part1);
        int part2 = findMarker(data[0], 14);
        System.out.println("Day 6 part 2: " + part2);
    }

    private static int findMarker(String s, int window) {
        int result = 0;
        Set<Character> set = new HashSet<Character>();
        for (int i = 0; i < s.length() - 3; i++) {
            for (int j = 0; j < window; j++) {
                set.add(s.charAt(i + j));
            }
            if (set.size() == window) return i + window;
            set.clear();
        }
        return result;
    }
}
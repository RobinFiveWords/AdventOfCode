import java.util.HashSet;
import java.util.Set;

public class Day03 {

    public static void main(String[] args) throws Exception {
        String[] data = aocUtils.readLinesFromFileIntoArray("2022day03input.txt");
        int part1 = do_part1(data);
        System.out.println("Day 3 part 1: " + part1);
        int part2 = do_part2(data);
        System.out.println("Day 3 part 2: " + part2);
    }

    private static int priority(char character) {
        int ascii = (int) character;
        if (ascii > 96) {
            return ascii - 96;  // lowercase 97-122, assigned to 1-26
        } else {
            return ascii - 38;  // uppercase 65-96, assigned to 27-52
        }
    }

    private static int do_part1(String[] data) {
        int result = 0;
        for (int i = 0; i < data.length; i++) {
            int midpoint = data[i].length() / 2;
            Set<Character> left = new HashSet<Character>();
            for (int j = 0; j < midpoint; j++) {
                left.add(data[i].charAt(j));
            }
            Set<Character> right = new HashSet<Character>();
            for (int j = midpoint; j < data[i].length(); j++) {
                right.add(data[i].charAt(j));
            }
            left.retainAll(right);
            assert left.size() == 1;
            for (char character :left) {
                result += priority(character);
            }
        }
        return result;
    }

    private static int do_part2(String[] data) {
        int result = 0;
        for (int i = 0; i < data.length; i += 3) {
            Set<Character> elf1 = new HashSet<Character>();
            for (int j = 0; j < data[i].length(); j++) {
                elf1.add(data[i].charAt(j));
            }
            Set<Character> elf2 = new HashSet<Character>();
            for (int j = 0; j < data[i+1].length(); j++) {
                elf2.add(data[i+1].charAt(j));
            }
            Set<Character> elf3 = new HashSet<Character>();
            for (int j = 0; j < data[i+2].length(); j++) {
                elf3.add(data[i+2].charAt(j));
            }
            elf1.retainAll(elf2);
            elf1.retainAll(elf3);
            assert elf1.size() == 1;
            for (char character :elf1) {
                result += priority(character);
            }
        }
        return result;
    }
}
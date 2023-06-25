import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class Day01 {
    
    public static void main(String[] args) throws Exception {
        String[] data = aocUtils.readLinesFromFileIntoArray("2022day01input.txt");
        int part1 = do_part1(data);
        System.out.println("Day 1 part 1: " + part1);
        int part2 = do_part2(data);
        System.out.println("Day 1 part 2: " + part2);
    }

    private static int do_part1(String[] data) {
        int result = 0;
        int current = 0;
        for (int i = 0; i < data.length; i++) {
            if (data[i].length() == 0) {
                if (current > result) {
                    result = current;
                }
            current = 0;
            } else {
                current += Integer.valueOf(data[i]);
            }
        }
        return result;
    }

    private static int do_part2(String[] data) {
        int counter = 1;  // each blank row represents an additional elf
        for (int i = 0; i < data.length; i++) {
            if (data[i].length() == 0) {
                counter++;
            }
        }
        Integer[] elves = new Integer[counter];  // arrays of primitive types like int[] can't be sorted in reverse order
        Arrays.fill(elves, 0);                   // arrays of objects are initialized as null
        int elf = 0;
        for (int i = 0; i < data.length; i++) {
            if (data[i].length() == 0) {
                elf++;
            } else {
                elves[elf] += Integer.valueOf(data[i]);
            }
        }
        Arrays.sort(elves, Collections.reverseOrder());
        int result = 0;
        for (int i = 0; i < 3; i++) {
            result += elves[i];
        }
        return result;
    }
}
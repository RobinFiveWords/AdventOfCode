public class Day04 {

    public static void main(String[] args) throws Exception {
        String[] data = aocUtils.readLinesFromFileIntoArray("2022day04input.txt");
        int part1 = do_part1(data);
        System.out.println("Day 4 part 1: " + part1);
        int part2 = do_part2(data);
        System.out.println("Day 4 part 2: " + part2);
    }

    private static int do_part1(String[] data) {
        int result = 0;
        for (int i = 0; i < data.length; i++) {
            int[] ints = aocUtils.parseInts(data[i]);
            int a = ints[0];
            int b = ints[1];
            int c = ints[2];
            int d = ints[3];
            assert a <= b && c <= d;
            if ((a <= c && b >= d) || (c <= a && d >= b)) {
                result++;
            }
        }
        return result;
    }

    private static int do_part2(String[] data) {
        int result = 0;
        for (int i = 0; i < data.length; i++) {
            int[] ints = aocUtils.parseInts(data[i]);
            int a = ints[0];
            int b = ints[1];
            int c = ints[2];
            int d = ints[3];
            assert a <= b && c <= d;
            if ((a <= c && b >= d) || (c <= a && d >= b) ||
                (a <= d && b >= c) || (c <= b && d >= a)) {
                result++;
            }
        }
        return result;
    }
}
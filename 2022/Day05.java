import java.util.ArrayList;
import java.util.List;

public class Day05 {

    public static void main(String[] args) throws Exception {
        String[] data = aocUtils.bufferLinesFromFile("2022day05input.txt");
        String part1 = do_part1(data);
        System.out.println("Day 5 part 1: " + part1);
        String part2 = do_part2(data);
        System.out.println("Day 5 part 2: " + part2);
    }

    private static String do_part1(String[] data) {
        int rowCounter = 0;
        Stack<String> stackInput = new Stack<String>();
        for ( ; ; rowCounter++) {
            if (data[rowCounter].length() == 0) {
                rowCounter++;
                break;
            }
            stackInput.push(data[rowCounter]);
        }
        Queue<String> instructions = new Queue<String>();
        for ( ; rowCounter < data.length; rowCounter++) {
            instructions.enqueue(data[rowCounter]);
        }

        String piles = stackInput.pop();
        int[] pileNums = aocUtils.parseInts(piles);

        List<Stack<Character>> stacks = new ArrayList<Stack<Character>>();
        for (int i = 0; i < pileNums.length + 1; i++) {
            stacks.add(new Stack<Character>());
        }

        while (!stackInput.isEmpty()) {
            String row = stackInput.pop();
            for (int i = 0; i < piles.length(); i++) {
                if (piles.charAt(i) == ' ') continue;
                int pile = Character.getNumericValue(piles.charAt(i));
                try {
                    if (row.charAt(i) == ' ') continue;
                } catch (ArrayIndexOutOfBoundsException e) {
                    continue;
                }
                stacks.get(pile).push(row.charAt(i));
            }
        }

        // check what's in the stacks
        // for (int i = 1; i < stacks.length; i++) {
        //     System.out.print(i);
        //     while (!stacks[i].isEmpty()) {
        //         System.out.print(" " + stacks[i].pop());
        //     }
        //     System.out.println();
        // }

        while (!instructions.isEmpty()) {
            String instruction = instructions.dequeue();
            int[] nums = aocUtils.parseInts(instruction);
            assert nums.length == 3;
            int quantity = nums[0];
            int pileFrom = nums[1];
            int pileTo = nums[2];
            for (int i = 0; i < quantity; i++) {
                stacks.get(pileTo).push(stacks.get(pileFrom).pop());
            }
        }

        char[] results = new char[pileNums.length];
        for (int i = 1; i < stacks.size(); i++) {
            results[i-1] = stacks.get(i).pop();
        }

        return String.valueOf(results);
    }

    private static String do_part2(String[] data) {
        int rowCounter = 0;
        Stack<String> stackInput = new Stack<String>();
        for ( ; ; rowCounter++) {
            if (data[rowCounter].length() == 0) {
                rowCounter++;
                break;
            }
            stackInput.push(data[rowCounter]);
        }
        Queue<String> instructions = new Queue<String>();
        for ( ; rowCounter < data.length; rowCounter++) {
            instructions.enqueue(data[rowCounter]);
        }

        String piles = stackInput.pop();
        int[] pileNums = aocUtils.parseInts(piles);

        List<Stack<Character>> stacks = new ArrayList<Stack<Character>>();
        for (int i = 0; i < pileNums.length + 1; i++) {
            stacks.add(new Stack<Character>());
        }

        while (!stackInput.isEmpty()) {
            String row = stackInput.pop();
            for (int i = 0; i < piles.length(); i++) {
                if (piles.charAt(i) == ' ') continue;
                int pile = Character.getNumericValue(piles.charAt(i));
                try {
                    if (row.charAt(i) == ' ') continue;
                } catch (ArrayIndexOutOfBoundsException e) {
                    continue;
                }
                stacks.get(pile).push(row.charAt(i));
            }
        }

        while (!instructions.isEmpty()) {
            String instruction = instructions.dequeue();
            int[] nums = aocUtils.parseInts(instruction);
            assert nums.length == 3;
            int quantity = nums[0];
            int pileFrom = nums[1];
            int pileTo = nums[2];
            Stack<Character> temp = new Stack<Character>();
            for (int i = 0; i < quantity; i++) {
                temp.push(stacks.get(pileFrom).pop());
            }
            while (!temp.isEmpty()) {
                stacks.get(pileTo).push(temp.pop());
            }
        }

        char[] results = new char[pileNums.length];
        for (int i = 1; i < stacks.size(); i++) {
            results[i-1] = stacks.get(i).pop();
        }

        return String.valueOf(results);
    }
}
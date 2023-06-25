import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

// if the contents of an ArrayList are being stored,
// and the ArrayList will be reused, need to store a copy
// because otherwise it's a reference to the values that will change

// oh so many logic errors from using == for String instead of .equals()

// substrings of String are still String, not char

class Day07 {
    static String TEST_INPUT_FILE = "2022day07testinput.txt";
    static String INPUT_FILE = "2022day07input.txt";

    static long TOTAL_DISK_SPACE = 70000000L;
    static long UNUSED_SPACE_NEEDED = 30000000L;

    public static void main(String[] args) throws Exception {
        String[] testData = aocUtils.bufferLinesFromFile("2022day07testinput.txt");
        List<ParsedOne> testTerminal = parseTerminal(testData);
        HashMap<String, Long> testDirSizes = walk(testTerminal);
        // for (Map.Entry<String, Long> ds : testDirSizes.entrySet()) {
        //     System.out.println(ds.getKey() + " " + ds.getValue());
        // }
        assert testDirSizes.get("/") == 48381165L;
        assert testDirSizes.get("/d/") == 24933642L;
        assert testDirSizes.get("/a/") == 94853L;
        assert testDirSizes.get("/a/e/") == 584L;
        assert totalSizeLE(testDirSizes, 100000L) == 95437L;
        assert smallestDirFreeUp(testDirSizes,
                                 TOTAL_DISK_SPACE,
                                 UNUSED_SPACE_NEEDED) == 24933642L;

        String[] realData = aocUtils.bufferLinesFromFile("2022day07input.txt");
        List<ParsedOne> realTerminal = parseTerminal(realData);
        HashMap<String, Long> realDirSizes = walk(realTerminal);
        long part1 = totalSizeLE(realDirSizes, 100000L);
        System.out.println("Day 7 part 1: " + part1);
        long part2 = smallestDirFreeUp(realDirSizes,
                                       TOTAL_DISK_SPACE,
                                       UNUSED_SPACE_NEEDED);
        System.out.println("Day 7 part 2: " + part2);
    }

    private static class ParsedOne {
        private String instruction;
        private List<String> output;

        public ParsedOne(String instruction, List<String> output) {
            this.instruction = instruction;
            this.output = output;
        }
    }

    private static List<ParsedOne> parseTerminal(String[] data) {
        List<ParsedOne> terminal = new ArrayList<ParsedOne>();

        String instruction = null;
        List<String> output = new ArrayList<String>();
        for (String row : data) {
            String[] tokens = row.split(" ");
            if (tokens[0].equals("$")) {
                terminal.add(new ParsedOne(instruction,
                                           new ArrayList<String>(output)));
                instruction = String.join(" ",
                                          Arrays.copyOfRange(tokens,
                                                             1,
                                                             tokens.length));
                output.clear();
            } else {
                output.add(row);
            }
        }
        if (instruction != null) {
            terminal.add(new ParsedOne(instruction, output));
        }
        return terminal.subList(1, terminal.size());
    }

    private static HashMap<String, Long> walk(List<ParsedOne> terminal) {
        String wd = "/"; // working directory
        HashMap<String, Long> dirSizes = new HashMap<String, Long>();
        Set<String> dirStack = new HashSet<String>();

        for (ParsedOne term : terminal) {
            String[] instruction = term.instruction.split(" ");
            List<String> output = term.output;
            String command = instruction[0];
            if (command.equals("cd")) {
                String arg = instruction[1];
                if (arg.equals("/")) {
                    wd = "/";
                    dirStack.clear();
                    dirStack.add(wd);
                } else if (arg.equals("..")) {
                    dirStack.remove(wd);
                    String wdTrimSlash = wd.substring(0, wd.length() - 1);
                    int lastSlash = wdTrimSlash.lastIndexOf('/');
                    wd = wd.substring(0, lastSlash + 1);
                } else {
                    wd = wd + arg + "/";
                    dirStack.add(wd);
                }
            } else if (command.equals("ls")) {
                for (String row : output) {
                    String[] tokens = row.split(" ");
                    if (!tokens[0].equals("dir")) {
                        Long fileSize = Long.valueOf(tokens[0]);
                        for (String d : dirStack) {
                            dirSizes.put(
                                d, dirSizes.getOrDefault(
                                    d, 0L) + fileSize);
                        }
                    }
                }
            }
        }

        return dirSizes;
    }

    private static Long totalSizeLE(HashMap<String, Long> dirSizes,
                                    Long le) {
        Long result = 0L;
        Long dirSize;
        for (Map.Entry<String, Long> ds : dirSizes.entrySet()) {
            if ((dirSize = ds.getValue()) <= le) {
                result += dirSize;
            }
        }
        return result;
    }

    private static Long smallestDirFreeUp(HashMap<String, Long> dirSizes,
                                          Long total,
                                          Long unused) {
        Long current = total - dirSizes.get("/");
        assert unused > current : "already have enough unused space";
        Long needed = unused - current;
        Long result = total;
        Long dirSize;
        for (Map.Entry<String, Long> ds : dirSizes.entrySet()) {
            if ((dirSize = ds.getValue()) >= needed) {
                if (dirSize < result) {
                    result = dirSize;
                }
            }
        }
        return result;
    }
}